import boto3
import os
from dotenv import load_dotenv
load_dotenv()

DYNAMODB_SERVICE = os.getenv("DYNAMODB_SERVICE")
TABLE_NAME = os.getenv("TABLE_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")
AWS_REGION = os.getenv("AWS_REGION")

dynamodbClient = boto3.client(DYNAMODB_SERVICE, region_name=AWS_REGION)

def query_table(resultName):
    pass
