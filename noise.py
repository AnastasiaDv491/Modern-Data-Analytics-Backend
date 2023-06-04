import pandas as pd
import os
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
    df.loc[:, 'Date'] = df['night_scale'].dt.strftime('%d-%m-%Y')

    return df

# Noise.py
# loop over parquet files & create dataframes. Store them in a list
collection_dfs = []
directory = "Dataset/parquet/"
for filename in os.listdir(directory):
    df_parquet = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(df_parquet):
        df = TimeBasedRegrouping(df_parquet)
        collection_dfs.append(df)


night_81 = collection_dfs[0]
night_calverie = collection_dfs[1]
night_filosovia = collection_dfs[2]
night_hears = collection_dfs[3]
night_maxim = collection_dfs[4]
night_taste = collection_dfs[5]
night_vrijthof = collection_dfs[6]
night_xior = collection_dfs[7]
night_collection = [night_81, night_calverie, night_filosovia, night_hears, night_maxim, night_taste, night_vrijthof, night_xior]


def mergeEventsNoiseWeather(noise_df, dist_column, output_name):
     # use the dataframes from the collection "night_collection" to merge 
    df_events_dist = pd.read_csv("Dataset/events_data/events_distances.csv")
    
    df = pd.merge(noise_df,df_events_dist[['Date', "Event_name", "Address","Event_type", "Weight_Event_Type","Organizer","Respondents",dist_column]],on='Date', how='outer')
    df.rename(columns={dist_column: 'Distance'}, inplace=True)
    #weather
    weather_data = pd.read_csv("Dataset/weather_data/weather_data.csv")
    weather_data["DATEUTC"] = weather_data["DATEUTC"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    df = pd.merge(df, weather_data, how='left', left_on="result_timestamp", right_on="DATEUTC")

    path = "./Dataset/merged_dataset/"
    # check if the directory exists; if not create it
    if os.path.isdir(path) == False:
        os.mkdir(path)

         # check if the file with output_name already exists
    output_path = os.path.join(path, f"{output_name}.csv")
    if os.path.isfile(output_path):
        print(f"File {output_path} already exists. Skipping CSV export.")
    else:
        df.to_csv(output_path)
        print(f"Exported merged dataframe to {output_path}.")

    return df

mergeEventsNoiseWeather(night_81, "Dist_81", "night_81_merged")
mergeEventsNoiseWeather(night_calverie, "Dist_calvariekapel", "night_calverie_merged")
mergeEventsNoiseWeather(night_filosovia, "Dist_filosofia", "night_filosovia_merged")
mergeEventsNoiseWeather(night_hears, "Dist_hears", "night_hears_merged")
mergeEventsNoiseWeather(night_maxim, "Dist_maxim", "night_maxim_merged")
mergeEventsNoiseWeather(night_taste, "Dist_taste", "night_taste_merged")
mergeEventsNoiseWeather(night_vrijthof, "Dist_vrijthof", "night_vrijthof_merged")
mergeEventsNoiseWeather(night_xior, "Dist_xior", "night_xior_merged")

def createTestTrainData(df_to_split,output_name):
    path = "Dataset/merged_dataset/"
    df_to_split= pd.read_csv(os.path.join(path, f"{df_to_split}_merged.csv"))
    df_to_split["result_timestamp"] = pd.to_datetime(df_to_split["result_timestamp"])
    train = df_to_split[df_to_split.result_timestamp.dt.month.isin(range(1,7))]
    test = df_to_split[df_to_split.result_timestamp.dt.month.isin(range(7, 13))]

    # store datasets in their folders
    paths = ["./Dataset/train/","./Dataset/test/" ]

    if os.path.isdir(paths[0]) == False:
        os.mkdir(paths[0])
    if os.path.isdir(paths[1]) == False:
        os.mkdir(paths[1])

    for dataset in paths:
        for filename in os.listdir(dataset):
            full_df = os.path.join(dataset, filename)
            if os.path.isfile(full_df):
                pass
            else:
                df.to_csv(dataset + f"{output_name}.csv")
    # save the train and test file
    train.to_csv(paths[0] + f"train_{output_name}.csv", index=False)
    test.to_csv(paths[1]+f"test_{output_name}.csv", index=False)

    return print("The data was split")

createTestTrainData("night_81", "night_81")
createTestTrainData('night_calverie', "night_calverie")
createTestTrainData("night_filosovia", "night_filosovia")
createTestTrainData("night_hears", "night_hears")
createTestTrainData("night_maxim", "night_maxim")
createTestTrainData("night_taste", "night_taste")
createTestTrainData("night_vrijthof", "night_vrijthof")
createTestTrainData("night_xior", "night_xior")


#########################################
# Train data manipulations
#########################################

# Create Holidays and Days of the week
def createHolidaysDaysoftheWeek(df):
    df['night_scale'] = pd.to_datetime(df['night_scale'], errors='coerce')
    df["weekday"] = df['night_scale'].dt.day_name()
    holiday = ["01-01-2022", "18-04-2022", "16-05-2022", "21-07-2022", "25-08-2022", "01-11-2022", "02-11-2022","11-11-2022", "25-12-2022"]
    is_holiday = df['Date'].isin(holiday)

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

    return print("Successfully created new dates")

def weight_respondents(df):
    df["Weight_respondent"] = ""
    quantiles = df.groupby("Organizer")["Respondents"].quantile([0.33, 0.66]).reset_index()
    quantiles = quantiles.set_index(['Organizer', 'level_1'])['Respondents'].unstack()
    quantiles = quantiles.reset_index()

    for organizer in ["Ambiorix", "City of Leuven", "Crimen", "Ekonomika", "HDR", "LOKO", "Politica", "Recup", "Rumba", "Stuk", "VRG", "t Archief"]:
        mask = df["Organizer"] == organizer
        quantile_33 = quantiles.loc[quantiles["Organizer"] == organizer, 0.33]
        quantile_66 = quantiles.loc[quantiles["Organizer"] == organizer, 0.66]
        if quantile_33.empty or quantile_66.empty:
            continue
        quantile_33 = quantile_33.values[0]
        quantile_66 = quantile_66.values[0]
        df.loc[mask & (df["Respondents"] <= quantile_33), "Weight_respondent"] = 1
        df.loc[mask & (df["Respondents"] >= quantile_66), "Weight_respondent"] = 3
        df.loc[mask & (df["Respondents"] > quantile_33) & (df["Respondents"] < quantile_66), "Weight_respondent"] = 2

    df.loc[df["Event_type"] == "Kermis", "Weight_respondent"] = 4
    df.loc[df["Event_name"] == "Kerstmis", "Weight_respondent"] = 2

    print("Successfully weight_respondents creation")
    return df


def Total_Event_Score(df):
    df["Event_Score"] = df["Weight_Event_Type"]*df["Weight_respondent"]/df["Distance"]
    df["Event_Score"] = pd.to_numeric(df["Event_Score"], errors='coerce').fillna(0)
    Total_Event_Scores= df.groupby(["result_timestamp"])["Event_Score"].sum().reset_index()
    print(Total_Event_Scores)
    df = pd.merge(df, Total_Event_Scores, on="result_timestamp", how="left")
    df.rename(columns={"Event_Score_y": "Total_Event_Score"}, inplace=True)

    print("Total event score created")
    return df

for filename in os.listdir("./Dataset/train/"):
    if filename == 'train_night_hears.csv':
        print('hears dataset = skip')
    else:
        print("Working on" +filename)
        csv_train = os.path.join("Dataset/train/", filename)
        # checking if it is a file
        if os.path.isfile(csv_train):
            df_train = pd.read_csv(csv_train) 
            createHolidaysDaysoftheWeek(df_train)
            weight_respondents(df_train)
            score = Total_Event_Score(df_train)
            score_remove_dup=score.drop_duplicates(subset=["night_scale"])
            score_remove_dup.to_csv(csv_train)

#########################################
# Test data manipulations
#########################################

# Create Holidays and Days of the week

for filename in os.listdir("./Dataset/test/"):
    print("Working on" +filename)
    csv_test = os.path.join("Dataset/test/", filename)
    # checking if it is a file
    if os.path.isfile(csv_test):
        df_test= pd.read_csv(csv_test) 
        createHolidaysDaysoftheWeek(df_test)
        weight_respondents(df_test)
        score = Total_Event_Score(df_test)
        score.to_csv(csv_test)

