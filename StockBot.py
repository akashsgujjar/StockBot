import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


def data_gather(symbol):
    tickerSymbol = symbol
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start='2019-1-1', end='2020-1-1')
    analyze(tickerDf)
    plt.show()


def analyze(tickerDf):
    close_price = tickerDf['Close'].to_list()
    percent_drop = (.05 * close_price[0])
    for day in range(close_price.__len__() - 2):
        x = close_price[day]
        y = close_price[day + 1]
        z = close_price[day + 2]
        if x > y > z and (x - z) > percent_drop:
            print(x, y, z, percent_drop)
    tickerDf['Close'].plot()


data_gather("MSFT")
