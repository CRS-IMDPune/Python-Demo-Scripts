#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Rishabh Dev
@affliation: IISER, Pune
@email: rishabh.dev@students.iiserpune.ac.in
@date: 17.01.2022

@credit: Dr. Rajib Chattopadhyay, Scientist-E India Meteorological Department, Pune
@note: This code is developed as a part of masters thesis with IMD, Pune and IITM Pune with Dr. Rajib Chattopadhyay

"""
# !Importing Modules

import os
import random
import sklearn
import numpy as np
from tqdm import tqdm
import pandas as pd   
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error

import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.callbacks import * 
from tensorflow.keras.optimizers import *
# from tensorflow.keras import backend as K

from kerashypetune import KerasGridSearch

from statistics import stdev
from scipy.stats import pearsonr

from libs import *
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator

import warnings
warnings.filterwarnings('ignore')


class predictions:
    # This class is used to predict the future values of the time series data
        
    class LSTM_Prediction:
        # This class is used for predictions made via LSTM model with target variable as a series or categorical of rainfall data
        
        def __init__(self , district, target, range, classifier):
            """Initializing the class with the district, target and range of the data

            Args:
                district ([type:str]): District name for which prediction is to be made
                
                target ([type: str]): Taget variable for which prediction is to be made
                                        * For example: 'Rainfall' for rainfall prediction
                                        * For example: 'Malaria' for malaria prediction (to be developed)
                                        
                range ([type: str]): Range of data selection
                                        * For example: '40_years' for 40 years of data to be used for prediction
                                        * For example: '7_years' for 7 years of data which is same as the Malaria data
                                        
                classifier ([type: str]): Classifier used for prediction
                                        * For example: 'Series' for for target as series (rainfall in mm)
                                        * For example: 'Category' for target as category (low, medium, high rainfall)
            """
            self.district = district
            self.target = target
            self.range = range
            self.classifier = classifier
        
        def import_data(self):
            """This will help in importing the data from the csv file for the district of ineterst for either rainfall or malaria data for specific range of years
            
                        * Rainfall Data: 1979 - 2020 Rainfall district wise rainfall data for Bihar state. 
                                        * Spatial Resolution: 0.5 x 0.5
                                        * Temporal Resolution: Weekly average of daily data
                                        * Source: IMD Gridded Rainfall Data
                                        
                        * Temeprature Data: 1979 - 2020 Temperature district wise temperature data for Bihar state.
                                        * Spatila Resolution: 0.5 x 0.5
                                        * Source: ERA5 Reanalysis data
                                        * Temporal Resolution: Daily data
                                        
                                * Tmax Data: Maximum Temperature
                                        * Temporal Resolution: Weekly maximum of daily data
                                        
                                *Tmin Data: Minimum Temperature
                                        * Temporal Resolution: Weekly minimum of daily data
                        
                        * Humidity Data: 1979 - 2020 Humidity district wise humidity data for Bihar state.
                                        * Spatial Resolution: 0.5 x 0.5
                                        * Source: ERA5 Reanalysis data
                                        * Temporal Resolution: Weekly average of daily data
                                        
                        * Soil Moisture Data: 1979 - 2020 Soil Moisture district wise soil moisture data for Bihar state.
                                        * Spatial Resolution: 0.5 x 0.5
                                        * Source: ERA5 Reanalysis data
                                        * Temporal Resolution: Weekly average of daily data
            Returns:
                [DataFrame]: DataFrame of the data with target district and specific range of years
            """
            #* Importing raw Data for 40 years 1979 - 2020
            rain = pd.read_csv(r'E:\MS_Project\Data\40_Years_Data\Rain_40_years.csv')
            Tmax = pd.read_csv(r'E:\MS_Project\Data\40_Years_Data\Tmax_40Years.csv')
            Tmin = pd.read_csv(r'E:\MS_Project\Data\40_Years_Data\Tmin_40Years.csv')
            Humidity = pd.read_csv(r'E:\MS_Project\Data\40_Years_Data\Humidity_40Years.csv')
            Soil_moisture = (pd.read_csv(r'E:\MS_Project\Data\40_Years_Data\Soil_Moisture_40Years.csv'))
            
            dist = self.district
            data = pd.concat([rain['weeks'] , rain[f'{dist}'] , Tmax[f'{dist}'] , Tmin[f'{dist}'] ,Humidity[f'{dist}'] , Soil_moisture[f'{dist}']],
                        axis = 1, ignore_index=True)

            data.reset_index(drop = True , inplace=True)

            df = data
            df.columns = ['Weeks' , 'Rain' , 'Tmax' , 'Tmin', 'Humidity' , 'Soil_moisture']
                
            ##?---------------- Importing 40 years Rainfall Data 1979 - 2020 ----------------##
            if self.target == 'Rainfall' and self.range == '40_years' and self.classifier == 'Series':
                return df
            
            ##?----------------- Importing 7 years Rainfall Data 2014 - 2020 ------------------##
            if self.target == 'Rainfall' and self.range == '7_years' and self.classifier == 'Series':
                return df.tail(366)
            
            
            ##### ------------------ creating categorical data ----------------------#####
            rainn = rain[f'{dist}'].values
            upper_tertile = np.quantile(rainn, .66)
            lower_tertile = np.quantile(rainn, .33)

            Rainfall = []

            for i in rainn:
                if i >= upper_tertile:
                    Rainfall.append(2)
                if i < upper_tertile and i > lower_tertile:
                    Rainfall.append(1)
                if i <= lower_tertile:
                    Rainfall.append(0)

            Rainfall = pd.DataFrame(Rainfall) # This will be predictand

            cat_data = pd.concat([rain['weeks'] , rain[f'{dist}'] , Tmax[f'{dist}'] , Tmin[f'{dist}'] ,Humidity[f'{dist}'] , Soil_moisture[f'{dist}'] , Rainfall],
                            axis = 1, ignore_index=True)

            cat_data.reset_index(drop = True , inplace=True)

            cat_data.columns = ['Weeks' , 'Rain' , 'Tmax' , 'Tmin', 'Humidity' , 'Soil_moisture' , 'Rainfall']
            
            ##?----------------- Importing 40 years Categorical Rainfall Data 2014 - 2020 ------------------##
            if self.target =='Rainfall' and self.classifier == 'Categorical' and self.range == '40_years':
                return cat_data
            
            ##?----------------- Importing 7 years Categorical Rainfall Data 2014 - 2020 ------------------##
            if self.target =='Rainfall' and self.classifier == 'Categorical' and self.range == '7_years':
                return cat_data.tail(366)
    
        def build_model(self , win_length, num_features):
            """Builds the LSTM model with the given parameters

            Args:
                win_length ([type: int]): Window length used for creating a sliding window
                
                num_features ([type: int]): Number of features used in training the model ( Here 5 features are used)
                                        * Rainfall
                                        * Tmax
                                        * Tmin
                                        * Humidity
                                        * Soil_moisture
            Returns:
                LSTM model
            """
            model =  tf.keras.Sequential()
            model.add(tf.keras.layers.LSTM(32, activation='elu', input_shape= (win_length, num_features)))
            model.add(tf.keras.layers.Dense(1))
            
            return model
            # This model is a simple one layer Vanilla LSTM model with 32 neurons
            
        def model_training(self , df):
            """This function will do the following:
                * Split the data into training and testing data using train_test_split
                * Shift data to create lead times
                * Normalize the shifted data
                * Imports the model using build_model
                * compiles the model
                * Trains the model
                
                * For lead time 1 and 2, history of the model is saved
                * For each lead time, Correlation, MSE and R-squared are calculated and stored in a list
                * For each lead time, the predictions are made and stored in a pandas dataframe
                * Prediction are then passed through a variance correction function to remove the smoothness effect

            Args:
                df ([type: Pandas data frame]):  Data obtained as output of import_data function
                
            Returns:

            """
            
            ##---------------------- Empty buckets for skill scores----------------##
            
            # df = self.import_data()
            R_sqrd = []
            R_mse = []
            Corr = []

            for i in range(1,5):
                
                #! Create the Preictors and Predictand with traintestsplit
                df_input=df[['Rain' , 'Tmax' , 'Tmin', 'Humidity' , 'Soil_moisture']]
                
                if self.classifier == 'Categorical':
                    X_train, X_test, y_train, y_test = train_test_split(df_input, df['Rainfall'], test_size=0.26, random_state=123, shuffle = False)
                    rainn = y_test.head(566)
                if self.classifier == 'Series':
                    rainn = []
                
                if self.classifier == 'Series':
                    X_train, X_test, y_train, y_test = train_test_split(df_input, df['Rain'], test_size=0.26, random_state=123, shuffle = False)
                    
                #! Shifting Data to create lag
                y_train = y_train.shift(-i)
                y_train = y_train.fillna(0)
                y_test = y_test.shift(-i)
                y_test = y_test.fillna(0)
                
                #! Scaling the data
                scaler = MinMaxScaler()
                X_train = scaler.fit_transform(X_train)
                X_test = scaler.fit_transform(X_test)
                y_train = scaler.fit_transform(pd.DataFrame(y_train))
                y_test = scaler.fit_transform(pd.DataFrame(y_test))
                
                #! Creating the Timeseries Generator
                win_length=4
                batch_size=32
                num_features=5
                train_generator = TimeseriesGenerator(X_train, y_train, length=win_length, sampling_rate=1, batch_size=batch_size)
                test_generator = TimeseriesGenerator(X_test, y_test, length=win_length, sampling_rate=1, batch_size=batch_size)
                
                #! Defining Model
                model =  self.build_model(win_length, num_features)

                # use of early stopping is optional since training time is short and #epochs is not a high value 
                #! Early Stopping
                early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                                patience=2,
                                                                mode='min')
                #! Model Compilation
                model.compile(loss=tf.losses.MeanSquaredError(),
                            optimizer=tf.optimizers.Adam(beta_1 = 0.5 , beta_2 = 0.9),
                            metrics=[tf.metrics.MeanAbsoluteError()])

                #! Model Fitting
                history = model.fit_generator(train_generator, epochs=50,
                                    validation_data=test_generator,
                                    shuffle=False , verbose = False)
                
                
                #! Saving the lead time 1 week model
                if i == 1:
                    training_mae = history.history['mean_absolute_error']
                    validation_mae = history.history['val_mean_absolute_error']
                    
                if i == 2:
                    training_mae_2 = history.history['mean_absolute_error']
                    validation_mae_2 = history.history['val_mean_absolute_error']
                    
                if i == 1 and self.classifier == 'Series':
                    
                    predictions1=model.predict(test_generator)
                    df_pred=pd.concat([pd.DataFrame(predictions1), pd.DataFrame(X_test[:,0].reshape(-1,1))],axis=1)
                    rev_trans1=scaler.inverse_transform(df_pred)
                    df_final_1= pd.DataFrame(rev_trans1)
                    df_final_1 = df_final_1.dropna()
                    dff = df_final_1
                    
                    sd_pred = stdev(dff[0])
                    sd_actual = stdev(dff[1])

                    mean_pred = np.mean(dff[0])
                    mean_actual = np.mean(dff[1])   

                    dff['var_corr'] = (dff[0] - mean_pred)*(sd_actual/sd_pred) + mean_actual
                    dff['var_corr'] = dff['var_corr'].apply(lambda x: np.abs(x))
                    
                if i == 1 and self.classifier == 'Categorical':
                    dff = pd.DataFrame()
                
                #! Creating the Test predictions
                predictions=model.predict(test_generator)
                df_pred=pd.concat([pd.DataFrame(predictions), pd.DataFrame(X_test[:,0].reshape(-1,1))],axis=1)
                rev_trans=scaler.inverse_transform(df_pred)
                df_final=pd.DataFrame(rev_trans)
                df_final = df_final.dropna()
                df_final['Rain_pred'] = df_final[0]
                    
                if i == 1 and self.classifier == 'Categorical':
                    upper_tertile = np.quantile(df_final['Rain_pred'], .66)
                    lower_tertile = np.quantile(df_final['Rain_pred'], .33)
                    Rainfall_pred = []

                    for i in df_final['Rain_pred']:
                        if i >= upper_tertile:
                            Rainfall_pred.append(2)
                        if i < upper_tertile and i > lower_tertile:
                            Rainfall_pred.append(1)
                        elif i <= upper_tertile:
                            Rainfall_pred.append(0)
                if i == 1 and self.classifier == 'Series': 
                    Rainfall_pred = []
                            
                if i == 2 and self.classifier == 'Categorical':
                    upper_tertile = np.quantile(df_final['Rain_pred'], .66)
                    lower_tertile = np.quantile(df_final['Rain_pred'], .33)
                    Rainfall_pred_2 = []

                    for i in df_final['Rain_pred']:
                        if i >= upper_tertile:
                            Rainfall_pred_2.append(2)
                        if i < upper_tertile and i > lower_tertile:
                            Rainfall_pred_2.append(1)
                        elif i <= upper_tertile:
                            Rainfall_pred_2.append(0)
                if i == 2 and self.classifier == 'Series':
                    Rainfall_pred_2 = []

                #! Calcukating the Corr and R-squared value for each tau
                corr,_ = (pearsonr(df_final[1] , df_final[0]))
                Corr.append(corr)
                R_sqrd.append((corr**2))
                
                #! Calcukating the MSE value for each tau
                rms = mean_squared_error(df_final[1] , df_final[0], squared=True)
                R_mse.append(rms)
                
            return dff, R_sqrd, R_mse, Corr, training_mae, validation_mae , training_mae_2, validation_mae_2, Rainfall_pred, Rainfall_pred_2, df_final,rainn
        
        def plot_LSTM(self , dff, R_sqrd, R_mse, Corr, training_mae, validation_mae, training_mae_2, validation_mae_2, Rainfall_pred, Rainfall_pred_2, df_final, rainn):
            dist = self.district
            fig, axs = plt.subplots(2,3, figsize=(23, 10), facecolor='w', edgecolor='k')
            fig.tight_layout(pad=4)

            #? Plotting the Epochs vs MAE
            axs[0][0].plot(training_mae, label='Training MAE')
            axs[0][0].plot(validation_mae, label='Validation MAE')
            axs[0][0].legend()
            axs[0][0].set_xlabel('Epoch')
            axs[0][0].set_ylabel('MAE')
            axs[0][0].set_title(f'Epochs vs MAE for {dist} District for Lead Time 1 week forecast')
            
            axs[0][1].plot(training_mae_2, label='Training MAE')
            axs[0][1].plot(validation_mae_2, label='Validation MAE')
            axs[0][1].legend()
            axs[0][1].set_xlabel('Epoch')
            axs[0][1].set_ylabel('MAE')
            axs[0][1].set_title(f'Epochs vs MAE for {dist} District for Lead Time 2 week forecast')

            #? Plotting the Tau vs R-squared
            x = range(4)
            x_ticks = [1,2,3,4]
            axs[0][2].plot(range(4) , R_sqrd , '-o' , label = "R-squared")
            ax2 = axs[0][2].twinx()
            ax2.plot(range(4) , R_mse , '-o' , label = "MSE" , color = 'orange')
            axs[0][2].legend()
            ax2.legend()
            axs[0][2].set_xticks(x , x_ticks)
            axs[0][2].set_xlabel('Time Lead - Tau (in weeks)')
            axs[0][2].set_ylabel('R-squared')
            ax2.set_ylabel('Mean Absolute Error')
            axs[0][2].set_title(f'Tau vs Skill for {dist} District')

            #? Creating the Skill Score
            axs[1][0].text(0.1, 0.40, f'R-squared value for {dist} at lead Time 1 week is : {np.round(R_sqrd[0]*100 , 2)}' , size = 16)
            axs[1][0].text(0.1, 0.55, f'Corrleation value for {dist} at lead Time 1 week is : {np.round(Corr[0] , 2)}' , size = 16)
            axs[1][0].text(0.1, 0.7, f'MSE value for {dist} at lead Time 1 week is : {np.round((R_mse[0]) , 2)}' , size = 16)
            axs[1][0].axis('off')
            
            #? Creating the Skill Score
            axs[1][1].text(0.1, 0.40, f'R-squared value for {dist} at lead Time 2 week is : {np.round(R_sqrd[1]*100 , 2)}' , size = 16)
            axs[1][1].text(0.1, 0.55, f'Corrleation value for {dist} at lead Time 2 week is : {np.round(Corr[1] , 2)}' , size = 16)
            axs[1][1].text(0.1, 0.7, f'MSE value for {dist} at lead Time 2 week is : {np.round((R_mse[1]) , 2)}' , size = 16)
            axs[1][1].axis('off')
            
            if self.classifier == 'Categorical':
                #? Creating the Confusion Matrix
                axs[1][2].axis('off')
                a =  sklearn.metrics.classification_report(rainn, Rainfall_pred)
                axs[1][2].text(0.1 , 0.2 , f'{a}' , size = 16)
                
            if self.classifier == 'Series':
                # axs[1][2].plot(df_final_1[0] , label = "Predicted")
                axs[1][2].plot(dff[1] , label = "Actual")
                axs[1][2].plot(dff['var_corr'] , label = "var_corr_Predicted")
                axs[1][2].legend()
                axs[1][2].set_xlabel('Weeks (Test Period)')
                axs[1][2].set_ylabel('Rainfall')
                axs[1][2].set_title(f'Actual vs Predicted Rainfall for {dist} District for Test Period for Lead Time 1 week')

            fig.show()
            
        
if __name__ == '__main__':
    
    a = predictions.LSTM_Prediction('Patna', 'Rainfall', '40_years', 'Categorical')
    dff, R_sqrd, R_mse, Corr, training_mae, validation_mae , training_mae_2, validation_mae_2, Rainfall_pred, Rainfall_pred_2, df_final,rainn = a.model_training(a.import_data())
    a.plot_LSTM(dff, R_sqrd, R_mse, Corr, training_mae, validation_mae, training_mae_2, validation_mae_2, Rainfall_pred, Rainfall_pred_2, df_final, rainn)