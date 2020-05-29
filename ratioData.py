import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


def fundamental_metric(soup, metric):
    return soup.find(text=metric).find_next(class_='snapshot-td2').text


def get_fundamental_data(df):
    for symbol in df.index:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/70.0.3538.77 Safari/537.36"}

        url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
        soup = bs(requests.get(url, headers=headers).content, features="html.parser")

        for m in df.columns:
            df.loc[symbol, m] = fundamental_metric(soup, m)
    return df


stock_list = ['AMZN']

metric = ['P/B',
          'P/E',
          'Forward P/E',
          'PEG',
          'Debt/Eq',
          'EPS (ttm)',
          'Dividend %',
          'ROE',
          'ROI',
          'EPS Q/Q',
          'Insider Own'
          ]

df = pd.DataFrame(index=stock_list, columns=metric)
df = get_fundamental_data(df)
df

df['Dividend %'] = df['Dividend %'].str.replace('%', '')
df['ROE'] = df['ROE'].str.replace('%', '')
df['ROI'] = df['ROI'].str.replace('%', '')
df['EPS Q/Q'] = df['EPS Q/Q'].str.replace('%', '')
df['Insider Own'] = df['Insider Own'].str.replace('%', '')
df = df.apply(pd.to_numeric, errors='coerce')
df

print(df)

