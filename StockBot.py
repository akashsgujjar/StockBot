import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


def data_gather(symbol):
    tickerSymbol = symbol
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start='2017-1-1', end='2020-1-1')
    print("Drop")
    analyze_low(tickerDf)
    print("Up")
    analyze_high(tickerDf)
    plt.show()


def analyze_low(tickerDf):
    close_price = tickerDf['Close'].to_list()
    percent_drop = (.2 * close_price[0])
    for day in range(close_price.__len__() - 2):
        x = close_price[day]
        y = close_price[day + 1]
        z = close_price[day + 2]
        if x > y > z and (x - z) > percent_drop:
            print(x, y, z)


def analyze_high(tickerDf):
    close_price = tickerDf['Close'].to_list()
    percent_up = (.1 * close_price[0])
    for day in range(close_price.__len__() - 2):
        x = close_price[day]
        y = close_price[day + 1]
        z = close_price[day + 2]
        if x < y < z and (x - z) < percent_up:
            print(x, y, z)
    tickerDf['Close'].plot()


data_gather("MSFT")
