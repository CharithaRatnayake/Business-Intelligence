import pyrebase
import csv
from model.imports import Imports
from datetime import datetime
import dateparser
from model.prediction import Prediction

config = {
    "apiKey": "AIzaSyAWTjNKOWCEQJmCEtNFAm4idevo67NB9Ao",
    "authDomain": "totemic-courage-327512.firebaseapp.com",
    "databaseURL": "https://totemic-courage-327512-default-rtdb.asia-southeast1.firebasedatabase.app",
    "storageBucket": "totemic-courage-327512.appspot.com",
    "projectId": "totemic-courage-327512",
    "messagingSenderId": "233393668944",
    "appId": "1:233393668944:web:73afadbba6791437292255",
    "measurementId": "G-J99TJ9YQRD"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def readCSVImports(file, row1, row2):
    list = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            im = Imports(row[row1], row[row2])
            list.append(im)
            line_count += 1
        print(list)
    return list


def runPrediction():
    # Imports
    CoconutOil = importPrediction("./resources/import_CoconutOil.csv")
    Milk = importPrediction("./resources/import_Milk.csv")
    Rice_Nadu = importPrediction("./resources/import_Rice_Nadu.csv")
    Rice_Samba = importPrediction("./resources/import_Rice_Samba.csv")
    Sugar = importPrediction("./resources/import_Sugar.csv")
    db.child("imports").child("CoconutOil").set(CoconutOil)
    db.child("imports").child("Milk").set(Milk)
    db.child("imports").child("Rice_Nadu").set(Rice_Nadu)
    db.child("imports").child("Rice_Samba").set(Rice_Samba)
    db.child("imports").child("Sugar").set(Sugar)

    # Price
    Sugar_Retail_Dambulla = pricePrediction("./resources/price_Sugar_Retail_Dambulla.csv")
    Sugar_Retail_Pettah = pricePrediction("./resources/price_Sugar_Retail_Pettah.csv")
    Sugar_WholeSale_Dambulla = pricePrediction("./resources/price_Sugar_WholeSale_Dambulla.csv")
    Sugar_WholeSale_Pettah = pricePrediction("./resources/price_Sugar_WholeSale_Pettah.csv")
    db.child("price").child("Sugar_Retail_Dambulla").set(Sugar_Retail_Dambulla)
    db.child("price").child("Sugar_Retail_Pettah").set(Sugar_Retail_Pettah)
    db.child("price").child("Sugar_WholeSale_Dambulla").set(Sugar_WholeSale_Dambulla)
    db.child("price").child("Sugar_WholeSale_Pettah").set(Sugar_WholeSale_Pettah)

    # Sales
    CoconutOil = salesPrediction("./resources/sales_CoconutOil.csv")
    Dhal = salesPrediction("./resources/sales_Dhal.csv")
    MilkPowder = salesPrediction("./resources/sales_MilkPowder.csv")
    Rice_Nadu = salesPrediction("./resources/sales_Rice_Nadu.csv")
    Rice_Samba = salesPrediction("./resources/sales_Rice_Samba.csv")
    Sugar = salesPrediction("./resources/sales_Sugar.csv")
    db.child("sales").child("Dhal").set(Dhal)
    db.child("sales").child("CoconutOil").set(CoconutOil)
    db.child("sales").child("MilkPowder").set(MilkPowder)
    db.child("sales").child("Rice_Nadu").set(Rice_Nadu)
    db.child("sales").child("Rice_Nadu").set(Rice_Nadu)
    db.child("sales").child("Rice_Samba").set(Rice_Samba)
    db.child("sales").child("Sugar").set(Sugar)


def importPrediction(path):
    csv = readCSVImports(path, "Date", "Price")
    count = 0
    currentMonthPrice = 0
    min = 100000
    max = 0

    for m in csv:
        month = datetime.strptime(m.date, "%m/%d/%Y").month
        currentMonth = datetime.today().month

        if month == currentMonth:
            price = int(m.importValue)
            currentMonthPrice += price
            count += 1
            if min > price:
                min = price
            if max < price:
                max = price

    prediction = Prediction("import", "Price", min, max, currentMonthPrice/count)
    return prediction.__dict__


def pricePrediction(path):
    csv = readCSVImports(path, "Date", "Price")
    count = 0
    currentMonthPrice = 0
    min = 100000
    max = 0

    for m in csv:
        month = datetime.strptime(m.date, "%m/%d/%Y").month
        currentMonth = datetime.today().month

        if month == currentMonth:
            price = int(m.importValue)
            currentMonthPrice += price
            count += 1
            if min > price:
                min = price
            if max < price:
                max = price

    prediction = Prediction("price", "Price", min, max, currentMonthPrice/count)
    return prediction.__dict__


def salesPrediction(path):
    csv = readCSVImports(path, "Date", "Sales")
    count = 0
    currentMonthPrice = 0
    min = 100000
    max = 0

    for m in csv:
        month = datetime.strptime(m.date, "%m/%d/%Y").month
        currentMonth = datetime.today().month

        if month == currentMonth:
            price = int(m.importValue)
            currentMonthPrice += price
            count += 1
            if min > price:
                min = price
            if max < price:
                max = price

    prediction = Prediction("Sales", "Sales", min, max, currentMonthPrice/count)
    return prediction.__dict__
