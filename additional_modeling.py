import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV

# reading the files
df_81_train = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/train/train_night_81.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
calverie_train = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/train/train_night_calverie.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
filosovia_train = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/train/train_night_filosovia.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
maxim_train = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/train/train_night_maxim.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
taste_train = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/train/train_night_taste.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
vrijthof_train = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/train/train_night_vrijthof.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
xior_train = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/train/train_night_xior.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])

df_81_test = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/test/test_night_81.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
calverie_test = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/test/test_night_calverie.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
filosovia_test = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/test/test_night_filosovia.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
maxim_test = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/test/test_night_maxim.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
taste_test = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/test/test_night_taste.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
vrijthof_test = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/test/test_night_vrijthof.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])
xior_test = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Dataset/test/test_night_xior.csv',
                             usecols=['result_timestamp','laeq','night_scale','night_hour','Date','Event_type',
                                    'Weight_Event_Type','Organizer','Respondents','Distance',
                                    'LC_HUMIDITY','LC_DWPTEMP','LC_WINDSPEED','weekday',
                                    'Holiday','downseason','Weight_respondent','Total_Event_Score'])

# Getting the best paramaters for Random forest
def rf_modeling(df_train, df_test):
   df_train['result_timestamp'] = pd.to_datetime(df_train['result_timestamp'])
   df_train['Hour'] = df_train['result_timestamp'].dt.hour
   df_train['laeq']= df_train['laeq'].interpolate(option='spline')
   df_train = pd.get_dummies(df_train, columns=['weekday'])
   df_train = df_train[['laeq','downseason','LC_HUMIDITY', 'LC_DWPTEMP', 'LC_WINDSPEED','Total_Event_Score', 'Hour','weekday_Friday', 'weekday_Monday',
       'weekday_Saturday', 'weekday_Sunday', 'weekday_Thursday',
       'weekday_Tuesday', 'weekday_Wednesday']]
   
   df_test['result_timestamp'] = pd.to_datetime(df_test['result_timestamp'])
   df_test['Hour'] = df_test['result_timestamp'].dt.hour
   df_test['laeq']= df_test['laeq'].interpolate(option='spline')
   df_test = pd.get_dummies(df_test, columns=['weekday'])
   df_test = df_test[['laeq','downseason','LC_HUMIDITY', 'LC_DWPTEMP', 'LC_WINDSPEED','Total_Event_Score', 'Hour','weekday_Friday', 'weekday_Monday',
       'weekday_Saturday', 'weekday_Sunday', 'weekday_Thursday',
       'weekday_Tuesday', 'weekday_Wednesday']]
   
   x_train = df_train.loc[:, df_train.columns != 'laeq']
   x_test = df_test.loc[:, df_test.columns != 'laeq']

   y_train = df_train['laeq']
   y_test = df_test['laeq']
    

    # the param to tune
   n_estimators = [int(x) for x in np.linspace(start = 10, stop = 1000, num = 10)]
   max_features = ['auto', 'sqrt']
   max_depth = [2,3,5,7,9]
   min_samples_split = [2, 5, 10, 20, 30]
   min_samples_leaf = [1, 2, 4, 8, 16]

   random_grid = {
      # The number of trees in the forest.
      'n_estimators': n_estimators,
      # The maximum depth of the tree
      'max_depth': max_depth,
      # The number of features to consider when looking for the best split
      'max_features': max_features,
      # The minimum number of samples required to split an internal node
      'min_samples_split': min_samples_split,
      # The minimum number of samples required to be at a leaf node
      'min_samples_leaf': min_samples_leaf}
   
   # tune the params
   rf = RandomForestRegressor()
   tuning_model = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=72, cv=5, verbose=1, n_jobs=-1) 
   # n_iter = Number of parameter settings that are sampled
    
   tuning_model.fit(x_train,y_train)
   print(tuning_model.best_params_)

   tuned_hyper_model= RandomForestRegressor(**tuning_model.best_params_)
   tuned_hyper_model.fit(x_train,y_train)
   tuned_pred=tuned_hyper_model.predict(x_test)

   plt.bar(x_train.columns, tuned_hyper_model.feature_importances_)
   plt.xticks(rotation=90)
   plt.show()

   print('R2: %.4f' %r2_score(y_test,tuned_pred))
   print('MSE: %.4f' %mean_squared_error(y_test,tuned_pred))

   print(tuned_pred)
   y_pred_rf = tuned_pred
   return y_pred_rf

# gradient boosting regression
def gbr_model(df_train,df_test):
    df_train['result_timestamp'] = pd.to_datetime(df_train['result_timestamp'])
    df_train['Hour'] = df_train['result_timestamp'].dt.hour
    df_train['laeq']= df_train['laeq'].interpolate(option='spline')
    df_train = pd.get_dummies(df_train, columns=['weekday'])
    df_train = df_train[['laeq','downseason','LC_HUMIDITY', 'LC_DWPTEMP', 'LC_WINDSPEED','Total_Event_Score', 'Hour','weekday_Friday', 'weekday_Monday',
       'weekday_Saturday', 'weekday_Sunday', 'weekday_Thursday',
       'weekday_Tuesday', 'weekday_Wednesday']]
   
    df_test['result_timestamp'] = pd.to_datetime(df_test['result_timestamp'])
    df_test['Hour'] = df_test['result_timestamp'].dt.hour
    df_test['laeq']= df_test['laeq'].interpolate(option='spline')
    df_test = pd.get_dummies(df_test, columns=['weekday'])
    df_test = df_test[['laeq','downseason','LC_HUMIDITY', 'LC_DWPTEMP', 'LC_WINDSPEED','Total_Event_Score', 'Hour','weekday_Friday', 'weekday_Monday',
       'weekday_Saturday', 'weekday_Sunday', 'weekday_Thursday',
       'weekday_Tuesday', 'weekday_Wednesday']]
   
    x_train = df_train.loc[:, df_train.columns != 'laeq']
    x_test = df_test.loc[:, df_test.columns != 'laeq']

    y_train = df_train['laeq']
    y_test = df_test['laeq']
    
    # parameters for gradien boosting regression
    params = {
    'learning_rate': [0.3, 0.2, 0.1, 0.05, 0.001],
    'n_estimators': [int(x) for x in np.linspace(start = 10, stop = 1000, num = 10)],
    'min_samples_split': [2, 5, 10, 20, 30],
    'min_samples_leaf': [1, 2, 4, 8, 16],
    'max_depth': [2, 3, 5, 7, 9],
    'max_features': ['auto', 'sqrt', 'log2']}

    gbr = GradientBoostingRegressor()
    tuning_model = RandomizedSearchCV(estimator=gbr, param_distributions=params,n_iter=200, cv=5, verbose=1, n_jobs=-1)
    tuning_model.fit(x_train,y_train)
    print(tuning_model.best_params_)
    
    tuned_hyper_model= GradientBoostingRegressor(**tuning_model.best_params_)
    tuned_hyper_model.fit(x_train,y_train)
    tuned_pred=tuned_hyper_model.predict(x_test)

    plt.bar(x_train.columns, tuned_hyper_model.feature_importances_)
    plt.xticks(rotation=90)
    plt.show()

    print('R2: %.4f' %r2_score(y_test,tuned_pred))
    print('MSE: %.4f' %mean_squared_error(y_test,tuned_pred))

    print(tuned_pred)
    y_pred_gbr = tuned_pred
    return y_pred_gbr

#81
y_pred_rf = pd.DataFrame(rf_modeling(df_81_train,df_81_test), columns=['y_pred_rf'])
y_pred_gbr = pd.DataFrame(gbr_model(df_81_train,df_81_test), columns=['y_pred_gbt'])
current_pred = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_81.csv')
y_pred_81 = pd.concat([current_pred, y_pred_rf,y_pred_gbr], axis=1)

y_pred_81.to_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_81.csv')

# calverie
y_pred_rf = pd.DataFrame(rf_modeling(calverie_train,calverie_test), columns=['y_pred_rf'])
y_pred_gbr = pd.DataFrame(gbr_model(calverie_train,calverie_test), columns=['y_pred_gbt'])
current_pred = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_calverie.csv')
y_pred_calverie = pd.concat([current_pred, y_pred_rf,y_pred_gbr], axis=1)

y_pred_calverie.to_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_calverie.csv')

# filosovia
y_pred_rf = pd.DataFrame(rf_modeling(filosovia_train,filosovia_test), columns=['y_pred_rf'])
y_pred_gbr = pd.DataFrame(gbr_model(filosovia_train,filosovia_test), columns=['y_pred_gbt'])
current_pred = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_filosovia.csv')
y_pred_filosovia = pd.concat([current_pred, y_pred_rf,y_pred_gbr], axis=1)

y_pred_filosovia.to_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_filosovia.csv')

# maxim
y_pred_rf = pd.DataFrame(rf_modeling(maxim_train,maxim_test), columns=['y_pred_rf'])
y_pred_gbr = pd.DataFrame(gbr_model(maxim_train,maxim_test), columns=['y_pred_gbt'])
current_pred = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_maxim.csv')
y_pred_maxim = pd.concat([current_pred, y_pred_rf,y_pred_gbr], axis=1)

y_pred_maxim.to_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_maxim.csv')

# taste
y_pred_rf = pd.DataFrame(rf_modeling(taste_train,taste_test), columns=['y_pred_rf'])
y_pred_gbr = pd.DataFrame(gbr_model(taste_train,taste_test), columns=['y_pred_gbt'])
current_pred = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_taste.csv')
y_pred_taste = pd.concat([current_pred, y_pred_rf,y_pred_gbr], axis=1)

y_pred_taste.to_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_taste.csv')

# vrijthof
y_pred_rf = pd.DataFrame(rf_modeling(vrijthof_train,vrijthof_test), columns=['y_pred_rf'])
y_pred_gbr = pd.DataFrame(gbr_model(vrijthof_train,vrijthof_test), columns=['y_pred_gbt'])
current_pred = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_vrijthof.csv')
y_pred_vrijthof = pd.concat([current_pred, y_pred_rf,y_pred_gbr], axis=1)

y_pred_vrijthof.to_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_vrijthof.csv')

# xior
y_pred_rf = pd.DataFrame(rf_modeling(xior_train,xior_test), columns=['y_pred_rf'])
y_pred_gbr = pd.DataFrame(gbr_model(xior_train,xior_test), columns=['y_pred_gbt'])
current_pred = pd.read_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_xior.csv')
y_pred_xior = pd.concat([current_pred, y_pred_rf,y_pred_gbr], axis=1)

y_pred_xior.to_csv('/Users/siucheung/School/Modern Data Analytics/Modern-Data-Analytics-Backend/Predictions/Predictions/y_pred_test_night_xior.csv')