import time
from datetime import date, timedelta
import yfinance as yf
# from Robinhood import Robinhood
from urllib.request import urlopen
# import json
import numpy as np
from flask import Flask, render_template
import pandas
import csv
import matplotlib.pyplot as plt

app = Flask(__name__)

stock_list = ["EBAY", "KO", "RDFN", "HRB", "ORCL", "MS", "CWEN", "INTC", "F", "GE", "AAL", "DIS", "DAL", "CCL", "GPRO"]
conf_list = []
with open("owned.txt") as f:
    ownedList = f.read().splitlines()
with open("data.txt", "w") as my_output_file:
    with open("stocks.csv", "r") as my_input_file:
        [my_output_file.write(",".join(row) + '\n') for row in csv.reader(my_input_file)]
    my_output_file.close()
f = open("data.txt", "a")


def analyze_market(symbol):
    confInt = .5
    confInt += avgCheck(symbol, .6) * .5
    conf_list.append(confInt)
    # pe_check(symbol, .2)
    checkStat(confInt, symbol)


def avgCheck(symbol, weight):
    tickerData = yf.Ticker(symbol)
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")
    start_date_short = (date.today() - timedelta(days=5)).isoformat()
    start_date_long = (date.today() - timedelta(days=20)).isoformat()
    short_term = tickerData.history(period='1d', start=start_date_short, end=current_date)
    long_term = tickerData.history(period='1d', start=start_date_long, end=current_date)
    shortChange = analyze_change(short_term) * .03
    longChange = analyze_change(long_term) * .03
    averageChange = (shortChange + longChange) / 2
    if averageChange > weight:
        return weight * - 1
    return averageChange * -1


def analyze_change(tickerDf):
    close_price = tickerDf['Close'].to_list()
    x = close_price[0]
    z = close_price[-1]
    return ((z - x) / x) * 100


def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    # return json.loads(data)


def pe_check(symbol, weight):
    url = "https://financialmodelingprep.com/api/v3/financial-ratios/" + "KO" + "?apikey=demo"
    print(get_jsonparsed_data(url))


def checkStat(confInt, symbol):
    if confInt <= .1:
        if symbol in ownedList:
            f.write("," + str(getCurrentPrices(symbol)) + "\n")
            ownedList.remove(symbol)
    if .1 < confInt <= .3:
        if symbol in ownedList:
            f.write("," + str(getCurrentPrices(symbol)) + "\n")
            ownedList.remove(symbol)
    if .3 < confInt <= .5:
        if symbol in ownedList:
            f.write("," + str(getCurrentPrices(symbol)) + "\n")
            ownedList.remove(symbol)
    if .5 < confInt <= .7:
        f.write(str(getCurrentPrices(symbol)) + "\n")
        ownedList.append(symbol)
    if .7 < confInt <= .9:
        f.write(str(getCurrentPrices(symbol)) + "\n")
        ownedList.append(symbol)
    if confInt >= .9:
        f.write(str(getCurrentPrices(symbol)) + "\n")
        ownedList.append(symbol)


def getCurrentPrices(symbol):
    tickerData = yf.Ticker(symbol)
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")
    start_date_short = (date.today() - timedelta(days=1)).isoformat()
    short_term = tickerData.history(period='1d', start=start_date_short, end=current_date)
    return short_term['Open'].to_list()[0]


def fileSwap():
    read_file = pandas.read_csv("data.txt")
    read_file.to_csv("stocks.csv", index=None)
    stockDF = pandas.read_csv("stocks.csv")
    bought = stockDF['Bought'].sum()
    sold = stockDF['Sold'].sum()
    coords = open("coords.txt", "a")
    coords.write(str(sold - bought) + "\n")


def graphProfit():
    xList = []
    yList = []
    start = 0
    with open('coords.txt', 'r') as f:
        coordinateString = [line.strip() for line in f]
    for _ in coordinateString:
        xList.append(start)
        start += 1
    for val in coordinateString:
        yList.append(float(val))
    plt.ylabel("Profits")
    plt.xlabel("Days")
    plt.plot(xList, yList)
    plt.savefig('static/akashofclans.png')


def finalPrint(rating):
    buy_me = ""
    for stock in stock_list:
        analyze_market(stock)
    fileSwap()
    with open("owned.txt", "w") as outfile:
        outfile.write("\n".join(ownedList))
    # graphProfit()
    rating = np.array(rating)
    rating.tolist()
    rating = list(dict.fromkeys(rating))
    highIndex = np.argpartition(rating, -4)[-4:]
    try:
        for high in highIndex:
            buy_me += stock_list[high] + ",\n"
    except:
        errorMessage = ""
        for stock in stock_list:
            errorMessage += stock + " "
        for num in rating:
            errorMessage += str(num) + " "
        return errorMessage
    return buy_me


def printAllStocks():
    stockReturn = ""
    for stockName in stock_list:
        stockReturn += stockName + ", "
    return stockReturn


@app.route("/")
def temp():
    return render_template('index.html', buyMe=finalPrint(conf_list), totalList=printAllStocks())
    # return finalPrint(conf_list)

# export FLASK_APP=main.py
# finalPrint(conf_list)

# print(temp())
