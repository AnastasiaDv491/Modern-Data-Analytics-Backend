# Modern-Data-Analytics-Backend

feature_creation.py:
- def createLatLongCols(df)
- def get_lat_long(address)
- def createHolidaysDaysoftheWeek(df)
- def TimeBasedRegrouping(parquet)


# Modelling
Given the longitudinal nature of the data and the high variablility between days, a mixed model is used to analyse the influence of the different created covariates. The data is clustered per night. i.e. from 19u00 to 07u00 the next morning. 
SAS® softeware is used to run the actual model as it is one of the best softeware packages for handeling mixed models. 

## Saspy 
The package Saspy is used to make the connection between python and the SAS softeware. For the specific configurations required for your operating system and the type of SAS softeware access, please consult the saspy manual: https://sassoftware.github.io/saspy/.
Please note that a SAS account is required.

Depending on your configurations the following dependencies apply:
- Python3.4 or higher
- SAS 9.4 or higher SAS Viya 3.1 or higher
- To use the integrated object method (IOM) access method, Java 7 or higher is required on the client.

For access to the SAS OnDemand Hosted Servers three additional jar files should be stored in the saspy/java/iomclient directory of the SASPy installation in your Python environment. The jar files can be downloaded from this link: https://support.sas.com/downloads/package.htm?pid=2494
