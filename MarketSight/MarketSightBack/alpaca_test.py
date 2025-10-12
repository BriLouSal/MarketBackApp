from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
import os




load_dotenv()



API_KEY = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')

print(API_KEY, SECRET_KEY)



# trading_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY, paper=True)




# print(trading_client)



