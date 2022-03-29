import numpy.random as npr
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

def weiner_process(dt=0.1, x0=0, n=1000):
    #initialize W(t) with 0
    W = np.zeros(n+1)
    t = np.linspace(x0, n, n+1)
    W[1:n+1] = np.cumsum(npr.normal(00, sqrt(dt), n))
    plt.plot(W)
    plt.show()
    return t,W

def plot_weiner_process(t, W):
    plt.plot(t, W)
    # plt.plot(t, np.sqrt(np.sqrt(t)))
    plt.show()
    return


def simulate_geometric_random_walk(S0, T=2, N=1000, mu=0.1, sigma=0.05):
    dt = T/N
    t = np.linspace(0, T, N);
    W = np.random.standard_normal(size=N)
    W = np.cumsum(W)  * np.sqrt(dt)
    X = (mu - 0.5 * sigma * sigma) * t + sigma * W
    S = S0 * np.exp(X)
    plt.plot(t, S)
    plt.show()

if __name__ == '__main__':
    #t,W = weiner_process()
    #plot_weiner_process(t, W)
    simulate_geometric_random_walk(10)