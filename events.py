import pandas as pd 
import os
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import distance

os.chdir("./Dataset/events_data/")
#dataframe with locations
Events_full = pd.read_excel("Events_data_full_KADI.xlsx")

addresses = np.unique(Events_full["Address"])
Locations_df = pd.DataFrame({'Address': addresses})

# get coordinates
geolocator = Nominatim(user_agent="Mozilla/5.0.")

def get_lat_long(address):
    location = geolocator.geocode(address)
    if location is None:
        return None, None
    return location.longitude, location.latitude


for index, row in Locations_df.iterrows():
    longitude, latitude = get_lat_long(row["Address"])
    Locations_df.loc[index, 'Long'] = longitude
    Locations_df.loc[index, 'Lat'] = latitude

#merge with original dataset
Events_full = Events_full.merge(Locations_df, on='Address', how='left') 

# Creating distances dataset
microphones = pd.read_excel("mic_locations.xlsx")

def dist(lat1, lon1, lat2, lon2):
    
    loc1 = (lat1, lon1)
    loc2 = (lat2, lon2)
    distance_km = distance(loc1, loc2).km
    
    return distance_km

Events_full['Dist_filosofia'] = 0
Events_full['Dist_xior'] = 0
Events_full['Dist_calvariekapel'] = 0
Events_full['Dist_hears'] = 0
Events_full['Dist_81'] = 0
Events_full['Dist_maxim'] = 0
Events_full['Dist_taste'] = 0
Events_full['Dist_vrijthof'] = 0

j = 14 
i = 0

for index, row in microphones.iterrows():
    lati1 = row['Lat']
    long1 =row['Long']
    for index, row in Events_full.iterrows():
        lati2 = row['Lat']
        long2 = row['Long']
        if (pd.isna(lati2) or pd.isna(long2)) == True:   
            d = "nan"
            Events_full.iloc[i,j] = d
            i += 1
        else:
            d = dist(lati1, long1, lati2, long2)
            Events_full.iloc[i,j] = d
            i += 1
    j += 1      # next column                 
    i = 0   # when events are done recet rows to zero
 

# weights for event type
def weight_event(event_type):
    if event_type == "Cantus":
        return 4   
    elif event_type == "Kermis":
        return 5
    elif event_type == "Other":
        return 1
    elif event_type == "Party":
        return 2
    else:
        return 3
Events_full['Weight_Event_Type'] = Events_full['Event_type'].apply(weight_event)

# combined weights per event --> after split
# sum all events per day --> after split
Events_full.to_csv('events_distances.csv')