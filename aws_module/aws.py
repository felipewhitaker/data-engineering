from typing import get_args
import boto3 #type: ignore

import time

from botocore import exceptions #type: ignore
from botocore.exceptions import ClientError #type: ignore

import logging
import logging
logging.getLogger()
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.ERROR)
from dotenv import load_dotenv #type: ignore
from os import getenv

load_dotenv('./.env')

s3_client = boto3.client(
    's3',
    aws_access_key_id = getenv('AWS_ID'),
    aws_secret_access_key = getenv('AWS_KEY')
)

bucket_name = 'thor-s3-bucket'
try:
    s3_client.create_bucket(Bucket = bucket_name)
    logging.info(f'Created {bucket_name} with success')
except ClientError:
    logging.error(f'Could not create {bucket_name}')
    quit()

time.sleep(10)
s3_client.delete_bucket(Bucket = bucket_name)