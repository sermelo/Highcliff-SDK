
# aws-data-ingest-model

AWS CDK stack used to setup IoT Greengrass on an ec2 instance, connected to other AWS services.


##  Setup

As a prerequisite the user should setup the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

The user should then configure the [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/cli.html) and install the [aws-cdk](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html) python libraries.

## Tagging

Prior to deployment, stack tags can be set in ~/app.py using the assigned variables:
```
org = 'SMF'
version = '1.0'
owner = 'dxc'
project = 'hackathon'
team = 'team1'
```
All resources created by the stack will be tagged with these values.

## Deployment

Note: please check ['Values to Change'](#values-to-change) section at the bottom of the page before proceeding.

To deploy the stack, the user should run the following command:

```
aws cdk deploy --context stack-name=<name> --context ec2-key<key-name>
```
`Flags:`

- `stack-name`: this value will be used when naming and tagging other resources deployed as part of the stack.

    Ensure this only consists of numbers and lowercase values, e.g. _ik9xlm_.
- `ec2-key`: the name of your ec2 key pair you would like to use to access the created ec2 instance.

## Components

The following components are deployed as part of the stack:

- `vpc, subnet, security group`: deployed as default to contain the ec2 instance. The security group has ingress rules configured to permit mqtt and ssh access.
- `ec2`: deployed with greengrass installed. The necessary certificates/keys are also generated and granted the correct permissions, to register the device with IoT Core. The device should appear under IoT Core 'Things', once initialization has complete.
- `dynamodb`: new table created with 'device_id' as the partition key and 'type' as the sort key.
- `s3`: provisioned to provide another means of arbitrary storage for the user.
- `kinesis firehose`: configured to stream data to s3.

## Examples

The following examples are deployed as part of the stack. Note: all examples are configured to run automatically on stack deployment, except for the Local Lambda Execution (5). 

1. `generate_data.py`: deployed under _/home/ubuntu_ to generate sample temperature data, publishing this to _'temps.csv'_. By default this is already running in the background on the ec2 isntance.

2. `monitor_temps.py`: located under _/home/ubuntu_ on the ec2 instance. This example publishes the temperature data from 'temps.csv' to the 'test/temperatures' mqtt messsage topic. It can be ran using the following command:
    ```
    ubuntu@ip:~# ./monitor_temps.py --client-id=<unique-name-for-device> --topic=<unique-topic-name>
    ```
    The data will be published to the topic, with the 'device_id' field containing the value supplied as '--client-id'.

    Note: _--topic_ should match the topic subscribed to by your lambda function.
 
3. `monitor_topic.py`: located under _/home/ubuntu_ on the ec2 instance. This example subscribe to the desired topic, or, by default, to all topics:
    ```
    ubuntu@ip:~# ./monitor_topic.py
    ```

4. `IoT Rule: push data to dyanamodb`: this rule obtains data from the 'test/temperatures' topic using the following SQL command:
    ```
    select * from 'test/temperatures'
    ```
    The returned json data is the split into fields which are pushed as columns to dynamobd.
    
5. `Lambda (cloud): temperature_feedback.py`: this reads the dynamodb table, detecting any rows containing a type of 'temperature'. Depending on the stored value, a message will be published to the _'test/temperatures-control'_ mqtt topic with a corresponding action. Scheduled by a CloudWatch event to run every 2 minutes.

6. `Lambda (on local device): local_temperature_feedback.py`: publishes the same data as _'temperature_feedback.py'_, but runs locally on the device to directly reads temperature data. 
    
    The requirements for this can be found in the repo under _~/iot/component_: _pack.sh_ is used to package the function into a zip file, which is then uploaded to s3 as part of the stack operations. The s3 location and function execution path are specified in _recipe.yaml_.

    To deploy the component, go to IoT Core > [Components](https://eu-west-2.console.aws.amazon.com/iot/home?region=eu-west-2#/greengrass/v2/components) > Your New Component > Select Deploy > Select your IoT thing as the device to deploy to > Follow remaining console steps to deploy component to your core device or a thing group.

    To ensure the lambda function is running, check that logs are being published on the ec2 instance:
    ```
    root@ip:/greengrass/v2/logs# ls
    aws.greengrass.Nucleus.log  dataingest.dosomething.7823.log  greengrass.log  main.log
    ```
    Checking that the function is publishing mqtt messages using the IoT Core [Test facility](https://eu-west-2.console.aws.amazon.com/iot/home?region=eu-west-2#/test) is also an option: for the demo, the user should subscribe to _'test/temperatures-control-local'_, once deployed.

## Removal

Stacks can be deleted by following the same procedure used to remove regular CloudFormation stacks.
Go to [CloudFormation](https://eu-west-2.console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks), select your stack, then _Delete_.

IoT Things need to be removed manually as these are not officially deployed as CloudFormation resources. Go to IoT Core [Things](https://eu-west-2.console.aws.amazon.com/iot/home?region=eu-west-2#/thinghub), then select your item, then _Delete_. Repeat the same action under [Greengrass Core Devices](https://eu-west-2.console.aws.amazon.com/iot/home?region=eu-west-2#/greengrass/v2/cores). 

## Values to Change

The following tables list changes which are required per deployment/subscription:

`PER STACK DEPLOYMENT:`

| File                          | Line | Variable | When                                                   | Description                                                                                   |
|-------------------------------|------|----------|--------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| local_temperature_feedback.py | 49   | TOPIC    | pre-deployment: change then run 'pack.sh' in local dir | var for local temp control topic                                                              |
| local_temperature_feedback.py | 51   | CLIENT   | pre-deployment: change then run 'pack.sh' in local dir | client name for mqtt json                                                                     |
| data_ingest_stack.py          | 154  | TOPIC    | pre-deployment                                         | var for global temp topic: publish to this with --topic when running monitor_temp.py on ec2 |
     

`PER SUBSCRIPTION:`

| File                          | Line | Variable | When                                                              | Description                                                    |
|-------------------------------|------|----------|-------------------------------------------------------------------|----------------------------------------------------------------|
| local_temperature_feedback.py | 45   | ENDPOINT | pre-deployment: change then run 'pack.sh' in local dir            | var for IoT Core Endpoint: available under Iot Core > Settings |
| monitor_temp.py               | 21   | ENDPOINT | pre-deployment: change then upload to smf-shared-resources bucket | var for IoT Core Endpoint: available under Iot Core > Settings |

NOTE:

The user will need to create the 'smf-shared-resources' bucket per subscription, then upload the following files:
- ~/iot/python/generate_data.py
- ~/iot/python/monitor_temp.py
- AmazonRootCA1.pem available [here](https://www.amazontrust.com/repository/).

The user will also need to create the following roles/policies (or renamed) per subscription:
- 'smf-data-ingest-role' role with inline policy ~/iam/data_ingest_policy.json
- 'smf-iot-cert-access' iot certificate inline policy ~/iam/iot_access_policy.json
- 'smf-iot-rule-handler' iot rule role with inline policy ~/iam/iot_access_policy.json

The user should also ensure that the default role _GreengrassV2TokenExchangeRole_ has permissions to access s3 (it should have s3:GetObject by default).
An inline policy can be created using ~/iam/iot_access_policy.json for this too, if needed.
Greengrass uses this role to obtain component artifacts from s3.






