import os
from utils import s3 as s3Util
from utils import dynamodb as dynamodbUtil
import face_recognition
import pickle
import json
import numpy as np

INPUT_BUCKET_NAME = os.getenv("INPUT_S3_BUCKET_NAME")
INPUT_LOCAL_STORAGE_DIR = os.getenv("INPUT_LOCAL_STORAGE_DIR")
INPUT_FRAME_STORAGE_DIR = os.getenv("INPUT_FRAME_STORAGE_DIR")
ENCODING_PATH = os.getenv("ENCODING_PATH")

def extract_frames(videoPath):
	os.system("ffmpeg -i " + str(videoPath) + " -r 1 " + str(INPUT_FRAME_STORAGE_DIR) + "image-%3d.jpeg")

# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def compare_image_with_embeddings(framePath, encodingData):
	frame = face_recognition.load_image_file(framePath)
	frameEncodings = face_recognition.face_encodings(frame)
	resultName = ''
	faceRecognized = False
	if len(frameEncodings) == 0:
		return faceRecognized, resultName
	else:
		frameEncoding = frameEncodings[0]
		results = []
		for encoding in encodingData['encoding']:
			results.append(face_recognition.compare_faces([encoding], frameEncoding))
		resultIndex = np.argmax(results)
		resultName = encodingData['name'][resultIndex]
		faceRecognized = True
		return faceRecognized, resultName

def face_recognition_handler(event, context):	
	eventJson = json.loads(event)
	objectKey = eventJson['Records'][0]['s3']['object']['key']
	videoPath = s3Util.downloadVideoFromS3ToLocal(objectKey)
	extract_frames(videoPath)
	encodingData = open_encoding(ENCODING_PATH)
	frames = os.listdir(INPUT_FRAME_STORAGE_DIR)
	for frame in frames:
		faceRecognized, resultName = compare_image_with_embeddings(os.path.join(INPUT_FRAME_STORAGE_DIR, frame), encodingData)
		if faceRecognized:
			break
		dynamodbUtil.query_table(resultName) #TODO: query the dynamo db and write a csv in output bucket
	context.done(None, "Function executed successfully")
