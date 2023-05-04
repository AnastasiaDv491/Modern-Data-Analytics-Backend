import fitz  # PyMuPDF module
import pandas as pd

# Open het PDF-bestand
with fitz.open("/Users/charlotte/Desktop/2680_BRO_OPKOT_23-24_definitief.pdf") as doc:
    # Krijg het paginobject voor pagina 60
    page = doc[59]

    # Haal de tekst van de pagina op
    text = page.get_text()

# Split de tekst op de regelovergangen
lines = text.split('•')

# Maak een lijst van lijsten met elke rij in de dataframe
data = [line.split('\n') for line in lines]

# Maak een pandas dataframe van de lijst van lijsten
df = pd.DataFrame(data)

# Verhoog het maximum aantal rijen en kolommen dat wordt weergegeven
pd.options.display.max_rows = 100
pd.options.display.max_columns = 10

# Verwijder de eerste 5 rijen (dit zijn geen residenties)
df = df.iloc[6:]
df = df.reset_index(drop=True)

# Selecteer rijen 14, 45, 47, 54, 55
#df_select = df.iloc[[14, 45, 47, 54, 55]]

# Bekijk de resulterende dataframe
#print(df_select)

# CORRECTION OF ROW 14
df.iloc[14, 3] = df.iloc[14, 0]   # verplaats inhoud van kolom 1 naar kolom 3
df.iloc[14, 0] = df.iloc[14, 0].split(',')[0]   # verwijder alles vanaf ',' in kolom 1

# CORRECTION OF ROW 45
new_rows = [
    [df.iloc[45, 0], "", "", df.iloc[45, 3].split(',')[0], "", "", ""],
    [df.iloc[45, 0], "", "", df.iloc[45, 3].split(',')[1], "", "", ""],
]

# Vervang rij 45 door de twee nieuwe rijen
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

# Bekijk de resulterende dataframe
#print(df)

# Zoek rijen met dezelfde waarde in de vierde kolom
#duplicates = df[df.duplicated(subset=[3], keep=False)].index.tolist()
#print(duplicates)

# Selecteer alleen kolom 0 en 3 met behulp van de methode 'loc'
df = df.loc[:, [0, 3]]

# Geef de kolomnamen op
df.columns = ['Name', 'Addresse']

# Bekijk de resulterende dataframe
print(df)



# TO DO: DUBBELE ADRESSEN + LETTERS BIJ HUISNUMMERS DELETEN WANT GEEFT ERROR BIJ COORDINATEN + KOLOM MET GROEP TOEVOEGEN


##################################################

from geopy.geocoders import Nominatim
import pandas as pd

# Initialiseer de Nominatim API
geolocator = Nominatim(user_agent="StudentRooms")

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
df.to_csv("/Users/charlotte/Desktop/MDA/Data/StudentRooms.csv", index=False)
