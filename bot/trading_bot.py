
#Trading Dependencies 
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST 
from timedelta import Timedelta 

#Other dependencies 
import numpy as np


class AITrader(Strategy):
    """
    This class is the baseline of the bot in order to complete all the trading required. 
    """

    def initialize(self, 
                   assets:list = [], 
                   risk:float = 0.5, 
                   BASE_URL:str = "",
                   API_KEY:str = "",
                   API_SECRET:str = ""):

        self.BASE_URL = BASE_URL
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET

        """
        if (not self.BASE_URL) and (not self.API_KEY) and (not self.API_SECRET):
            print('(*******************)')
            print("HERE")
            print('(*******************)')
            self.data_api = REST(base_url=self.BASE_URL, key_id=self.API_KEY, secret_key=self.API_SECRET)
        else:
            raise ValueError("Missing the API")
        """
        self.risk = risk
        self.assets = assets
        self.sleeptime = "24H"
        self.last_trade = None
       

    def position_sizing(self):

        """
        This function will return the position size wanting to be taken on a particular asset, set in the
        self.market variable 
        
        """

        cash = self.get_cash()
        if len(self.assets) == 0:
            raise ValueError("No assets selected")
        else:
            prices = np.array(self.get_last_prices(self.markets))
            quantities = np.floor((cash * self.risk)/prices)
        
        return cash, prices, quantities
    
    def on_trading_iteration(self):
        """
        Performing the trading iterations, based on the sleep time, set in self.sleep_time
        """
        cash, last_prices, quantities = self.position_sizing() # Find the position size for the markets selected
        for i in range(len(last_prices)):
            #create the order
            if cash > last_prices[i]:
                order = self.create_order(
                    asset=self.assets,
                    quantity=quantities[i],
                    side="buy",
                    take_profit_price=last_prices[i]*1.2,
                    stop_loss_price=last_prices[i]*0.95
                )
                #submit the order
                self.submit_order(order)

if __name__ == "__main__":
    pass




        


        

