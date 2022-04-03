import pandas as pd
from matplotlib import pyplot as plt
from skopt.plots import plot_objective
from backtesting import Strategy, Backtest
from backtesting.lib import crossover
from backtesting.test import SMA


class SmaCross(Strategy):
    n1 = 50
    n2 = 100

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, self.n1)
        self.ma2 = self.I(SMA, price, self.n2)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1) and self.position.pl > 0:
            self.sell()


BTCUSDT = pd.read_csv(
    'clean/data-spot-monthly-klines-BTCUSDT-1d',
    index_col=0, parse_dates=True, infer_datetime_format=True
)


if __name__ == "__main__":

    bt = Backtest(
        BTCUSDT,
        SmaCross,
        commission=.002,
        exclusive_orders=True,
        cash=100000
    )

    stats_skopt, heatmap, optimize_result = bt.optimize(
        n1=[10, 100],  # Note: For method="skopt", we
        n2=[20, 200],  # only need interval end-points
        maximize='Equity Final [$]',
        method='skopt',
        max_tries=200,
        random_state=0,
        return_heatmap=True,
        return_optimization=True)

    _ = plot_objective(optimize_result, n_points=10)

    # print(heatmap.sort_values().iloc[-3:])
    # print(heatmap.sort_values().iloc[-1:])
    # print(heatmap.sort_values().iloc[-1:].index)

    # n1
    print(heatmap.sort_values().iloc[-1:].index.get_level_values('n1')[0])

    # n2
    print(heatmap.sort_values().iloc[-1:].index.get_level_values('n2')[0])

    plt.show()
