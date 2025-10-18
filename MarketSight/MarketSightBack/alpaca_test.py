from alpaca.trading.client import TradingClient

import alpaca_trade_api as tradeapi


from MSOAI import StockSummary, StockInfo

from dotenv import load_dotenv
import os

from trading_classes import get_asset_info
# This primarily to test my algorithim by adding into my Paper Traeding Simulator

# Load our env files
load_dotenv()


ALPACA = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')



# This is my account for experimental stuff such as using paper trading in order
# to experiment with my algorithims
trading_client = TradingClient(api_key=ALPACA, secret_key=SECRET_KEY)

# This is the main api
trading_api = tradeapi.REST(key_id=ALPACA, secret_key=SECRET_KEY)





account = trading_client.get_account()

print(type(account))



print(get_asset_info)