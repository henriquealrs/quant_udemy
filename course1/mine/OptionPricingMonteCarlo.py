import numpy as np
import matplotlib.pyplot as plt

class OptionPricing:
    def __init__(self, S0, E, T, rf, sigma, iterations):
        self.S0 = S0
        self.E = E
        self.T = T
        self.rf = rf
        self.sigma = sigma
        self.iterations = iterations

    def call_option_simulation(self):
        options = np.zeros([self.iterations, 2])
        # print(options)
        rand = np.random.normal(0, 1, [1,self.iterations])
        stock_price = self.S0 * np.exp(self.T * (self.rf - 0.5*self.sigma*self.sigma) +
                                          self.sigma * np.sqrt(self.T) * rand)
        options[:,1] = stock_price - self.E
        average = np.amax()

if __name__ == "__main__":
    model = OptionPricing(100, 100, 1, 0.005, 0.02, 500)
    model.call_option_simulation()