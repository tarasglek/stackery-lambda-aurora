import boto3
import logging
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()
xray_recorder.configure(stream_sql=True)
import os
import sys
import json

db_name = 'mydb'
db_arn = os.environ['DB_ARN']
secret_arn = os.environ['DB_ROOT_USER_SECRET_ARN']

print(db_arn, secret_arn)
rdsData = boto3.client('rds-data')

@xray_recorder.capture("## sql_bla")
def sql(query):
    # document = xray_recorder.current_segment()
    xray_recorder.put_metadata("sql", query)
    # xray_recorder.put_metadata("my key", "my value");
    return rdsData.execute_statement(
        resourceArn = db_arn,
        secretArn = secret_arn,
        database = db_name,
        sql = query)

def handler(message, context):
    response1 = sql("SELECT COUNT(*) from sample_table")
    response2 = sql("SELECT * from sample_table")
    ret = [response1['records'], response2['records']]
    return {'statusCode':200, 'body':json.dumps(ret)}