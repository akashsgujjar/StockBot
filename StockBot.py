import time
from datetime import date, timedelta
import yfinance as yf
from Robinhood import Robinhood


def analyze_market(symbol):
    qr_code = ''
    robinhood_client = Robinhood()
    robinhood_client.login(username='', password='', qr_code=qr_code)
    confInt = .5
    confInt += perCheck(symbol, .6) * .5


def perCheck(symbol, weight):
    tickerData = yf.Ticker(symbol)
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")
    start_date_short = (date.today() - timedelta(days=5)).isoformat()
    start_date_long = (date.today() - timedelta(days=20)).isoformat()
    short_term = tickerData.history(period='1d', start=start_date_short, end=current_date)
    long_term = tickerData.history(period='1d', start=start_date_long, end=current_date)
    addTo = 0
    if analyze_buy(short_term, .05, weight / 2):
        addTo += weight / 2
    if analyze_buy(long_term, .1, weight / 2):
        addTo += weight / 2
    if analyze_sell(short_term, .05, weight / 2):
        addTo -= weight / 2
    if analyze_sell(long_term, .1, weight / 2):
        addTo -= weight / 2
    return addTo


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
    analyze_market("EBAY")
    analyze_market("KO")
    analyze_market("RDFN")
    analyze_market("HRB")
    analyze_market("ORCL")
    analyze_market("MS")
    analyze_market("CWEN")
    analyze_market("INTC")

    print("daily check done")
    time.sleep(86400)
