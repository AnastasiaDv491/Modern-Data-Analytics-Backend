import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.opcafegaan.be/leuven/category/fakbar'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')


fakbar_list = []
fakbars = soup.find_all('div', class_= 'mt-n2 flex-grow-1')
for fakbar in fakbars:
    #name = fakbar.find_all('h2', class_='h6 mb-0')[0].text.strip()
    name = fakbar.h2.text.strip()
    #address = fakbar.find_all('div', class_='c-icon-label align-middle d-flex font-size-sm mb-2')[0].find_all('p', class_='m-0')[0].text.strip().replace('\n', '')
    address = fakbar.find_all('div')[0].p.text.strip().replace('\n', '')
    #print(name)
    #print(address)
    fakbar_list.append([name, address])

df = pd.DataFrame(fakbar_list, columns=['Name', 'Address'])
print(df)


##################################################

from geopy.geocoders import Nominatim
import pandas as pd

# Initialiseer de Nominatim API
geolocator = Nominatim(user_agent="Fakbars")

# Functie om longitudinale en latitudinale gegevens op te halen voor een adres
def get_lat_long(address):
    location = geolocator.geocode(address)
    if location is None:
        return None, None
    return location.longitude, location.latitude

# Voeg de longitudinale en latitudinale kolommen toe aan de dataset
df['Longitude'] = ""
df['Latitude'] = ""

# Loop door de dataset en vul de longitudinale en latitudinale kolommen in
for index, row in df.iterrows():
    address = row[1]
    longitude, latitude = get_lat_long(address)
    df.at[index, 'Longitude'] = longitude
    df.at[index, 'Latitude'] = latitude

# Sla de dataset op naar een nieuw CSV-bestand
df.to_csv("/Users/charlotte/Desktop/MDA/Data/Fakbars.csv", index=False)