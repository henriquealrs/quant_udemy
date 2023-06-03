import numpy as np
#from sklearn.metrics.cluster import  normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_mutual_info_score, mutual_info_score
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def calc_MI(x, y, bins=10):
    c_xy = np.histogram2d(x, y, bins)[0]
    # plt.hist(x, bins=bins)
    # plt.hist(y, bins=bins)
    # plt.show()
    mi = mutual_info_score(None, None, contingency=c_xy)
    return mi

if __name__ == '__main__':
    x1 = np.random.randn(5000)
    x2 = 0.2 * np.random.randn(5000) + 0.8*x1
    a = calc_MI(x1, x2) #mutual_info_score(x1.tolist(), x2.tolist())
    print(a)
