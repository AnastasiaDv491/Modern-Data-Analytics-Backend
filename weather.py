import pandas as pd
import os


def get_df(path):
    df=pd.DataFrame()
    for file in os.listdir(path):
        if file.endswith('.csv'):
            print(path+file)
            aux=pd.read_csv(path+file)
            df = pd.concat([df, aux], ignore_index=True)
    df['DATEUTC'] = pd.to_datetime(df['DATEUTC'],format='%Y-%m-%d %H:%M:%S')
    df = df[["DATEUTC","LC_HUMIDITY", "LC_DWPTEMP", "LC_WINDSPEED"]]
    df = df.resample('20Min', on='DATEUTC').mean()
    df = df.rename(columns={"DATEUTC": "Datetime"})
    df.to_csv("weather_data.csv")
    return df

df = get_df("C:/Users/nastj/Downloads/dataverse_files/")

print(df)