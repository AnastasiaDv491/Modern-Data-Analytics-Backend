# Modern-Data-Analytics-Backend ⚙️
<img src ="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Police_of_Belgium_insignia.svg/1200px-Police_of_Belgium_insignia.svg.png" width="200" height="200" />

feature_creation.py:
- def createLatLongCols(df)
- def get_lat_long(address)
- def createHolidaysDaysoftheWeek(df)
- def TimeBasedRegrouping(parquet)


# Modelling
Given the longitudinal nature of the data and the high variablility between days, a mixed model is used to analyse the influence of the different created covariates. The data is clustered per night. i.e. from 19u00 to 07u00 the next morning. 
SAS® softeware is used to run the actual model as it is one of the best softeware packages for handeling mixed models. 

# Additional installations
## Saspy 
For the modelling part, SAS® softeware is used to run the mixed models. A connection with python can be made through the packages Saspy. For the specific configurations required for your operating system and the type of SAS softeware access, please consult the saspy manual: https://sassoftware.github.io/saspy/.
Please note that a SAS account is required to access SAS® softeware.

Depending on your configurations the following dependencies apply:
- Python3.4 or higher
- SAS 9.4 or higher SAS Viya 3.1 or higher
- To use the integrated object method (IOM) access method, Java 7 or higher is required on the client.

For access to the SAS OnDemand Hosted Servers three additional jar files should be stored in the saspy/java/iomclient directory of the SASPy installation in your Python environment. The jar files can be downloaded from this link: https://support.sas.com/downloads/package.htm?pid=2494

# File structure
To get the raw data into `parquet` files, you have to run `data_fetching.py` 
The repository exists of the following .py files:
1. `events.py` 
- creation of events_distance and event_weights
2. `weather.py` 
- select variables and reduce to 20 min scale
3. `noise.py` 
- select night hours only
- merge with events and weather data 
- test/train split
- creation of additional variables        
4. `Mixed models.py`
- running model on train set
- create predicitons for test set
5.
6.

The files should be run in this order to respect the dependencies between the files.

## AWS
The final files are pushed to AWS S3 storage. This is done via  `datapush_AWS.py` file. You will need your access keys and S3 bucket to push the files to AWS. The following files/folders have to be pushed to the front-end repository to run:
- Predictions/
- events_data/
- events_distances.csv, Fakbars.csv, mic_locations.xlsx
- weather_data.csv
