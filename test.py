import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA, ARMAResults
import ipywidgets as widgets
import seaborn as sns
from sklearn.metrics import r2_score, median_absolute_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_squared_error, mean_squared_log_error
import warnings
warnings.simplefilter("ignore")
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
init_notebook_mode(connected=True)

# predict food price
def predict_food_price(food_name):
    df = pd.read_csv("/content/drive/MyDrive/FYP/2.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['price'] = df['price'].astype(float)
    df.index = df['date']
    del df['date']
    df["production"] = df["production"]
    df = df.dropna()

    productions = set(df.production)

    chosen_Item = food_name
    Item_df = df[df.production == chosen_Item].drop("production", 1)
    
    print ("Stationarity Check for %s" % chosen_Item) 
    
    #check stationarity
    is_stationary = check_stationarity(Item_df,'food')
    
    # ACF and PACF plots
    plot_acf(Item_df,lags = 20)
    plot_pacf(Item_df,lags = 20)
    plt.show()
    

    if (is_stationary==True):
        d = 0    
    else:
        d = 1

  # creating the arima model
    arima_model = ARIMA(Item_df, order=(2, d, 2)).fit()
    
    out_of_sample_forecast = arima_model.forecast(steps=1)[0]  # predictions
    
    food_price = out_of_sample_forecast[0]

    # getting the values of  predicted USD for next month and the last month mean value
    usd_price, mean_rate = predict_usd_price()
    
    new_food_price = food_price * (usd_price/mean_rate)
    return round(new_food_price,2)
    
            
# usd prediction fro next month
def predict_usd_price():

    df_usd = pd.read_csv("/content/drive/MyDrive/FYP/USD.csv")
    df_usd['date'] = pd.to_datetime(df_usd['date'])
    df_usd['rate'] = df_usd['rate'].astype(float)
    df_usd.index = df_usd['date']
    del df_usd['date']

    df_usd["curr"] = df_usd["curr"]

    df_usd = df_usd.dropna()

    curr = set(df_usd.curr)
    
    chosen_Item_usd = 'USD'
    Item_df_usd = df_usd[df_usd.curr == chosen_Item_usd].drop("curr", 1).tail(90)
    
    print ("Stationarity Check for USD")
    
    is_stationary = check_stationarity(Item_df_usd,'usd')

    rateX = Item_df_usd["rate"].tail(30)
    rateX_mean = rateX.mean()
    # ACF and PACF plots
    plot_acf(Item_df_usd,lags = 20)
    plot_pacf(Item_df_usd,lags = 20)
    plt.show()
    d = -1
    if (is_stationary==True):
        d = 0    
    else:
        d = 1

    arima_model = ARIMA(Item_df_usd, order=(2, d, 2)).fit()

    ## Evaluating the model using MSE and MAE values
    #predictions = arima_model.predict(start=0, end=len(Item_df_usd))
    
    #mse = mean_squared_error(list(Item_df_usd.rate), list(predictions))
    #print("Mean Squared Error:", mse)
    
    #mae = mean_absolute_error(list(Item_df_usd.rate), list(predictions))
    #print("Mean Absolute Error:", mae)
  
  #predicting usd price 
    out_of_sample_forecast_usd = arima_model.forecast(steps=1)[0]
    usd = out_of_sample_forecast_usd[0]
    print("Next Month: ", usd, 'LKR')
    return usd,rateX_mean
        
    
    
    
def check_stationarity(Item_df,Type):

    Item_df.plot(figsize=(10, 10))
    Item_df.hist(figsize=(10, 10))
    plt.show()
    
    if(Type == 'food'):
        X = Item_df["price"].values
    else:
        X = Item_df["rate"].values
        
    split = int(len(X) / 2)
    X1, X2 = X[0:split], X[split:]
    mean1, mean2 = X1.mean(), X2.mean()
    var1, var2 = X1.var(), X2.var()
    print('mean1=%f, mean2=%f' % (mean1, mean2))
    print('variance1=%f, variance2=%f' % (var1, var2))
      
    result = adfuller(X)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    
    p = result[1]
    if (p > 0.05):
        print("Time Series is NOT Stationary")
        Item_df = Item_df.diff()
        return False
    else:
        print("Time Series is Stationary")
        return True
