import os
from logging import getLogger

import pandas as pd
from backtesting.lib import crossover
from backtesting.test import SMA
from investing_algorithm_framework import App, AlgorithmContext, OHLCV, Ticker

logger = getLogger(__name__)

app = App(
    resource_directory=os.path.abspath(
        os.path.join(os.path.realpath(__file__), os.pardir)
    ),
    config={
        "PORTFOLIOS": {
            "PRODUCTION_PORTFOLIO": {
                "API_KEY": "<YOUR_API_KEY>",
                "SECRET_KEY": "<YOUR_SECRET_KEY>",
                "TRADING_SYMBOL": "USDT",
                "MARKET": "BINANCE",
                "SQLITE": False
            }
        }
    }
)


def get_simple_moving_average(data_frame, amount_of_days=50):
    return SMA(data_frame.close, amount_of_days)


# Our strategy runs every 5 minutes and receives OHLCV data from binance
# It gets 100 '1d' data points, enough to create our 35 and 55 SMA's.
@app.algorithm.strategy(
    time_unit="SECOND",
    interval=5,
    market="BINANCE",
    target_symbol="BTC",
    trading_symbol="USDT",
    trading_data_types=["OHLCV", "TICKER"],
    trading_time_unit="ONE_DAY",
    limit=100
)
def perform_strategy(context: AlgorithmContext, ticker: Ticker, ohlcv: OHLCV):
    # Convert the ohlcv data to a pandas df
    df = pd.DataFrame.from_dict(ohlcv.to_dict(date_format="%Y-%m-%d"))

    # Create 33 and 55 SMA's
    sma_one = get_simple_moving_average(df, amount_of_days=33)
    sma_two = get_simple_moving_average(df, amount_of_days=55)

    # Check your portfolio positions
    position = context.get_position("BTC")
    unallocated = context.get_unallocated()

    # We have no open position for BTC/USDT, check if we need to buy
    if position.get_amount() == 0 and crossover(sma_one, sma_two):

        logger.info("Found buying cross")

        # At least 100 USDT needs to be present in the portfolio
        if unallocated.get_amount() > 100:
            # We open a position with 50 % of our portfolio
            amount_trading_symbol = unallocated.get_amount() / 2

            logger.info(f"Opening position BTC with {amount_trading_symbol}")

            context.create_limit_buy_order(
                "BTC",
                ticker.get_price(),
                amount_trading_symbol=unallocated.get_amount() / 2,
                execute=False
            )

    # Check if we have an open position on BTC/USDT and if we need to sell
    elif position.get_amount() > 0 and crossover(sma_two, sma_one):
        context.create_limit_sell_order(
            "BTC",
            ticker.get_price(),
            amount_target_symbol=position.get_amount(),
            execute=False
        )


if __name__ == "__main__":
    # Run the trading bot
    app.start(stateless=True)

