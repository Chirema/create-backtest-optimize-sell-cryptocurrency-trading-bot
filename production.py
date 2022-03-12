import decimal
import math
from datetime import datetime

import requests
from eltyer import Client, OrderSide
import pandas as pd
from backtesting.test import SMA
from backtesting.lib import crossover

# OrderSide!!!
# find profit of current position
# get max amount to buy


def get_real_time_klines(target_symbol, trading_symbol, interval = "1d", limit = 100):
    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
    response = requests.get(
        f"https://api.binance.com/api/v3/klines?symbol={target_symbol}"
        f"{trading_symbol}&interval={interval}&limit={100}"
    )
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "Open time", "Open", "High", "Low", "Close", "Volume", "Close time",
        "Quote asset volume", "Number of trades", "Taker buy base asset volume",
        "Taker buy quote asset volume", "Ignore"
    ])

    df = df.drop([
        "Open time", "Open", "High", "Low", "Volume",
        "Quote asset volume", "Number of trades", "Taker buy base asset volume",
        "Taker buy quote asset volume", "Ignore"
    ], axis=1)  # drop all except "Close" and "Close time"

    df["Close time"] = pd.to_datetime(df['Close time'], unit='ms')
    df = df.set_index("Close time")
    return df


if __name__ == "__main__":

    target_symbol = "BTC"
    trading_symbol = "USDT"

    client = Client()
    client.config.API_KEY = "9Lco7s6fMNO6qILTABeAG01xtnAVSDOjlWzWxF1Sl8BmDGxASNrDgETH4uzC4BXh"
    client.start()

    # BTCUSDT = pd.read_csv(
    #     'clean/data-spot-monthly-klines-BTCUSDT-1d',
    #     index_col=0, parse_dates=True, infer_datetime_format=True
    # )

    BTCUSDT = get_real_time_klines(target_symbol, trading_symbol)
    price = BTCUSDT.Close
    ma1 = SMA(price, 33)
    ma2 = SMA(price, 55)

    last_closing_price = price[-1]

    def get_minimal_amount_step_size(target_symbol, trading_symbol):
        # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#exchange-information
        # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#lot_size
        response = requests.get(url="https://api.binance.com/api/v3/exchangeInfo?symbol=BTCUSDT")
        data = response.json()
        filters = data['symbols'][0]['filters']
        amount_filter = next(filter for filter in filters if filter["filterType"] == "LOT_SIZE")
        return float(amount_filter['minQty'])

    def buy(symbol):

        def get_decimal_places_of_number(number):
            d = decimal.Decimal(str(number))
            return -d.as_tuple().exponent

        def floor_amount(amount, decimals):
            factor = 10 ** decimals
            return math.floor(amount * factor) / factor

        def max_amount_to_buy(price):
            portfolio = client.get_portfolio()
            unallocated = portfolio.unallocated
            theoretical_max_amount = unallocated / price
            minimal_amount = get_minimal_amount_step_size(
                target_symbol, trading_symbol
            )
            decimals = get_decimal_places_of_number(minimal_amount)
            valid_amount = floor_amount(theoretical_max_amount, decimals)
            print(valid_amount)
            return valid_amount

        client.create_limit_order(
            target_symbol=symbol,
            price=last_closing_price,
            amount=max_amount_to_buy(last_closing_price),
            side=OrderSide.BUY.value
        )

    def sell(symbol):
        position = client.get_position(symbol)

        client.create_limit_order(
            target_symbol=symbol,
            price=last_closing_price,
            amount=position.amount,
            side=OrderSide.SELL.value
        )

    def valid_buy(symbol):

        def no_open_buy_order(symbol):
            order_states = [
                "TO_BE_SENT",
                "PENDING"
            ]

            for order_state in order_states:
                orders = client.get_orders(
                    target_symbol=symbol, status=order_state
                )

                if len(orders) > 0:
                    return False

            return True

        def no_open_position(symbol):
            position = client.get_position(symbol)
            if position:
                if position.amount > 0:
                    return False

            return True

        return no_open_buy_order(symbol) and no_open_position(symbol)

    def valid_sell(symbol):

        def profit_made(symbol):
            orders = client.get_orders(
                target_symbol=symbol, status="SUCCESS"
            )

            last_completed_buy_order = next(
                (o for o in orders if o.side == OrderSide.BUY), None
            )

            if last_completed_buy_order:
                buying_price = last_completed_buy_order.initial_price

                if last_closing_price > buying_price:
                    return True

            return False

        def position_open(symbol):
            position = client.get_position(symbol=symbol)
            if position and position.amount > 0:
                return True

            return False

        return profit_made(symbol) and position_open(symbol)

    if crossover(ma1, ma2) & valid_buy(target_symbol):
        print("Buy")
        buy(target_symbol)
    elif crossover(ma2, ma1) & valid_sell(target_symbol):
        print("Sell")
        sell(target_symbol)
    else:
        print("No action")

    client.stop()
