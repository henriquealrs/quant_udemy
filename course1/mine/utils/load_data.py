from threading import Thread
from queue import Queue
from datetime import date
import yfinance as yf
import pandas as pd


class Worker(Thread):
    def __init__(self, stocks_queue: Queue, start_date, end_date):
        Thread.__init__(self)
        self.q = stocks_queue
        self.results = {}
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        while not self.q.empty():
            stock = self.q.get()
            if stock == '':
                break
            ticker = yf.Ticker(stock)
            self.results[ticker] = ticker.history(start=self.start_date, end=self.end_date)['Close']


def download_data(stocks_list: list, start_date: str, no_workers: int=4) -> pd.DataFrame:
    stock_data = {}
    end_date = date.today().strftime("%Y-%m-%d")
    # filePathStr = './data/' + end_date
    # path = Path(filePathStr)
    #
    # if path.is_file():
    #     ret = pd.read_csv(path, header=1)
    #     ret.drop(columns=ret.columns[0], axis=1, inplace=True)
    #     return ret
    q = Queue()
    for stock in stocks_list:
        q.put(stock)

    workers = [Worker(q, start_date, end_date) for _ in range(no_workers)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    print("All joined")
    d = {}
    for w in workers:
        d = {**d, **w.results}
    ret = pd.DataFrame(d)
    # ret.to_csv(path)

    return ret  # pd.DataFrame(d)
