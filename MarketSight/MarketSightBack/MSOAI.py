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

def check_stock(stock: str) -> str:
    try:
        asset = alpaca_client.get_asset(stock.upper())
        if asset:
            return True
        else:
            return False
    

    except APIError as e:
        # We can have an if-statement on
        return False
# I want to create a summary of the stock 

# MUST BE A STRING
def StockInfo(symbol: str) -> str:
    # First check stock
    symbol = symbol.upper()
    stock = Ticker([symbol])
    financial_data = stock.financial_data.get(symbol, {})
    return financial_data


def StockSummary(stock: str) -> str:
    stock = stock.upper()
    # Check if stock exist,  if it deos pass response and return it
    if check_stock(stock):
        information_of_stock = StockInfo(stock)
        response = client.messages.create(
            model=MODEL_AI,
            max_tokens=int(MAX_TOKENS),
            messages=[
                {"role": "user", 
                 "content": f"Summarize  stock information {information_of_stock} and the updates it should have such as that it has it properly formmated such as that we're able to have it organized prompt, and we want it to be formmated and useable in Django (NO CODE, BUT THIS IS  A REFERENCE TO JUST FORMAT IT HAHA. DO NOT ADD THE REMAINING FORMALITY, JUST ADD INFORMATION ONLY!). What does the stock infomration entail the company and what should investors do when investing in {stock} "}
            ],
        )
            # Create a max tokens for users, MAKE SURE TO ADD THE MAX TOKEN VALUE IN ENV
        return response.content[0].text.strip()
    else:
        return f"The Stock {stock} Does not Exist, Please Try Again!"







print(type(StockSummary('AAPL')))
