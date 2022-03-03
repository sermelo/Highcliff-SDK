import boto3
import os
import uuid

# import dynamodb resource from boto module
dynamodb = boto3.resource('dynamodb')

# get table name from environment
TABLE = os.environ['TABLE']

# define lambda function
# this will generate a sample id and push to table
def lambda_handler(event, context) -> None:
    table = dynamodb.Table(TABLE)

    response = table.put_item(
        Item={
            'id': str(uuid.uuid4())
        })
 

