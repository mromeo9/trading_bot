
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
        
        #Creating the API for the news 
        self.BASE_URL = BASE_URL
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET

        if (not self.BASE_URL) or (not self.API_KEY) or (not self.API_SECRET):
            raise ValueError("Missing the API")
        else:  
            self.data_api = REST(base_url=self.BASE_URL, key_id=self.API_KEY, secret_key=self.API_SECRET)
        
        #Setting the paramters 
        self.risk = risk
        self.assets = assets
        self.sleeptime = "24H"
        self.last_trade = None
       

    def position_sizing(self):

        """
        This function will return the position size wanting to be taken on a particular asset, set in the
        self.market variable 
        
        """
        quantities = []

        cash = self.get_cash()
        if len(self.assets) == 0:
            raise ValueError("No assets selected")
        else:
            prices = self.get_last_prices(self.assets) #returns a dictionary of assets with prices 
            for asset in prices:
                quantities.append(np.floor((cash * self.risk)/prices[asset]))
        
        return cash, prices, quantities
    
    def on_trading_iteration(self):
        """
        Performing the trading iterations, based on the sleep time, set in self.sleep_time
        """
        cash, last_prices, quantities = self.position_sizing() # Find the position size for the markets selected
        for i, asset in enumerate(last_prices):
            print("***************")
            print("cash: {}\nasset: {}\nquanities: {}\nlast price {}".format(cash,self.assets[i], quantities[i],last_prices[asset]))
            #create the order
            if cash > last_prices[asset]:
                order = self.create_order(
                    asset=self.assets[i],
                    quantity=quantities[i],
                    side="buy",
                    take_profit_price=last_prices[asset]*1.2,
                    stop_loss_price=last_prices[asset]*0.95
                )

                #submit the order
                self.submit_order(order)

if __name__ == "__main__":
    pass




        


        

