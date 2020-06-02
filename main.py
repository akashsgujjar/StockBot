import time
from datetime import date, timedelta
import yfinance as yf
# from Robinhood import Robinhood
from urllib.request import urlopen
# import json
import numpy as np
from flask import Flask

stock_list = ["EBAY", "KO", "RDFN", "HRB", "ORCL", "MS", "CWEN", "INTC"]
conf_list = []
app = Flask(__name__)
if __name__ == '__main__':
    app.debug = True
    app.run()


def analyze_market(symbol):
    # qr_code = '7LXYQQ2B7EZ3GD5F'
    # robinhood_client = Robinhood()
    # robinhood_client.login(username='', password='', qr_code=qr_code)
    # stock_instrument = robinhood_client.instruments(symbol)[0]
    confInt = .5
    confInt += avgCheck(symbol, .6) * .5
    conf_list.append(confInt)
    # pe_check(symbol, .2)
    # checkStat(confInt, stock_instrument, Robinhood, symbol)


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


def checkStat(confInt, stock_instrument, robinhood_client, symbol):
    if confInt <= .1:
        robinhood_client.place_market_sell_order(stock_instrument['url'], symbol, 'GFD', 3)
    if .1 < confInt <= .3:
        robinhood_client.place_market_sell_order(stock_instrument['url'], symbol, 'GFD', 2)
    if .3 < confInt <= .4:
        robinhood_client.place_market_sell_order(stock_instrument['url'], symbol, 'GFD', 1)
    if .6 < confInt <= .7:
        robinhood_client.place_market_buy_order(stock_instrument['url'], symbol, 'GFD', 1)
    if .7 < confInt <= .9:
        robinhood_client.place_market_buy_order(stock_instrument['url'], symbol, 'GFD', 2)
    if confInt >= .9:
        robinhood_client.place_market_buy_order(stock_instrument['url'], symbol, 'GFD', 3)


def finalPrint(conf_list):
    buy_me = ""
    for stock in stock_list:
        analyze_market(stock)

    conf_list = np.array(conf_list)
    temp = np.argpartition(conf_list, -4)[-4:]
    try:
        for high in temp:
            buy_me += stock_list[high] + "\n"
    except:
        errorMessage = ""
        for stock in stock_list:
            errorMessage += stock + " "
        for num in temp:
            errorMessage += str(num) + " "
        return errorMessage
    return buy_me


@app.route("/")
def temp():
    return finalPrint(conf_list)

# export FLASK_APP=main.py
