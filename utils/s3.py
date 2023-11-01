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

s3Client = boto3.client(S3_SERVICE)

def addVideoToS3ForAPI(fileToUploadPath, bucket, fileNameInS3, userIp): #TODO: Not sure whether upload_file can be used for videos as well
    try:
        s3Client.upload_file(
            fileToUploadPath,
            bucket,
            fileNameInS3
        )
        s3Client.put_object_tagging(
            Bucket=bucket,
            Key=fileNameInS3,
            Tagging={'TagSet': [{'Key': 'UserIP', 'Value': userIp}]}
        )
    except Exception as exception:
        print("Exception in uploading file from API", exception)
        return exception
    return "{}{}".format(INPUT_S3_FILE_LOCATION, fileNameInS3)

def downloadVideoFromS3ToLocal(key):
    if not os.path.exists(INPUT_LOCAL_STORAGE_DIR):
        os.makedirs(INPUT_LOCAL_STORAGE_DIR)
    try:
        response = s3Client.get_object_tagging(
            Bucket=INPUT_BUCKET_NAME,
            Key=key
        )
        for tag in response['TagSet']:
            if tag['Key'] == 'UserIP':
                userIp = tag['Value']
            else:
                userIp = ""
        fileName = key + ":" + userIp
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

def addResultObjectToS3(imageName, imageResult): #TODO: Need to edit this to store the output in .csv file format
    try:
        keyList = imageName.split(":")
        s3Client.put_object(
            Bucket=OUTPUT_BUCKET_NAME,
            Key=keyList[0],
            Body=imageResult.encode('utf-8'),
            ContentType='text/plain'
        )
        s3Client.put_object_tagging(
            Bucket=OUTPUT_BUCKET_NAME,
            Key=keyList[0],
            Tagging={'TagSet': [{'Key': 'UserIP', 'Value': keyList[1]}]}
        )
    except Exception as exception:
        print("Exception in uploading result from App Instance", exception)
        return exception
    return "{}{}".format(OUTPUT_S3_FILE_LOCATION, keyList[0])
