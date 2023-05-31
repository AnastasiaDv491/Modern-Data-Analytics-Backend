import fitz  # PyMuPDF module
import pandas as pd

# Open PDF-file
with fitz.open("/Users/charlotte/Desktop/2680_BRO_OPKOT_23-24_definitief.pdf") as doc:
    # store page 60 in dataobject
    page = doc[59]

    # get the the text from page 60
    text = page.get_text()

# Split the text on lines
lines = text.split('•')

# make list of lists from each row in the dataframe 
data = [line.split('\n') for line in lines]
df = pd.DataFrame(data)


# remove first 5 rows (these are not residencies) 
df = df.iloc[6:]
df = df.reset_index(drop=True)


# CORRECTION OF ROW 14
df.iloc[14, 3] = df.iloc[14, 0]   # move content from columnm 1 to column 4 
df.iloc[14, 0] = df.iloc[14, 0].split(',')[0]   # remove everything after ',' in column 1 

# CORRECTION OF ROW 45
new_rows = [
    [df.iloc[45, 0], "", "", df.iloc[45, 3].split(',')[0], "", "", ""],
    [df.iloc[45, 0], "", "", df.iloc[45, 3].split(',')[1], "", "", ""],
]

# replace row 45 by corrected ones
df.drop(45, inplace=True)
df = df.reset_index(drop=True)
df = pd.concat([df.iloc[:45], pd.DataFrame(new_rows, columns=df.columns), df.iloc[45:]]).reset_index(drop=True)

# CORRECTION OF ROW 48 AND 55
df.iloc[48, 3] = df.iloc[48, 4]
df.iloc[55, 3] = df.iloc[55, 4]

# CORRECTION OF ROW 56
new_rows = [
    [df.iloc[56, 0], "", "", df.iloc[56, 3], "", "", ""],
    [df.iloc[56, 0], "", "", df.iloc[56, 4], "", "", ""],
    [df.iloc[56, 0], "", "", df.iloc[56, 5], "", "", ""]
]
df = df.append(pd.DataFrame(new_rows, columns=df.columns), ignore_index=True)
df = df.drop(index=56)


# select column 1 and 4
df = df.loc[:, [0, 3]]

# give names
df.columns = ['Name', 'Addresse']


##################################################

from geopy.geocoders import Nominatim
import pandas as pd

# Initialise Nominatim API
geolocator = Nominatim(user_agent="StudentRooms")


def get_lat_long(address):
    location = geolocator.geocode(address)
    if location is None:
        return None, None
    return location.longitude, location.latitude

# create new Longitude and Latitude columns
df['Longitude'] = ""
df['Latitude'] = ""

# get the coordinates from each row
for index, row in df.iterrows():
    address = row[1]
    longitude, latitude = get_lat_long(address)
    df.at[index, 'Longitude'] = longitude
    df.at[index, 'Latitude'] = latitude


df.to_csv("/Users/charlotte/Desktop/MDA/Data/StudentRooms.csv", index=False)
