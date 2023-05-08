import boto3
import os


# Push DF to AWS bucket
aws_access_key_id = ''
aws_secret_access_key = ''
bucket_name = 'mda-test'
local_folder_path = 'Dataset/'

def upload_to_s3(local_file_path, bucket_name, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        with open(local_file_path, 'rb') as file:
            s3.upload_fileobj(file, bucket_name, s3_key)
            print(f"File {local_file_path} uploaded to {bucket_name}/{s3_key}.")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

# List of file names you want to upload
files_to_upload = os.listdir('Dataset/')

for file_name in files_to_upload:
    local_file_path = os.path.join(local_folder_path, file_name)
    s3_key = file_name
    upload_to_s3(local_file_path, bucket_name, s3_key)