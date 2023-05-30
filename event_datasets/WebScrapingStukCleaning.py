import pandas as pd 
import re

df = pd.read_csv('df_stuk.csv')
# get room capacity of Stuk rooms
df_STUK_locations_capacity = pd.read_excel("C:/Users/nastj/OneDrive - KU Leuven/Desktop/MDA project/Project notes/room_capacity_stuk.xlsx")

def cleanDFStuk(df, df_capacity):
    # cleaning the Date column
    df["Date"] = df["Date"].astype('string')
    df["Date"] = df["Date"].apply(lambda x: " ".join(x.split()))
    df["Location"] = df.Location.str.replace("\n", " ")

    # filtering on year 2022
    df = df[df["Date"].str.contains("2022")]
    # creating Day column
    date =[]
    start_time = []
    for i in df['Date']:
    
        # using Regex expressions to find months and days and concatenate them together
        month = re.search("([a-zA-Z]{3})",i)
        day =  re.search("(\d{1,2})",i)
        time = re.search("(\d{1,2}:\d{2})", i)
        # regex return Match object; use .group() to get raw value
        date.append("-".join([day.group(), month.group()]))
        start_time.append(time.group())
    df["Day"] = date
    df["DateTime"] = start_time

    # removing far away & unclear locations
    df = df[(df["Location"] != "Leuven" )|(df["Location"] != "CC Gasthuis Aarschot (start)") ]
    df_capacity.rename(columns = {"Room": "Location"}, inplace = True)

    df_stuk_events = pd.merge(df, df_capacity[["Responded","Location"]],on='Location', how='left')
    df_stuk_events.to_csv("./Dataset/events_data/df_stuk.csv", index = False)
    return df_stuk_events

cleanDFStuk(df, df_STUK_locations_capacity)

