import pandas as pd 
import os
from geopy.geocoders import Nominatim

os.chdir("C:/Users/katri/Documents/Python_scripts/MDA_project/Modern-Data-Analytics-Backend/event_datasets")
# TODO: weights
# combine date and time to one variable
# + merge noise and events
# + distances

# Initialize Nominatim API
import pandas as pd 
import os
import numpy as np
from geopy.geocoders import Nominatim

os.chdir("C:/Users/katri/Documents/Python_scripts/MDA_project/Modern-Data-Analytics-Backend/event_datasets")
#dataframe with locations
Events_full = pd.read_excel("Events_data_full.xlsx")
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