import os
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.arima_model import ARIMA


def runArima(file_name):
    path = "./resources/"
    os.chdir(path)
    os.getcwd()

    df = pd.read_csv(file_name, index_col='Date', parse_dates=True)
    print('Shape of data', df.shape)
    df.head()
    df

    price = df['Price']
    lnprice = np.log(price)
    lnprice
    plt.plot(lnprice)
    plt.show()

    # Test data set accuracy
    acf_1 = acf(lnprice)[1:20]
    test_df = pd.DataFrame([acf_1]).T
    test_df.columns = ['Auto Correlation']
    test_df.index += 1
    test_df.plot(kind='bar')
    plt.show()

    pacf_1 = pacf(lnprice)[1:20]
    test_df = pd.DataFrame([pacf_1]).T
    test_df.columns = ['Partial Auto Correlation']
    test_df.index += 1
    test_df.plot(kind='bar')
    plt.show()

    result = ts.adfuller(lnprice, 1)
    result
    lnprice_diff = lnprice - lnprice.shift()
    diff = lnprice_diff.dropna()
    acf_1_diff = acf(diff)[1:20]
    test_df = pd.DataFrame([acf_1_diff]).T
    test_df.columns = ['First Difference Auto Correlation']
    test_df.index += 1
    test_df.plot(kind='bar')
    pacf_1_diff = pacf(diff)[1:20]
    plt.plot(pacf_1_diff)
    plt.show()

    test_df = pd.DataFrame([pacf_1_diff]).T
    test_df.columns = ['First Difference Partial Correlation']
    test_df.index += 1
    test_df.plot(kind='bar')
    plt.show()

    price_matrix = lnprice.to_numpy()
    model = ARIMA(price_matrix, order=(1, 0, 1))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())
    predictions = model_fit.predict(122, 127, typ='levels')
    predictions
    predictionsAdjusted = np.exp(predictions)
    predictionsAdjusted
    plt.plot(predictionsAdjusted)
    plt.title("Price Prediction")
    plt.show()
