from cProfile import label
from turtle import goto
import pandas as pd
from geopy.distance import lonlat, distance
import os

os.chdir("C:/Users/jirka/Documents/MDA/events/event_datasets")

events = pd.read_excel("Events_data_full.xlsx")
microphones = pd.read_excel("mic_locations.xlsx")
print(events.head)
print(microphones.head)

def dist(lat1, lon1, lat2, lon2):
    
    loc1 = (lat1, lon1)
    loc2 = (lat2, lon2)
    distance_km = distance(lonlat(*loc1), lonlat(*loc2)).km
    
    return distance_km

events['Dist_filosofia'] = 0
events['Dist_xior'] = 0
events['Dist_calvariekapel'] = 0
events['Dist_hears'] = 0
events['Dist_81'] = 0
events['Dist_maxim'] = 0
events['Dist_taste'] = 0
events['Dist_vrijthof'] = 0

distances = []

j = 14 
i = 0
c = 0

for index, row in microphones.iterrows():
    lati1 = row['Lat']
    long1 =row['Long']
    for index, row in events.iterrows():
         lati2 = row['Lat']
         long2 = row['Long']
         if (lati2 or long2) == "na":
             d = "na"
             events.iloc[i,j] = d
             distances.append(d)
             i += 1
         else:
            d = dist(lati1, long1, lati2, long2)
            events.iloc[i,j] = d
            distances.append(d)
            i += 1
    j += 1
    c += 1
    if c > 0:
        i = 0
 
print(events.head)

events.to_excel('events_distances.xlsx')