import glob
import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim
from boto.s3.key import Key
import os
from cProfile import label
from turtle import goto
import pandas as pd
from geopy.distance import lonlat, distance
import os


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
    df_name = df

# Only uncomment if you need to change something to the structure of the file
# df_taste = createDataFiles( file_path_end="taste",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_vrijthof = createDataFiles(file_path_end="vrijthof",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_hears= createDataFiles(file_path_end="hears",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_81= createDataFiles(file_path_end="81",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_filosovia= createDataFiles(file_path_end="filosovia",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_maxim =createDataFiles(file_path_end="maxim",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_xior = createDataFiles(file_path_end="xior",path= 'C:/Users/nastj/Downloads/Full Data Set/')
# df_kapel = createDataFiles(file_path_end="calvariekapel-ku-leuven",path= 'C:/Users/nastj/Downloads/Full Data Set/')


