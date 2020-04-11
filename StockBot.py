import yfinance as yf
import matplotlib.pyplot as plt
from Robinhood import Robinhood
from flask import Flask
import pandas as pd
from datetime import date
import schedule
import time


def analyze_market(symbol, day):
    qr_code = ''
    robinhood_client = Robinhood()
    robinhood_client.login(username='', password='', qr_code=qr_code)
    tickerData = yf.Ticker(symbol)
    today = date.today()
    current = today.strftime("%Y-%m-%d")
    tickerDf = tickerData.history(period='1d', start='2020-4-4', end=current)
    if analyze_buy(tickerDf, symbol, day):
        stock_instrument = robinhood_client.instruments(symbol)[0]
        # buy_order = robinhood_client.place_market_buy_order(stock_instrument['url'], symbol, 'GFD', 1)
        print("Stock Bought")
    if analyze_sell(tickerDf, symbol, day):
        stock_instrument = robinhood_client.instruments(symbol)[0]
        # sell_order = robinhood_client.place_market_sell_order(stock_instrument['url'], symbol, 'GFD', 1)
        print("Stock Sold")


def analyze_buy(tickerDf, symbol, day):
    close_price = tickerDf['Close'].to_list()
    print(close_price)
    percent_drop = (.05 * close_price[day])
    x = close_price[day]
    y = close_price[day + 1]
    z = close_price[day + 2]
    if (x - z) > percent_drop:
        print(x, y, z)
        return True
    else:
        return False


def analyze_sell(tickerDf, symbol, day):
    close_price = tickerDf['Close'].to_list()
    percent_up = (.05 * close_price[day])
    x = close_price[day]
    y = close_price[day + 1]
    z = close_price[day + 2]
    if (z - x) > percent_up:
        print(x, y, z)
        return True
    else:
        return False


for day_count in range(6):
    print(time.ctime())
    analyze_market("PSEC", day_count)
    time.sleep(86400)
