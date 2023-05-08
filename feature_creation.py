import pandas as pd
import os
from geopy.geocoders import Nominatim
import pandas as pd
from datetime import datetime

# Time regrouping
# Noise.py

def TimeBasedRegrouping(parquet):
    df = pd.read_parquet(parquet)

    df = df.loc[(df['result_timestamp'].dt.hour <= 7) | (df['result_timestamp'].dt.hour >= 19)]
    df.loc[:, 'night_scale'] = (df['result_timestamp'] - pd.Timedelta(hours=8)).dt.strftime('%d-%m-%Y %H:%M')
    df['night_scale'] = pd.to_datetime(df['night_scale'])
    #night from monday to tuesday counted as monday
    df.loc[:, 'night_hour'] = (df['night_scale'].dt.hour + df['night_scale'].dt.minute/60) - 11
    df.loc[:, 'night'] = df['night_scale'].dt.strftime('%d-%m-%Y')

    return df

# Noise.py
# loop over parquet files & create dataframes. Store them in a list
collection_dfs = []
directory = "Dataset/"
for filename in os.listdir(directory):
    df_parquet = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(df_parquet):
        df = TimeBasedRegrouping(df_parquet)
        collection_dfs.append(df)

# Create Holidays and Days of the week
def createHolidaysDaysoftheWeek(df):
    df["weekday"] = df['night_scale'].dt.day_name()
    holiday = ["01-01-2022", "18-04-2022", "16-05-2022", "21-07-2022", "25-08-2022", "01-11-2022", "02-11-2022","11-11-2022", "25-12-2022"]
    is_holiday = df['night'].isin(holiday)
   
    df['Holiday']=is_holiday.map({True: 1, False:0})
    down_season = [
        (datetime.strptime("2021-12-31 00:00:00", '%Y-%m-%d %H:%M:%S'), datetime.strptime("2022-02-13 00:00:00", '%Y-%m-%d %H:%M:%S')),
        (datetime.strptime("2022-04-02 00:00:00", '%Y-%m-%d %H:%M:%S'), datetime.strptime("2022-04-19 00:00:00", '%Y-%m-%d %H:%M:%S')),
        (datetime.strptime("2022-05-28 00:00:00", '%Y-%m-%d %H:%M:%S'), datetime.strptime("2022-09-26 00:00:00", '%Y-%m-%d %H:%M:%S')),
        (datetime.strptime("2022-12-24 00:00:00", '%Y-%m-%d %H:%M:%S'), datetime.strptime("2023-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')),
    ]
    is_downseason = False
    for start_date, end_date in down_season:
        is_downseason = is_downseason | ((df['night_scale'] >= start_date) & (df['night_scale'] <= end_date))
    df['downseason'] = is_downseason.astype(int)
    df['night_hour_sq'] = df['night_hour']**2
    df['night_hour_cu'] = df['night_hour']**3
    return df

for df in collection_dfs:
    createHolidaysDaysoftheWeek(df)

# Helper function: Latitude and Longitude

# Initialize Nominatim API
geolocator = Nominatim(user_agent="Mozilla/5.0")

# Get Lat and Long based on the address
def get_lat_long(address):
    location = geolocator.geocode(address)
    if location is None:
        return None, None
    return location.longitude, location.latitude

# For now, it is only reading STUK dataframe, but this can be expanded for multiple events dataframes
def createLatLongCols(df):
    df = pd.read_csv(df)
    df['Longitude'] = ""
    df['Latitude'] = ""
    # Loop door de dataset en vul de longitudinale en latitudinale kolommen in
    for index, row in df.iterrows():
        address = row[1]
        longitude, latitude = get_lat_long(address)
        df.at[index, 'Longitude'] = longitude
        df.at[index, 'Latitude'] = latitude
    
    return df

createLatLongCols("event_datasets/df_stuk_events.csv")