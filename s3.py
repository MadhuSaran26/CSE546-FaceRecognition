import boto3
import os
from dotenv import load_dotenv
load_dotenv()

S3_SERVICE = os.getenv("S3_SERVICE")
INPUT_BUCKET_NAME = os.getenv("INPUT_S3_BUCKET_NAME")
INPUT_S3_FILE_LOCATION = os.getenv("S3_LOCATION").format(INPUT_BUCKET_NAME)
OUTPUT_BUCKET_NAME = os.getenv("OUTPUT_S3_BUCKET_NAME")
OUTPUT_S3_FILE_LOCATION = os.getenv("S3_LOCATION").format(OUTPUT_BUCKET_NAME)
INPUT_LOCAL_STORAGE_DIR = os.getenv("INPUT_LOCAL_STORAGE_DIR")
INPUT_FRAME_STORAGE_DIR = os.getenv("INPUT_FRAME_STORAGE_DIR")
OUTPUT_FILE_DIRECTORY = os.getenv("OUTPUT_FILE_DIRECTORY")

s3Client = boto3.client(S3_SERVICE)

def downloadVideoFromS3ToLocal(key):
    if not os.path.exists(INPUT_LOCAL_STORAGE_DIR):
        os.makedirs(INPUT_LOCAL_STORAGE_DIR)
    try:
        fileName = key
        localPath = os.path.join(INPUT_LOCAL_STORAGE_DIR, fileName)
        s3Client.download_file(
            INPUT_BUCKET_NAME,
            key,
            localPath
        )
    except Exception as exception:
        print("Exception in downloading file to local", exception)
        return exception
    return "{}{}".format(localPath, key)

def addResultObjectToS3(imageName):
    filepath = OUTPUT_FILE_DIRECTORY + '/' + imageName + '.csv'
    print(filepath)
    try:
        s3Client.upload_file(filepath, OUTPUT_BUCKET_NAME, imageName + '.csv')
    except Exception as exception:
        print("Exception in uploading result from App Instance", exception)
        return exception
    return "{}{}".format(OUTPUT_S3_FILE_LOCATION, imageName)
