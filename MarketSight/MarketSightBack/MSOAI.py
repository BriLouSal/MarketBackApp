from alpaca.trading.client import TradingClient
from anthropic import AnthropicVertex
from alpaca.common.exceptions import APIError
import os
from dotenv import load_dotenv
from anthropic import Anthropic

from yahooquery import Ticker




load_dotenv()



API_KEY = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')


CLAUDE = os.getenv('CLAUDE')


alpaca_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY)


# First we need to check if stock exists, using the library from Alpaca, we can raise API error



# def stock(symbol: str):

#     request_param = StockTradesRequest(   )






client = Anthropic(api_key=CLAUDE)

MODEL_AI = "claude-sonnet-4-5"

MAX_TOKENS = os.getenv('MAX_TOKENS')


tools = {}

def check_stock(stock: str):
    try:
        asset = alpaca_client.get_asset(stock.capitalize())
        if asset:
            return f"The stock {stock} exists!"
        else:
            return f"The stock: {stock}, does not exist! Please Try Again"
    

    except APIError as e:
        # We can have an if-statement on
        return False
# I want to create a summary of the stock 

# MUST BE A STRING
def StockInfo(symbol: str):
    # First check stock
    symbol = symbol.capitalize
    stock = Ticker([symbol])
    financial_data = stock.financial_data.get(symbol, {})
    return financial_data


def StockSummary(stock: str):
    response = client.messages.create(
        model=MODEL_AI,
        max_tokens=int(MAX_TOKENS),
        messages=[
            {"role": "user", "content": f"Summarize {StockInfo(stock.capitalize())} stock information and the updates it should have such as that "}
        ],
    )
        # Create a max tokens for users, MAKE SURE TO ADD THE MAX TOKEN VALUE IN ENV
    return response







print(StockSummary('AAPL'))
