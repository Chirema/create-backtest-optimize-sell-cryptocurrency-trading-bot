import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

BTCUSDT = pd.read_csv(
    'clean/data-spot-monthly-klines-BTCUSDT-1d',
    index_col=0, parse_dates=True, infer_datetime_format=True
)

if __name__ == "__main__":

    class SmaCross(Strategy):
        def init(self):
            price = self.data.Close
            self.ma1 = self.I(SMA, price, 33)
            self.ma2 = self.I(SMA, price, 55)

        def next(self):
            if crossover(self.ma1, self.ma2):
                self.buy()
            elif crossover(self.ma2, self.ma1) and self.position.pl > 0:
                self.sell()


    bt = Backtest(
        BTCUSDT, SmaCross, commission=.002, exclusive_orders=True, cash=100000
    )

    output = bt.run()
    bt.plot()

    print(output)
