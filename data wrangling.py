import glob
import os
import pandas as pd
from datetime import datetime
import sys
import boto3
import boto.s3
from boto.s3.key import Key

# Read csv files and create parquet files and df 
def createDataFiles( file_path_end, path):
    '''
    Loops over the provided file path ends & retrieves csv files to create parquet files 
    file_path_end: last word before .csv in your csv files
    path: local path to where the data is stored. 
    '''    
    df_list = (pd.read_csv(file, sep = ";")
    for file in glob.glob(path + "/*/*"+f'{file_path_end}'+".csv") )
    df_name = pd.concat(df_list, ignore_index=True)
    df_name = df_name[['result_timestamp','lamax','laeq','lceq','lcpeak']]

    df_name['result_timestamp'] =df_name['result_timestamp'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S.%f'))

    df_name.sort_values(by=['result_timestamp'],inplace=True)
    df_name =df_name.resample('20min',closed = 'right', on='result_timestamp').mean()
    df_name.reset_index(inplace=True)
    df_name.to_parquet(f"Dataset/full_{file_path_end}_df.parquet")
        
    return df_name
    # df_name = df

# Only uncomment if you need to change something to the structure of the file
# df_taste = createDataFiles( file_path_end="taste",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_vrijthof = createDataFiles(file_path_end="vrijthof",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_hears= createDataFiles(file_path_end="hears",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_81= createDataFiles(file_path_end="81",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_filosovia= createDataFiles(file_path_end="filosovia",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_maxim =createDataFiles(file_path_end="maxim",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_xior = createDataFiles(file_path_end="xior",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_kapel = createDataFiles(file_path_end="calvariekapel-ku-leuven",path= 'C:/Users/nastj/Downloads/Full Data Set/')


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