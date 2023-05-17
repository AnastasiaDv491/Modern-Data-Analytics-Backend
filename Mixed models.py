import pandas as pd
import os
import saspy

# starting sas session
sas = saspy.SASsession(
# own pathway to your Java 7 or 8 file on
java='C:\\Program Files (x86)\\Java\\jre-1.8\\bin\\java.exe',
#European Home Region 1
iomhost=['odaws01-euw1.oda.sas.com','odaws02-euw1.oda.sas.com'],
iomport= 8591,
authkey= 'oda',
encoding ='utf-8')
sas

#sas code to run
mixed_model_code = """ 
proc mixed data=df_sas;
class Date weekday Organizer downseason;
model laeq=night_hour  night_hour_sq night_hour_cu 
downseason night_hour*downseason night_hour_sq*downseason night_hour_cu*downseason 
weekday night_hour*weekday night_hour_sq*weekday night_hour_cu*weekday
downseason*weekday night_hour*downseason*weekday night_hour_sq*downseason*weekday night_hour_cu*downseason*weekday

LC_HUMIDITY night_hour*LC_HUMIDITY night_hour_sq*LC_HUMIDITY night_hour_cu*LC_HUMIDITY
LC_DWPTEMP night_hour*LC_DWPTEMP night_hour_sq*LC_DWPTEMP night_hour_cu*LC_DWPTEMP
LC_WINDSPEED night_hour*LC_WINDSPEED night_hour_sq*LC_WINDSPEED night_hour_cu*LC_WINDSPEED
	
Total_Event_Score night_hour*Total_Event_Score night_hour_sq*Total_Event_Score night_hour_cu*Total_Event_Score
/ solution;

random intercept night_hour night_hour_sq night_hour_cu/ subject=Date type=un; 
ods output solutionf = fixed_out; 
run; 

"""
#create directory if necessary
path = "./Predictions/"
    # check if the directory exists; if not create it
if os.path.isdir(path) == False:
    os.mkdir(path)

#loop over all training files
for filename in os.listdir("./Dataset/train/"):
    if filename == 'train_night_hears.csv':
        print('Skipping hears dataset')
    else:
        print("Working on" +filename)
        csv_train = os.path.join("Dataset/train/", filename)
        # checking if it is a file
        if os.path.isfile(csv_train):
            df = pd.read_csv(csv_train)
            # create sas table named 'df_sas'
            python_object = sas.df2sd(df, 'df_sas', libref='WORK')
            #run the sas code 
            model_out = sas.submit(mixed_model_code)
            print(model_out['LOG'])
            #retrieve solution of fixed effects
            fixed_df = sas.sasdata('fixed_out').to_df()
            fixed_df.to_csv(f"Predictions/^pred_{filename}")
            
#close sas connection
sas.endsas
