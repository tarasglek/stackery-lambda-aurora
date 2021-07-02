import boto3
import logging
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

import os
import sys
import json


rds_host = os.environ['DB_ADDRESS']
name = 'root'
password = '~<nqs6EUz;-ozaRP'
db_name = 'db'
port = os.environ['DB_PORT']

db_arn = os.environ['DB_ARN']
secret_arn = os.environ['DB_ROOT_USER_SECRET_ARN']

print(db_arn, secret_arn)
rdsData = boto3.client('rds-data')
def handler(message, context):
    sql = "SELECT * from sample_table"
    response1 = rdsData.execute_statement(
            resourceArn = db_arn,
            secretArn = secret_arn,
            database = 'mydb',
            sql = sql)
    print(response1)
    return {'statusCode':200, 'body':json.dumps(response1['records'])}