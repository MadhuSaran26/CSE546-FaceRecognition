import boto3
import os

DYNAMODB_SERVICE = os.getenv("DYNAMODB_SERVICE")
TABLE_NAME = os.getenv("TABLE_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")

dynamodbClient = boto3.client(DYNAMODB_SERVICE)

def query_table(resultName):
    pass
