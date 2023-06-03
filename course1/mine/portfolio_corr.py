import pandas as pd
# import pandas_datareader as pdr
import datetime as dt
import numpy as np
import scipy.cluster.hierarchy as spc
from sklearn.cluster import KMeans
from mi_test import calc_MI
from utils.load_data import download_data
from sklearn.feature_selection import mutual_info_regression
from utils.print import * # pretty_print, prinf_diag_diff
from pyinform.mutualinfo import mutual_info


n_groups_arr = [3, 4, 5, 6]
N_GROUPS = 4

# tickers = ['AAPL',  'MSFT', 'DPZ', 'CMG']
tickers = ['ITUB3.SA',
           'BBDC4.SA',
           'flry3.sa',
           'slce3.sa',
           'itsa3.sa',
           'klbn4.sa',
           'wege3.sa',
             # 'egie3.sa',
             # 'b3sa3.sa',
             'AGRO3.SA',
             # 'ARZZ3.SA',
             # 'LEVE3.SA',
             # 'ABEV3.SA',
             # 'VIVA3.SA',
             # 'YDUQ3.SA',
             # 'TOTS3.SA',
             # 'SQIA3.SA',
             # 'LOGG3.SA',
           'RADL3.SA'
           ]

# ['AAPL',  'MSFT', 'DPZ', 'CMG', 'EGIE3.SA']

start = dt.datetime(2020, 1, 1).strftime("%Y-%m-%d")

# data = pdr.get_data_yahoo(tickers, start)
# data = data['Adj Close']
data: pd.DataFrame = download_data(tickers, start)

# data = data.resample('M').last()
log_returns = np.log(data / data.shift())[1:]

# mi = mutual_info_regression(log_returns.iloc[:,0].values.reshape(-1,1), log_returns.iloc[:,1].values)
# print(f"Mutual information: {mi}")


n_cols = len(log_returns.columns)
mutual_info_matrix = np.zeros((n_cols, n_cols))
for i in range(n_cols):
    for j in range(n_cols):
        # if i == j:
        #     mutual_info_matrix[i][j] = 9999
        #     continue
        mutual_info_matrix[i,j] = mutual_info_regression(log_returns.iloc[:, i].values.reshape(-1,1), log_returns.iloc[:,j].values)
print_MI(mutual_info_matrix, tickers)
# pretty_print(mutual_info_matrix)
print(type(mutual_info_matrix))
exit()

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
