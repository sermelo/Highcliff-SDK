import boto3
import json
import os
import uuid
from datetime import datetime

# import dynamodb resource from boto module
dynamodb = boto3.resource('dynamodb')

# get env vars
TABLE = os.environ['TABLE']
REGION = os.environ['REGION']
TOPIC = os.environ['TOPIC']

# define lambda function:
# this will publish an mqtt message if an action is required
# in response to the current temperature level
def lambda_handler(event, context) -> None:
    table = dynamodb.Table(TABLE)
    
    
    client = boto3.client('iot-data', region_name=REGION)

    response = table.scan(
        TableName=TABLE)

    print(response['Items'])
    
    for x in response['Items']:
        if x['type'] == 'temperature':
            if int(x['value']) >= 39:
                action = 'temp_turn_down'
            elif int(x['value']) in (38, 37):
                action = 'maintain_temp'
            else:
                action = 'turn_temp_up'


            r = client.publish(
                topic=TOPIC,
                qos=1,
                payload=json.dumps({"device_id":x['device_id'], 
                                    "action":action, 
                                    "pre_change_detected_temp":str(x['value']), 
                                    "action_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                )
            
           