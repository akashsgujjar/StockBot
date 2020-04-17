import yfinance as yf
import matplotlib.pyplot as plt
from Robinhood import Robinhood
from flask import Flask
import pandas as pd
from datetime import date, datetime, timedelta
import schedule
import time


def analyze_market(symbol):
    qr_code = ''
    robinhood_client = Robinhood()
    robinhood_client.login(username='', password='', qr_code=qr_code)
    tickerData = yf.Ticker(symbol)
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")
    start_date_short = (date.today() - timedelta(days=3)).isoformat()
    start_date_long = (date.today() - timedelta(days=20)).isoformat()
    short_term = tickerData.history(period='1d', start=start_date_short, end=current_date)
    long_term = tickerData.history(period='1d', start=start_date_long, end=current_date)

    if analyze_buy(short_term, .05):
        stock_instrument = robinhood_client.instruments(symbol)[0]
        # buy_order = robinhood_client.place_market_buy_order(stock_instrument['url'], symbol, 'GFD', 1)
        print(symbol + " Stock Bought")
    if analyze_sell(short_term, .05):
        stock_instrument = robinhood_client.instruments(symbol)[0]
        # sell_order = robinhood_client.place_market_sell_order(stock_instrument['url'], symbol, 'GFD', 1)
        print(symbol + " Stock Sold")

    if analyze_buy(long_term, .1):
        stock_instrument = robinhood_client.instruments(symbol)[0]
        # buy_order = robinhood_client.place_market_buy_order(stock_instrument['url'], symbol, 'GFD', 2)
        print(symbol + " Stock Bought")
    if analyze_sell(long_term, .1):
        stock_instrument = robinhood_client.instruments(symbol)[0]
        # sell_order = robinhood_client.place_market_sell_order(stock_instrument['url'], symbol, 'GFD', 2)
        print(symbol + " Stock Sold")


def analyze_buy(tickerDf, percent):
    close_price = tickerDf['Close'].to_list()
    percent_drop = (percent * close_price[-1])
    x = close_price[0]
    z = close_price[-1]
    print(close_price)
    print(percent_drop)
    if (x - z) > percent_drop:
        return True
    else:
        return False


def analyze_sell(tickerDf, percent):
    close_price = tickerDf['Close'].to_list()
    percent_up = (percent * close_price[-1])
    x = close_price[0]
    z = close_price[-1]
    if (z - x) > percent_up:
        return True
    else:
        return False


for day_count in range(6):
    print(time.ctime())
    analyze_market("PSEC")
    analyze_market("FSM")
    analyze_market("EROS")
    analyze_market("USAS")
    time.sleep(86400)
