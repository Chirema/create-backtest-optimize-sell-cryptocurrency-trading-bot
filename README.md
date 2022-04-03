#How to create, backtest, optimize and sell a cryptocurrency trading bot 

This is the repository for the medium articles ["How to create, backtest, optimize and sell a cryptocurrency trading bot"](https://medium.com/p/21e0ec3abdcf).

## Getting Started
Make sure that you install all the requirements of the project and download 
all the training data for the testing and optimization of your trading bot.

### Installing the dependencies
`pip install -r requirements.txt`

### Downloading Binance OHLCV data

`python download-kline.py`

## Creating a trading bot
This part belongs to the following medium article: ["How to create, backtest, optimize and sell a cryptocurrency trading bot (1/4)"](https://medium.com/p/21e0ec3abdcf).

### Running with arguments
| Argument        | Explanation |         
| --------------- | ---------------- |
| -h              | show help messages| 
| -s              | Single **symbol** or multiple **symbols** separated by space | 
| -y              | Single **year** or multiple **years** separated by space| 
| -m              | Single **month** or multiple **months** separated by space | 
| -d              | single **date** or multiple **dates** separated by space    | 
| -startDate      | **Starting date** to download in [YYYY-MM-DD] format    | 
| -endDate        | **Ending date** to download in [YYYY-MM-DD] format     | 
| -folder         | **Directory** to store the downloaded data    | 
| -c              | 1 to download **checksum file**, default 0       | 
| -i              | single kline **interval** or multiple **intervals** separated by space      |
| -t              | Trading type: **spot**, **um** (USD-M Futures), **cm** (COIN-M Futures)    |

e.g download ETHUSDT BTCUSDT BNBBUSD kline of 1 week interval from year 2020, month of Feb and Dec with CHECKSUM file:<br/>
`python3 download-kline.py -s ETHUSDT BTCUSDT BNBBUSD -i 1w -y 2020 -m 02 12 -c 1`

e.g. download ETHUSDT kline from 2020-01-01 to 2021-02-02 to directory /Users/bob/Binance:<br/>
`python3 download-kline.py -s ETHUSDT -startDate 2020-01-01 -endDate 2021-02-02 -folder '/Users/bob/Binance'`

## Optimizing the test trading bot

## Making your trading bot production ready
This part belongs to the following medium article: ["How to create, backtest, optimize and sell a cryptocurrency trading bot (3/4)"](https://medium.com/p/21e0ec3abdcf).

For a production read trading bot production we use the [investing algorithm framework](https://investing-algorithm-framework.com).
The trading bot uses trading data from BINANCE and also has 
its portfolio configured with BINANCE. If you would like to use a different 
broker, we recommend you to visit the documentation page of the [investing algorithm framework](https://investing-algorithm-framework.com).

For this article, two trading bots are made. One with the [backtesting framework](https://pypi.org/project/Backtesting/)
and the other with plain python. 

Both have the same functionality and behavior, however in this way you can see that
you can mix and match different frameworks and libraries with your trading bot.

### Configuration
You must provide your (Binance) Broker api key and secret key in order to 
have a properly functioning trading bot.

In the "main.py" file of the production trading bot folder you must replace 
the template values of the portfolio definition.

Replace 'API_KEY' and 'SECRET_KEY' with your keys 
found at [Binance](https://binance.com)

#### Default configuration
```python
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
```

#### Production configuration

---
**NOTE**

The used values are dummy values.

---
```python
app = App(
    resource_directory=os.path.abspath(
        os.path.join(os.path.realpath(__file__), os.pardir)
    ),
    config={
        "PORTFOLIOS": {
            "PRODUCTION_PORTFOLIO": {
                "API_KEY": "7p6voD97MqAvtSktyyJqiSHg5aRj3aPZ733rUJhU",
                "SECRET_KEY": "7p6voD97MqAvtSktyyJqiSHg5aRj3aPZ733rUJhU",
                "TRADING_SYMBOL": "USDT",
                "MARKET": "BINANCE",
                "SQLITE": False
            }
        }
    }
)
```


### Production ready trading bot with the backtesting framework
The production ready trading bot made with the [backtesting framework](https://pypi.org/project/Backtesting/) can 
be found at the location:
```shell
/production/backtesting_framework
```

#### Starting the trading bot
You can start the trading bot by running:

```shell
python  production/backtesting_framework/main.py
```

### Production ready trading bot with own metrics
The production ready trading bot made with self-made metrics can 
be found at the location:
```shell
/production/base
```


## Sharing and selling your trading bot on ELTYER


## Authors

Parts of the code are based on https://github.com/binance/binance-public-data (MIT)

## License

MIT
