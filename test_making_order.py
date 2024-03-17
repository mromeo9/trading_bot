from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST 
from timedelta import Timedelta 

#class for the trader 
from bot.trading_bot import AITrader

"""
Basic tester created for quick testing 

"""

BASE_URL = "https://paper-api.alpaca.markets/v2"
API_KEY = "PKWGMFYLO82Q6VAM0F8Y"
API_SECRET = "5VI04IG0OzOfQSoS7aXXj6gPUnoyRhqSvfgcIkWD"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

start_date = datetime(2024,1,15)
end_date = datetime(2024,1,31) 
broker = Alpaca(ALPACA_CREDS) 
strategy = AITrader(name='mlstrat', 
                    broker=broker, 
                    parameters={"assets":["SPY"], 
                                "risk":.5,
                                "BASE_URL":BASE_URL,
                                "API_KEY":API_KEY,
                                "API_SECRET":API_SECRET})
strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters={"assets":["SPY"], 
                "risk":.5,
                "BASE_URL":BASE_URL,
                "API_KEY":API_KEY,
                "API_SECRET":API_SECRET}
)
