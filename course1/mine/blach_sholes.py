from scipy import stats
from numpy import exp, log, sqrt
import yfinance as yf
import pandas as pd

def call_option_price(S, E, T, rf, sigma):
    d1 = log(S/E) + (rf + sigma*sigma/2)*T/(sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    print("(d1, d2) = (%s,%s)" % (d1, d2))

    # Use the N(x), to calculate the price of the option
    return S * stats.norm.cdf(d1) - E*exp(-rf * T)*stats.norm.cdf(d2)

def put_option_price(S, E, T, rf, sigma):
    d1 = log(S/E) + (rf + sigma*sigma/2)*T/(sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    print("(d1, d2) = (%s,%s)" % (d1, d2))

    # Use the N(x), to calculate the price of the option
    return -S * stats.norm.cdf(-d1) + E*exp(-rf * T)*stats.norm.cdf(-d2)

if __name__ == "__main__":
    S0 = 100
    E = 100
    T = 1
    rf = 0.05
    sigma = 0.2
    print("Call price :%s\n Put price: %s" % (call_option_price(S0,E,T,rf,sigma), put_option_price(S0,E,T,rf,sigma)))