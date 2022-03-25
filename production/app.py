import os
from investing_algorithm_framework import App, AlgorithmContext


app = App(
    resource_directory=os.path.abspath(
        os.path.join(os.path.realpath(__file__), os.pardir)
    ),
)


def get_simple_moving_average_100_day(data_frame):
    pass


def get_simple_moving_average_50_day(data_frame):
    pass


def cross_over(sma_one, sma_two) -> bool:
    pass


# Our strategy runs every 5 minutes and receives OHLCV data from binance
# It gets 100 '1d' data points, enough to create our 35 and 55 SMA's.
@app.algorithm.strategy(
    time_unit="SECOND",
    interval=5,
    market="BINANCE",
    target_symbol="BTC",
    trading_symbol="USDT",
    trading_data_type="OHLCV",
    trading_time_unit="ONE_DAY",
    limit=100
)
def perform_strategy(context: AlgorithmContext, ohlcv):
    print(ohlcv)


if __name__ == "__main__":
    # Run the trading bot
    app.start()

