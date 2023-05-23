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

random intercept night_hour night_hour_sq/ subject=Date type=un; 
ods output solutionf = fixed_out; 
run; 

"""
#create directory if necessary
path = "./Predictions/Estimates/"
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
            fixed_df.to_csv(f"Predictions/Estimates/estimates_{filename}")
            
#close sas connection
sas.endsas

def Predictions(est, df):
    y_pred = (
        est[0] + est[1] *df["night_hour"] + est[2] *df["night_hour_sq"] + est[3] *df["night_hour_cu"]
        + (est[96] + est[97] *df["night_hour"] + est[98] *df["night_hour_sq"] + est[99] *df["night_hour_cu"]) *df["LC_HUMIDITY"]
        + (est[100] + est[101] *df["night_hour"] + est[102] *df["night_hour_sq"] + est[103] *df["night_hour_cu"]) *df["LC_DWPTEMP"]
        + (est[104] + est[105] *df["night_hour"] + est[106] *df["night_hour_sq"] + est[107] *df["night_hour_cu"]) *df["LC_WINDSPEED"]
        + (est[108] + est[109] *df["night_hour"] + est[110] *df["night_hour_sq"] + est[111] *df["night_hour_cu"]) *df["Total_Event_Score"]
        )
    
    for index, row in df.iterrows():
        if row["weekday"] == "Wednesday":
            if row["downseason"] == 1:
                y_pred[index] = y_pred[index] 
            else:
                y_pred[index] = (y_pred[index] + est[4] + est[6]*row["night_hour"] + est[8]*row["night_hour_sq"] + est[10]*row["night_hour_cu"])
    
        elif row["weekday"] == "Friday":
            y_pred[index] = (y_pred[index] + est[12] + est[19]*row["night_hour"] + est[26]*row["night_hour_sq"] + est[33]*row["night_hour_cu"])
            if row["downseason"] == 1:
                y_pred[index] = y_pred[index] 
            else:
                y_pred[index] = (y_pred[index] + est[4] + est[6]*row["night_hour"] + est[8]*row["night_hour_sq"] + est[10]*row["night_hour_cu"]
                      + est[40] + est[54]*row["night_hour"] + est[68]*row["night_hour_sq"] + est[82]*row["night_hour_cu"])
        
        elif row["weekday"] == "Monday":
            y_pred[index] = (y_pred[index] + est[13] + est[20]*row["night_hour"] + est[27]*row["night_hour_sq"] + est[34]*row["night_hour_cu"])
            if row["downseason"] == 1:
                y_pred[index] = y_pred[index] 
            else:
                y_pred[index] = (y_pred[index] + est[4] + est[6]*row["night_hour"] + est[8]*row["night_hour_sq"] + est[10]*row["night_hour_cu"]
                      + est[42] + est[56]*row["night_hour"] + est[70]*row["night_hour_sq"] + est[84]*row["night_hour_cu"])
    
        elif row["weekday"] == "Saturday":    
            y_pred[index] = (y_pred[index] + est[14] + est[21]*row["night_hour"] + est[28]*row["night_hour_sq"] + est[35]*row["night_hour_cu"])
            if row["downseason"] == 1:
                y_pred[index] = y_pred[index] 
            else:
                y_pred[index] = (y_pred[index] + est[4] + est[6]*row["night_hour"] + est[8]*row["night_hour_sq"] + est[10]*row["night_hour_cu"]
                      + est[44] + est[58]*row["night_hour"] + est[72]*row["night_hour_sq"] + est[86]*row["night_hour_cu"])
    
        elif row["weekday"] == "Sunday":
            y_pred[index] = (y_pred[index] + est[15] + est[22]*row["night_hour"] + est[29]*row["night_hour_sq"] + est[36]*row["night_hour_cu"])
            if row["downseason"] == 1:
                y_pred[index] = y_pred[index] 
            else:
                y_pred[index] = (y_pred[index] + est[4] + est[6]*row["night_hour"] + est[8]*row["night_hour_sq"] + est[10]*row["night_hour_cu"]
                      + est[46] + est[60]*row["night_hour"] + est[74]*row["night_hour_sq"] + est[88]*row["night_hour_cu"])
    
        elif row["weekday"] == "Thursday":
            y_pred[index] = (y_pred[index] + est[16] + est[23]*row["night_hour"] + est[30]*row["night_hour_sq"] + est[37]*row["night_hour_cu"])
            if row["downseason"] == 1:
                y_pred[index] = y_pred[index] 
            else:
                y_pred[index] = (y_pred[index] + est[4] + est[6]*row["night_hour"] + est[8]*row["night_hour_sq"] + est[10]*row["night_hour_cu"]
                      + est[48] + est[62]*row["night_hour"] + est[76]*row["night_hour_sq"] + est[90]*row["night_hour_cu"])
        
        elif row["weekday"] == "Tuesday":
            y_pred[index] = (y_pred[index] + est[17] + est[24]*row["night_hour"] + est[31]*row["night_hour_sq"] + est[38]*row["night_hour_cu"])
            if row["downseason"] == 1:
                y_pred[index] = y_pred[index] 
            else:
                y_pred[index] = (y_pred[index] + est[4] + est[6]*row["night_hour"] + est[8]*row["night_hour_sq"] + est[10]*row["night_hour_cu"]
                      + est[50] + est[64]*row["night_hour"] + est[78]*row["night_hour_sq"] + est[92]*row["night_hour_cu"])
    
    return y_pred



if os.path.isdir("Predictions/Predictions/") == False:
    os.mkdir("Predictions/Predictions/")

#Delete test_night_file if still exists
if os.path.isfile("Dataset/test/test_night_hears.csv"):
    os.remove("Dataset/test/test_night_hears.csv")
    
Pred = os.listdir("Predictions/Estimates/")
Test = os.listdir("Dataset/test/")

# Iterate over the corresponding pairs of files
for pred_file, test_file in zip(Pred, Test):
    print("Working on " + test_file)
    csv_pred = os.path.join("Predictions/Estimates/", pred_file)
    csv_test = os.path.join("Dataset/test/", test_file)
        
    estimates = pd.read_csv(csv_pred) 
    est = estimates["Estimate"]
    df = pd.read_csv(csv_test)
    y_pred = Predictions(est, df)
        
    # Assign a name to y_pred Series
    y_pred.name = "y_pred"
    # Merge DataFrame with y_pred based on index
    df_y_pred = pd.merge(df, y_pred, left_index=True, right_index=True)
    
    # Save the merged DataFrame to a new file
    output_file = f"Predictions/Predictions/y_pred_{test_file}"
    df_y_pred.to_csv(output_file)
    print("Saved merged predictions to " + output_file)
