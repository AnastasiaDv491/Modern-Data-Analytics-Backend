import pandas as pd 
import os
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import lonlat, distance

# os.chdir("C:/Users/katri/Documents/Python_scripts/MDA_project/Modern-Data-Analytics-Backend/Dataset/events_data")
# TODO: weights
# combine date and time to one variable
# + merge noise and events
# + distances

# TODO: fix the code so i doesnt create double columns Lat Long
os.chdir("./Dataset/events_data/")
#dataframe with locations
Events_full = pd.read_excel("Events_data_full.xlsx")
# print(Events_full)
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
    Locations_df.at[index, 'Long'] = longitude
    Locations_df.at[index, 'Lat'] = latitude

#merge with original dataset
Events_full = Events_full.merge(Locations_df, on='Address', how='left')
Events_full.to_excel("Events_data_full.xlsx", index=False)  

# Creating distances dataset
Events_full = pd.read_excel("Events_data_full.xlsx")
microphones = pd.read_excel("C:/Users/nastj/OneDrive - KU Leuven/Desktop/MDA project/mic_locations.xlsx")

def dist(lat1, lon1, lat2, lon2):
    
    loc1 = (lat1, lon1)
    loc2 = (lat2, lon2)
    distance_km = distance(lonlat(*loc1), lonlat(*loc2)).km
    
    return distance_km

Events_full['Dist_filosofia'] = 0
Events_full['Dist_xior'] = 0
Events_full['Dist_calvariekapel'] = 0
Events_full['Dist_hears'] = 0
Events_full['Dist_81'] = 0
Events_full['Dist_maxim'] = 0
Events_full['Dist_taste'] = 0
Events_full['Dist_vrijthof'] = 0

distances = []

j = 14 
i = 0
c = 0

for index, row in microphones.iterrows():
    
    lati1 = row['Lat']
    long1 =row['Long']
    print("75",lati1, long1)
    for index, row in Events_full.iterrows():
         lati2 = row['Lat']
         long2 = row['Long']
         print("79",lati2, long2)
         print(pd.isna(lati2))
         if (pd.isna(lati2 or pd.isna(long2))) == True:
             d = "na"
             Events_full.iloc[i,j] = d
             distances.append(d)
             i += 1
         else:
            print("87",lati1, long1,lati2, long2)

            d = dist(lati1, long1, lati2, long2)
            Events_full.iloc[i,j] = d
            distances.append(d)
            i += 1
    j += 1
    c += 1
    if c > 0:
        i = 0
 
print(Events_full.head)

Events_full.to_excel('events_distances.xlsx')