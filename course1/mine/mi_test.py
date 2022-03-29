import numpy as np
#from sklearn.metrics.cluster import  normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_mutual_info_score, mutual_info_score
import matplotlib.pyplot as plt


def calc_MI(x, y, bins=10):
    c_xy = np.histogram2d(x, y)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    return mi


x1 = np.random.rand(5000)

x2 =  np.random.randn(5000) #  np.random.rand(500)

a = calc_MI(x1, x2) #mutual_info_score(x1.tolist(), x2.tolist())

print(a)

#dist = np.histogram(x1)

#mi_score = calc_MI(x1, x2, 10)


plt.hist(x2, bins=20)
plt.show()
