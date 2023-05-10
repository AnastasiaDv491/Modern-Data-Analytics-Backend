import pandas as pd 
import os
from geopy.geocoders import Nominatim

# TODO:
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
    Locations_df.loc[index, 'Long'] = longitude
    Locations_df.loc[index, 'Lat'] = latitude

#merge with original dataset
Events_full = pd.merge(Events_full, Locations_df[['Address', 'Long', 'Lat']], on='Address', how='left')

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

def weight_respondents(Events_full):
    quantiles = Events_full.groupby("Organizer")["Respondents"].quantile([0.33, 0.66]).reset_index()
    quantiles = quantiles.set_index(['Organizer', 'level_1'])['Respondents'].unstack()
    quantiles = quantiles.reset_index()

    for organizer in ["Ambiorix", "City of Leuven", "Crimen", "Ekonomika", "HDR", "LOKO", "Politica", "Recup", "Rumba", "Stuk", "VRG", "t Archief"]:
        mask = Events_full["Organizer"] == organizer
        quantile_33 = quantiles.loc[quantiles["Organizer"] == organizer, 0.33]
        quantile_66 = quantiles.loc[quantiles["Organizer"] == organizer, 0.66]
        if quantile_33.empty or quantile_66.empty:
            continue
        quantile_33 = quantile_33.values[0]
        quantile_66 = quantile_66.values[0]
        Events_full.loc[mask & (Events_full["Respondents"] <= quantile_33), "Weight_Respondent_type"] = 1
        Events_full.loc[mask & (Events_full["Respondents"] >= quantile_66), "Weight_Respondent_type"] = 3
        Events_full.loc[mask & (Events_full["Respondents"] > quantile_33) & (Events_full["Respondents"] < quantile_66), "Weight_Respondent_type"] = 2

    Events_full.loc[Events_full["Event_type"] == "Kermis", "Weight_Respondent_type"] = 4
    Events_full.loc[Events_full["Event_name"] == "Kerstmis", "Weight_Respondent_type"] = 2

weight_respondents(Events_full)


# combined weights per event
# sum all events per day
Events_full.to_excel("Events_data_full.xlsx", index=False)  