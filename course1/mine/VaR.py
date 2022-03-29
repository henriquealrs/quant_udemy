import pandas as pd
import numpy as np
from scipy.stats import norm
import datetime
import yfinance as yf
import matplotlib.pyplot as plt

def download_data(stock, start_date, end_date):
    data = {}
    ticker = yf.download(stock, start_date, end_date)
    data[stock] = ticker['Adj Close']
    return pd.DataFrame(data);

def calculate_var(position, c, mu, sigma):
    v = norm.ppf(1-c)
    var = position *(mu - sigma*v)
    return var

if __name__ == '__main__':

    stock_data = download_data('V', datetime.datetime(2013, 1, 1), datetime.datetime(2021,1,1))
    stock_data['returns'] = np.log( stock_data['V'] / stock_data['V'].shift())
    stock_data = stock_data[1:]
    print(stock_data)
    S = 1e6
    c = 0.95
    mu = stock_data['returns'].mean()
    sigma = stock_data['returns'].std()
    print("VaR is: %.2f" % calculate_var(S, c, mu, sigma))
    plt.hist(stock_data['returns'], bins=60)
    plt.show()
