import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL voor de events archive pagina's
#url = 'https://ekonomika.be/events-archive/'
base_url = 'https://ekonomika.be/events-archive/page/'

# Lijsten voor de gegevens van de events
names = []
dates = []
addresses = []

# Loop door de pagina's van 1 tot en met 24
for i in range(1, 25):
    # URL voor de huidige pagina
    url = base_url + str(i) + '/'

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    EventsEkonomika_list = []

    EventsEkonomika = soup.find_all('div', class_= 'post-item__inner')

    for event in EventsEkonomika:
        #name = event.find_all('div', class_='post-item__content post-item__content--has-status')[0].find_all('p', class_='h5 post-item__title')[0].text.strip()
        name = event.find_all('div', class_='post-item__content post-item__content--has-status')[0].p.text.strip()
        #address = event.find_all('div', class_='post-item__meta')[0].find_all('div', class_='post-item__location')[0].text.strip()
        # THE CODE ABOVE DOES NOT WORK BECAUSE EMPTY ARRAY GIVES ERROR
        meta_divs = event.find_all('div', class_='post-item__meta')
        if meta_divs:
            location_divs = meta_divs[0].find_all('div', class_='post-item__location')
            if location_divs:
                address = location_divs[0].text.strip()
            else:
                address = ''
        else:
            address = ''
        date = event.find_all('div', class_='post-item__meta')[0].find_all('div', class_='post-item__time')[0].text.strip()
        #print(name)
        #print(address)
        #print(date)
        names.append(name)
        dates.append(date)
        addresses.append(address)

df = pd.DataFrame({'Name': names, 'Address': addresses, 'Date': dates})

## LOOK AT MULTIPLE PAGES
## CLEAN UP THE DATA
## COORDINATES 

print(df)

##################################################

import pandas as pd

# API key voor Google Maps Geocoding API
API_KEY = 'EventsEkonomika'

# Functie om longitudinale en latitudinale gegevens op te halen voor een adres
def get_lat_long(address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'
    response = requests.get(url).json()
    if response['status'] == 'OK':
        longitude = response['results'][0]['geometry']['location']['lng']
        latitude = response['results'][0]['geometry']['location']['lat']
    else:
        longitude, latitude = None, None
    return longitude, latitude

# Voeg de longitudinale en latitudinale kolommen toe aan de dataset
df['Longitude'] = ""
df['Latitude'] = ""

# Loop door de dataset en vul de longitudinale en latitudinale kolommen in
for index, row in df.iterrows():
    address = row['Address']
    longitude, latitude = get_lat_long(address)
    df.at[index, 'Longitude'] = longitude
    df.at[index, 'Latitude'] = latitude

# Sla de dataset op naar een nieuw CSV-bestand
df.to_csv("/Users/charlotte/Desktop/MDA/Data/EventsEkonomika.csv", index=False)