# CDK Python alternative for genenrating the required role

# Add this to data_ingest_stack.py if you want a role to be created per stack:
# if this is added, set role=ec2_iot_role_ for the _ec2 instance 


        ec2_iot_role_ = _iam.Role(self,
                          id=self._resource_name + '-data-ingest-role',
                          role_name=self._resource_name + '-data-ingest-role',
                          managed_policies=[_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')],
                          assumed_by=_iam.ServicePrincipal('ec2.amazonaws.com')
                          )
        ec2_iot_role_.add_to_policy(_iam.PolicyStatement(resources=['*'],
                                                         actions=['iam:GetRole', 
                                                                  'iam:CreateRole', 
                                                                  'iam:PassRole', 
                                                                  'iam:CreatePolicy', 
                                                                  'iam:AttachRolePolicy',
                                                                  'iam:getPolicy'],
                                                         effect=_iam.Effect.ALLOW))                                                         
        ec2_iot_role_.add_to_policy(_iam.PolicyStatement(resources=['arn:aws:s3:::smf-shared-resources/*'],
                                                         actions=['s3:GetObject',
                                                                  's3:ListBucket',
                                                                  's3:GetBucketLocation',
                                                                  's3:GetObjectVersion'],
                                                         effect=_iam.Effect.ALLOW))
        ec2_iot_role_.add_to_policy(_iam.PolicyStatement(resources=['arn:aws:s3:::*'],
                                                         actions=['s3:ListAllMyBuckets'],
                                                         effect=_iam.Effect.ALLOW))
        ec2_iot_role_.add_to_policy(_iam.PolicyStatement(resources=['*'],
                                                         actions=['iot:Publish',
                                                                  'iot:Receive',
                                                                  'iot:RetainPublish',
                                                                  'iot:Subscribe',
                                                                  'iot:Connect',
                                                                  'iot:AttachThingPrincipal',
                                                                  'iot:AttachPolicy',
                                                                  'iot:AttachPrincipalPolicy'],
                                                         effect=_iam.Effect.ALLOW))