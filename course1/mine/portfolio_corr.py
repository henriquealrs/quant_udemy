import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import numpy as np
import scipy.cluster.hierarchy as spc
from sklearn.cluster import KMeans

n_groups = [3, 4, 5, 6]

# tickers = ['AAPL',  'MSFT', 'DPZ', 'CMG', 'EGIE3.SA']
tickers = [ 'SLCE3.SA',
            'ITUB3.SA',
            'ITSA3.SA',
            'KLBN4.SA',
            'WEGE3.SA',
            'EGIE3.SA',
            'B3SA3.SA',
            'AGRO3.SA',
            'ARZZ3.SA',
            'LEVE3.SA',
            'ABEV3.SA',
            'VIVA3.SA',
            'YDUQ3.SA',
            'PETZ3.SA',
            'TOTS3.SA',
            'SQIA3.SA',
            'LOGG3.SA',
            'FLRY3.SA',
            'RADL3.SA'
            ]

# ['AAPL',  'MSFT', 'DPZ', 'CMG', 'EGIE3.SA']

start = dt.datetime(2020, 1, 1)

data = pdr.get_data_yahoo(tickers, start)
data = data['Adj Close']

data = data.resample('M').last()

log_returns = np.log(data / data.shift())[1:]

# print(log_returns)
corr_pd = log_returns.corr()
print(corr_pd)
corr = corr_pd.values



for ng in n_groups:
    print("\n\nFor %d groups" % ng)
    kmeansClass = KMeans(n_clusters = ng, init='k-means++')
    kmeansClass.fit(corr)
    groups = [kmeansClass.predict(col.reshape(1,-1)) for col in corr]
    sprint = []
    for i in range(ng):
        sprint.append("")

    for i in range(len(tickers)):
        t = tickers[i]
        sprint[groups[i][0]] = sprint[groups[i][0]] + t + ", "

    for i in range(len(sprint)):
        s = sprint[i]
        print("in group %d\n\t%s" %(i, s))
#print(kmeansClass)

#knnClass.fit(corr)

#pdist = spc.distance.pdist(corr)
#linkage = spc.linkage(pdist, method='complete')
#idx = spc.fcluster(linkage, 0.5*pdist.max(), 'distance')
#print(idx)