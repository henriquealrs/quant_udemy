from urllib.parse import parse_qs
import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization
from pathlib import Path
from datetime import date
from threading import Thread
import queue


stocks = ['GOOGL', 'TSLA', 'DIS', 'AMZN', 'CSCO', 'SQ', 'SBUX'] #, 'NVDA', 'DG', 'MNST', 'COST', 'MELI']

NUM_TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000

start_date = '2016-01-01'


def download_data(no_workers: int) -> pd.DataFrame :
    stock_data = {}
    end_date = date.today().strftime("%Y-%m-%d")
    filePathStr = './data/' + end_date
    path = Path(filePathStr)
    
    if path.is_file():
        ret = pd.read_csv(path, header=1)
        ret.drop(columns=ret.columns[0], axis=1, inplace=True)
        return ret 

    ret = None

    class Worker(Thread):
        def __init__(self, stocks_queue: queue.Queue):
            Thread.__init__(self)
            self.q = stocks_queue
            self.results = {}

        def run(self):
            while not self.q.empty():
                stock = self.q.get()
                if stock == '':
                    break
                ticker = yf.Ticker(stock)
                self.results[ticker] = ticker.history(start=start_date, end=end_date)['Close']
    
    q = queue.Queue()
    for stock in stocks:
        q.put(stock)
    
    workers = []
    for _ in range(no_workers):
        worker = Worker(q)
        worker.start()
        workers.append(worker)
    for w in workers:
        w.join()
    
    print("All joined")
    d = {}
    for w in workers:
        d = {**d, **w.results}

    
    ret = pd.DataFrame(d)
    ret.to_csv(path)

    return ret # pd.DataFrame(d)

def show_data(data: pd.DataFrame, log_daily_returns: pd.DataFrame):
    # data['MELI-1'] = log_daily_returns['MELI']
    # data['TSLA-1'] = log_daily_returns['TSLA']
    # data[['MELI','TSLA','MELI-1','TSLA-1']].plot(figsize=(10, 15))
    #log_daily_returns.plot(figsize=(10, 15))
    data.plot(figsize=(10,15))
    plt.show()

def calculate_return(data: pd.DataFrame):
    # shifted = data.shift(1)
    # ddata = data/shifted
    # log_return = np.log(ddata)
    log_return = np.log(data / data.shift(1))
    return log_return[1:]

def show_statistics(returns: pd.DataFrame):
    print("means: ", returns.mean() * NUM_TRADING_DAYS)
    print("cov: ", returns.cov() * NUM_TRADING_DAYS)
    return

def show_mean_and_covariance(returns: pd.DataFrame, weights):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS  
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))
    print("Expected portolio mean (return): ", portfolio_return)
    print("Expected portfolio volatility (standard deviation): ", portfolio_volatility)


def show_portfolios(returns, volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(volatilities, returns, c=returns / volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()


def show_portfolios_1(m: np.array, r: np.array):
    plt.figure(figsize=(10,6))
    plt.scatter(r, m, c=m/r, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel("Expected return")
    plt.colorbar(label="Sharpe ratio")
    plt.show()

def generate_portfolios(returns: pd.DataFrame):
    portfolio_means = []
    portfolio_risk = []
    portfolio_weights = []
    for _ in range(NUM_PORTFOLIOS):
        w = np.random.random(len(stocks))
        w = w / np.sum(w)
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean() * w) * NUM_TRADING_DAYS)
        portfolio_risk.append( 
            np.sqrt(    
                np.dot(w.T, 
                    np.dot(returns.cov() * NUM_TRADING_DAYS, w) 
                ) 
            )   
        )
        #print("For portfolio: ", stocks, "\n", w)
        #print("Means: ", portfolio_means[len(portfolio_means)-1])
        #print("Risk: ", portfolio_risk[len(portfolio_risk)-1])
    return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risk)


def statistics(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov()
                                                            * NUM_TRADING_DAYS, weights)))
    return np.array([portfolio_return, portfolio_volatility,
                     portfolio_return / portfolio_volatility])
    
def min_functions_sharpe(weights, returns):
    return -statistics(weights, returns)[2]

def optimize_portfolio(weights, returns):
    constraints = {'type' : 'eq',
                    'fun' : lambda x: np.sum(x)-1 }
    bounds = tuple((0, 1) for _ in range(len(stocks)))
    return optimization.minimize(fun=min_functions_sharpe, x0=weights[0], args=returns, method='SLSQP', bounds = bounds, constraints=constraints)


def print_optimal_portfolio(optimum, returns):
    print("Optimal portfolio: ", optimum['x'].round(3))
    print("Expected return, volatility and Sharpe ratio: ",
          statistics(optimum['x'].round(3), returns))


def show_optimal_portfolio(opt, rets, portfolio_rets, portfolio_vols):
    plt.figure(figsize=(10, 6))
    plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets / portfolio_vols, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.plot(statistics(opt['x'], rets)[1], statistics(opt['x'], rets)[0], 'g*', markersize=20.0)
    plt.show()


if __name__ == '__main__':
    data_set = download_data(5)
        
    log_daily_returns = calculate_return(data_set)
    # show_statistics(log_daily_returns)
    show_data(data_set, log_daily_returns)

    pweights, means, risks = generate_portfolios(log_daily_returns)
    show_portfolios(means,risks)
    optimum = optimize_portfolio(pweights, log_daily_returns);
    print_optimal_portfolio(optimum, log_daily_returns)
    show_optimal_portfolio(optimum, log_daily_returns, means, risks)

