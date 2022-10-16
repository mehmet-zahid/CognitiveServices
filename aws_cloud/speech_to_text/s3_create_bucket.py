import boto3
import uuid
import os
import botocore.exceptions

s3_resource = boto3.resource('s3')
first_bucket_name = 'mehmet-aibucket-1'
second_bucket_name = 'pythonaitest03ac4061-a907-4ad7-84bc-3a2aa39ae930'


def create_bucket_name(bucket_prefix):
    # the generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])


def create_bucket(bucket_prefix, s3_connection):
    session = boto3.Session()
    current_region = session.region_name
    print(current_region)
    bucket_name = create_bucket_name(bucket_prefix)
    try:
        bucket_response = s3_connection.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
             'LocationConstraint': 'eu-west-2'})
        print(bucket_name, current_region)
        return bucket_name, bucket_response
    except botocore.exceptions.ClientError as err:
        print(err)


def upload_files(files: list, bucket_name):
    for file in files:
        s3_resource.Bucket(bucket_name).upload_file(Filename=file["filepath"], Key=file["filename"])


def get_files(folder_path):
    files_to_upload = []
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            files_to_upload.append({"filename": name,
                                    "filepath": os.path.join(root, name)})
            print(f"{name} Added")
    return files_to_upload


audio_files_path = "C:\\Users\\Mehmet\\Desktop\\audios"

upload_files(files=get_files(audio_files_path), bucket_name=second_bucket_name)






























