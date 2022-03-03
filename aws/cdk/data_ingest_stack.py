from aws_cdk import (
    CfnParameter,
    Duration,
    RemovalPolicy,
    Stack,
    aws_ec2 as _ec2,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb,
    aws_events as _events,
    aws_events_targets as _events_targets,
    aws_iam as _iam,
    aws_iot as _iot,
    aws_greengrassv2 as _greengrass,
    aws_s3_deployment as _s3_deployment
)

import aws_solutions_constructs.aws_kinesis_firehose_s3 as _kinesisfirehose
from constructs import Construct
from random import randrange

import extensions

class DataIngestStack(Stack):
    

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # define cdk input parameters:
        # stack-name - all resources will include this in their name:
	   # GitHub Error 12 - add str() wrapper to force type
        self._resource_name = str(self.node.try_get_context('stack-name'))
        # ec2-key - key pair to access ec2:
        self._ec2_key = self.node.try_get_context('ec2-key')
        # define other vars:
        # these roles/policies have already been defined in IAM,
        # they can be recreated using the json files under ~/iam
        self._ec2_role = 'smf-data-ingest-role'        # role to be used by ec2 instance
        self._iot_cert_policy = 'smf-iot-cert-access'  # policy name to be applied to iot device cert
        self._iot_rule_role = 'smf-iot-rule-handler'   # role to be applied to iot topic rule

        
        # define new vpc and subnet
        vpc_ = _ec2.Vpc(self, 
                        id=self._resource_name + '-vpc', 
                        cidr='172.0.0.0/24',
                        subnet_configuration=[_ec2.SubnetConfiguration(name='public', 
                                                                       cidr_mask=28,
                                                                       map_public_ip_on_launch=True,
                                                                       subnet_type=_ec2.SubnetType.PUBLIC)])


        # define security group with ingress rules for traffic
        sg_ = _ec2.SecurityGroup(self,
                                 id=self._resource_name + '-sg', 
                                 vpc=vpc_,
                                 allow_all_outbound=True)
        sg_.add_ingress_rule(_ec2.Peer.any_ipv4(), _ec2.Port.tcp(22), 'Permit ssh access.')
        sg_.add_ingress_rule(_ec2.Peer.any_ipv4(), _ec2.Port.tcp(8883), 'Permit MQTT access.')
        
        
        # obtain user_data script for ec2 setup
        mappings = {'__CORE_NAME__': self._resource_name,
                    '__REGION__': self.region,
                    '__POLICY__': self._iot_cert_policy}
        user_data = extensions.fileVarMapper(mappings, 'user_data/user_data.sh')

        
        # define new ec2 instance
        instance_ = _ec2.Instance(self, 
            id=self._resource_name + '-ec2',
            instance_name=self._resource_name + '-ec2',
            instance_type=_ec2.InstanceType.of(_ec2.InstanceClass.BURSTABLE3, _ec2.InstanceSize.MICRO),
            machine_image=_ec2.MachineImage.generic_linux({'eu-west-2':'ami-0015a39e4b7c0966f'}),
            vpc=vpc_,
            key_name=self._ec2_key,
            security_group=sg_,
            role=_iam.Role.from_role_arn(self,
                                         role_arn='arn:aws:iam::' + self.account +':role/' + self._ec2_role,
                                         id=self._resource_name + '-ec2-role'),
            user_data=_ec2.UserData.custom(user_data)
            )
        
        # define new kinesis firehose with s3 collection bucket
        stream_ = _kinesisfirehose.KinesisFirehoseToS3(self, 
                                                       id=self._resource_name + '-firehose', 
                                                       log_s3_access_logs=False,
                                                       bucket_props={
                                                           'bucket_name': self._resource_name + '-bucket',
                                                           'auto_delete_objects': True,
                                                           'removal_policy': RemovalPolicy.DESTROY
                                                       },
                                                       kinesis_firehose_props={
                                                           'delivery_stream_name': self._resource_name + '-stream',
                                                       })


        # define new dynamodb instance
        dynamodb_ = _dynamodb.Table(self, 
                                    id=self._resource_name + '-dynamodb',
                                    table_name=self._resource_name + '-metadata',
                                    partition_key=_dynamodb.Attribute(
                                        name='device_id',
                                        type=_dynamodb.AttributeType.STRING
                                    ),
                                    sort_key=_dynamodb.Attribute(
                                        name='type',
                                        type=_dynamodb.AttributeType.STRING
                                    ),
                                    removal_policy=RemovalPolicy.DESTROY
                                    )


    ####### FOLLOWING BLOCKS ARE USED TO DEPLOY EXAMPLES #######

        # example topic rule:
        # this subscribes to the test/temperatures topic
        # then pushes the data to dynamodb
        topic_rule_= _iot.CfnTopicRule(self, id=self._resource_name + '-topic-rule',
            rule_name='smf_send_to_dynamodb_' + self._resource_name,
            topic_rule_payload=_iot.CfnTopicRule.TopicRulePayloadProperty(
                actions=[_iot.CfnTopicRule.ActionProperty(
                    dynamo_d_bv2=_iot.CfnTopicRule.DynamoDBv2ActionProperty(
                        put_item=_iot.CfnTopicRule.PutItemInputProperty(
                            table_name=dynamodb_.table_name
                        ),
                        role_arn='arn:aws:iam::' + self.account + ':role/' + self._iot_rule_role
                    )
                )],
                sql="select * from 'test/temperatures'"
            )
        )
        
        
        # define new lambda to run in the aws cloud:
        # action response to temperature level being too high
        temperature_control_ = _lambda.Function(self, 
                                          id=self._resource_name + '-push-dynamodb',
                                          runtime=_lambda.Runtime.PYTHON_3_8,
                                          handler='temperature_feedback.lambda_handler',
                                          code=_lambda.Code.from_asset('./lambda/consumer'),
                                          initial_policy=[_iam.PolicyStatement(
                                                          resources=['*'],
                                                          actions=['iot:Publish',
                                                                   'iot:Receive',
                                                                   'iot:RetainPublish',
                                                                   'iot:Subscribe',
                                                                   'iot:Connect',
                                                                   'logs:CreateLogGroup',
                                                                   'logs:CreateLogStream',
                                                                   'logs:PutLogEvents'],
                                                          effect=_iam.Effect.ALLOW)])
        temperature_control_.add_environment("TABLE", dynamodb_.table_name)
        temperature_control_.add_environment("REGION", self.region)
        temperature_control_.add_environment("TOPIC", 'test/temperatures-control') # simply for test purposes: change per stack deployment

        
        # grant lambda read/write permissions on new table
        dynamodb_.grant_read_write_data(temperature_control_)

        
        # define a cloudwatch periodic event to trigger lambda
        periodic_2m = _events.Rule(self,
                                   id=self._resource_name + '-event-1m',
                                   targets=[_events_targets.LambdaFunction(temperature_control_)],
                                   schedule=_events.Schedule.rate(Duration.minutes(2)))


        # deploy a sample lambda component
        # to be ran on the greengrass core ec2 instance:
        # upload sample python script to s3 bucket
        push_s3_ = _s3_deployment.BucketDeployment(self,
                                                   id=self._resource_name + '-push-s3',
                                                   destination_bucket=stream_.s3_bucket,
                                                   sources=[_s3_deployment.Source.asset('./iot/component/artifacts.zip')])

       
        # obtain iot component recipe
        mappings = {'__S3_BUCKET_NAME__': stream_.s3_bucket.bucket_name,
                    '__CORE_NAME__': self._resource_name}
        recipe = extensions.fileVarMapper(mappings, 'iot/component/recipe.yaml')
        

        # define new iot component
        component_ = _greengrass.CfnComponentVersion(self,
                                                     id=self._resource_name + '-iot-component',
                                                     inline_recipe=recipe)
        component_.node.add_dependency(push_s3_)
