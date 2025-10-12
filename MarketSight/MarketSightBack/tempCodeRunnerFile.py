from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from alpaca.trading.client import TradingClient
import os





API_KEY = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')



owner_client =  TradingClient(API_KEY, SECRET_KEY)








