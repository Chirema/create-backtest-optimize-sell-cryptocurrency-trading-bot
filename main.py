import os
import time
from os.path import isdir

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


OUTPUT_DIR = 'result'


def visualise(df):
    plt.style.use('classic')

    x = df["ma1"]
    y = df["ma2"]

    # size and color:
    sizes = df["Result"]
    colors = df["Result"]

    # plot
    fig, ax = plt.subplots()

    ax.scatter(x, y, s=sizes, c=colors)

    plt.show()


def visualize_two(df):
    x = df["ma1"]
    y = df["ma2"]
    z = df["Result"]
    levels = np.linspace(z.min(), z.max(), 50)

    # plot:
    fig, ax = plt.subplots()

    ax.plot(x, y, 'o', markersize=2, color='grey')
    ax.tricontourf(x, y, z, levels=levels)

    plt.show()


def generate_backtest_variables():
    from itertools import product
    ma1 = np.arange(1, 20, 1)
    ma2 = np.arange(1, 100, 1)
    df = pd.DataFrame(list(product(ma1, ma2)), columns=['ma1', 'ma2'])
    df['result'] = 0
    return df


def save(df_result):
    if not isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    df_result.to_csv(f"{OUTPUT_DIR}/{time.strftime('%Y%m%d-%H%M%S')}.csv")


def run_btcusdt():

    df_result = generate_backtest_variables()

    for index, row in df_result.iterrows():

        print(f"{index}/{len(df_result)}")

        result = backtest(row["ma1"], row["ma2"])
        df_result.at[index, 'result'] = result

    save(df_result)


def backtest(ma1, ma2):

    BTCUSDT = pd.read_csv(
        'clean/data-spot-monthly-klines-BTCUSDT-1d',
        index_col=0, parse_dates=True, infer_datetime_format=True
    )

    class SmaCross(Strategy):
        def init(self):
            price = self.data.Close
            self.ma1 = self.I(SMA, price, ma1)
            self.ma2 = self.I(SMA, price, ma2)

        def next(self):
            if crossover(self.ma1, self.ma2):
                self.buy()
            elif crossover(self.ma2, self.ma1):
                self.sell()

    bt = Backtest(BTCUSDT, SmaCross, commission=.002, exclusive_orders=True)
    stats = bt.run()

    result = stats["Return [%]"]
    return result


if __name__ == '__main__':
    run_btcusdt()

    # df = pd.read_csv("result/20220207-124134.csv")
    # visualize_two(df)
