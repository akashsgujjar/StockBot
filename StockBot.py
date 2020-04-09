import yfinance as yf
import matplotlib.pyplot as plt
from Robinhood import Robinhood
import pandas as pd


def buyStock():
    qr_code = ''
    robinhood_client = Robinhood()
    robinhood_client.login(username='', password='', qr_code=qr_code)
    #stock_instrument = robinhood_client.instruments('PSEC')[0]
    #buy_order = robinhood_client.place_market_buy_order(stock_instrument['url'], 'PSEC', 'GFD', 1)


def data_gather(symbol):
    tickerSymbol = symbol
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start='2020-4-1', end='2020-4-9')
    print("Drop")
    analyze_low(tickerDf)
    print("Up")
    analyze_high(tickerDf)
    tickerDf['Close'].plot()
    plt.show()


def analyze_low(tickerDf):
    close_price = tickerDf['Close'].to_list()
    for day in range(close_price.__len__() - 2):
        percent_drop = (.05 * close_price[day])
        x = close_price[day]
        y = close_price[day + 1]
        z = close_price[day + 2]
        if (x - z) > percent_drop:
            print(x, y, z)


def analyze_high(tickerDf):
    close_price = tickerDf['Close'].to_list()
    for day in range(close_price.__len__() - 2):
        percent_up = (.05 * close_price[day])
        x = close_price[day]
        y = close_price[day + 1]
        z = close_price[day + 2]
        if (z - x) > percent_up:
            print(x, y, z)


data_gather("MSFT")
buyStock()
