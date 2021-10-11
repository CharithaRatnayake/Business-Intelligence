import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simplejson as simplejson
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.arima_model import ARIMA
import rest.response
from model.price import Price
from rest.response import Response
import csv


def readCSV(file):
    list = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            print(row)
            im = Price(row["Date"], row["Price"])
            # list.append(json.dumps(im.__dict__))
            list.append(im.__dict__)
            line_count += 1
        print(list)
    return list


def runArima(file_name, category, sub):
    path = "./resources/"

    try:
        os.chdir(path)
    except:
        print("not an error but ok")

    print("File name: " + file_name)
    print("category: " + category)
    print("sub: " + sub)
    print("Current Path: " + os.getcwd())

    p1 = rest.response

    if category != "":
        file_name = file_name + "_" + category

    if sub != "":
        file_name = file_name + "_" + sub

    file = file_name + ".csv"
    print("File name: " + file)

    try:
        df = pd.read_csv(file, index_col='Date', parse_dates=True)
    except FileNotFoundError:
        p1 = Response(401, "File not found.", "")
        return p1

    print('Shape of data', df.shape)
    df.head()
    df

    try:
        imports = df['Price']
    except:
        p1 = Response(401, "Couldn't find the data in CSV file.", "")
        return p1


    p1 = Response(0, "Success", readCSV(file))
    return p1

    df.plot()

    lnPrice = np.log(imports)
    lnPrice
    plt.plot(lnPrice)
    plt.show()

    # Test data set accuracy
    acf_1 = acf(lnPrice)[1:20]
    test_df = pd.DataFrame([acf_1]).T
    test_df.columns = ['Auto Correlation']
    test_df.index += 1
    test_df.plot(kind='bar')
    plt.show()

    pacf_1 = pacf(lnPrice)[1:20]
    test_df = pd.DataFrame([pacf_1]).T
    test_df.columns = ['Partial Auto Correlation']
    test_df.index += 1
    test_df.plot(kind='bar')
    plt.show()

    result = ts.adfuller(lnPrice, 1)
    result
    lnpqty_diff = lnPrice - lnPrice.shift()
    diff = lnpqty_diff.dropna()
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

    import_matrix = lnPrice.to_numpy()
    model = ARIMA(import_matrix, order=(1, 0, 1))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())
    predictions = model_fit.predict(0, 60, typ='levels')
    predictions
    predictionsAdjusted = np.exp(predictions)
    predictionsAdjusted
    plt.plot(predictionsAdjusted)
    plt.title("Import Prediction")
    plt.show()
