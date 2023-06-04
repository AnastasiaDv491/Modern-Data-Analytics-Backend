import boto3
import os

bucket_name = 'mda-test'
local_folder_path = 'Predictions/Predictions/'

def upload_to_s3(local_file_path, bucket_name, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id="",
        aws_secret_access_key = ""
    )

    try:
        with open(local_file_path, 'rb') as file:
            s3.upload_fileobj(file, bucket_name, s3_key)
            print(f"File {local_file_path} uploaded to {bucket_name}/{s3_key}.")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

# List of file names you want to upload
files_to_upload = os.listdir('Predictions/Predictions/')

for file_name in files_to_upload:
    local_file_path = os.path.join(local_folder_path, file_name)
    s3_key = file_name
    upload_to_s3(local_file_path, bucket_name, s3_key)

events_data_upload = "Dataset/events_data/"
events_filename = ["events_distances.csv", "Fakbars.csv", "mic_locations.xlsx"]

for file_name in events_filename:
    local_file_path = os.path.join(events_data_upload, file_name)
    s3_key = file_name
    upload_to_s3(local_file_path, bucket_name, s3_key)

upload_to_s3("Dataset/weather_data/weather_data.csv", bucket_name, "weather_data.csv")
