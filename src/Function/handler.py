import boto3
import pymysql
import os
import logging
import sys
import json

rds_host = os.environ['DB_ADDRESS']
name = 'root'
password = '~<nqs6EUz;-ozaRP'
db_name = 'db'
port = os.environ['DB_PORT']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

print("db info", json.dumps([rds_host,port, name, password, db_name ]))
try:
  conn = pymysql.connect(rds_host, port=port ,user=name, passwd=password, db=db_name, connect_timeout=10000)
  print(conn)
except:
  logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
  sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(message, context):
  with conn.cursor() as cur:
    sql = "SELECT * from sample_table"
    cur.execute(sql)
    for row in cur:
      print(repr(row))