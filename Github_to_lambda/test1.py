import json
import pymysql.cursors
import boto3 
from botocore.client import ClientError
session = boto3.session.Session()
Client = session.client('secretsmanager')
secret_response={}
keys={}
try:
    secret_response = Client.get_secret_value(
        SecretId='aws-key-eventswedo-db',VersionStage='AWSCURRENT')
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        print("The requested secret " + "secret_name" + " was not found")
keys=json.loads(secret_response['SecretString'])
print(keys["access_key"])