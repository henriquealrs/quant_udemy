import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NUM_OF_SIMULATIONS = 1000

def stock_monte_carlo(S0, mu, sigma, N=1000):
    r_shape = (N+1,NUM_OF_SIMULATIONS)
    result = np.empty(r_shape)
    for j in range(NUM_OF_SIMULATIONS):
        result[0][j] = S0
        for i in range(1,N+1):
            result[i][j] = result[i-1][j] * np.exp((mu - 0.5 * sigma*sigma) + sigma * np.random.normal())

    simulation_data = pd.DataFrame(result)
    simulation_data['mean'] = simulation_data.mean(axis=1)
    plt.plot(simulation_data['mean'])
    # plt.show()

if __name__ == "__main__":

    for _ in range(10):
        stock_monte_carlo(50, 0.0002, 0.01, 255)
    plt.show()
