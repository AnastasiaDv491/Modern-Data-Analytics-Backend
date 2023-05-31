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

