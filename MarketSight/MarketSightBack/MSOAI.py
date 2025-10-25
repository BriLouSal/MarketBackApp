from alpaca.trading.client import TradingClient
from anthropic import Anthropic
from alpaca.common.exceptions import APIError
import os
from dotenv import load_dotenv




load_dotenv()



API_KEY = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')


CLAUDE = os.getenv('CLAUDE')


alpaca_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY)


# First we need to check if stock exists, using the library from Alpaca, we can raise API error



# def stock(symbol: str):

#     request_param = StockTradesRequest(   )






client = Anthropic(api_key=CLAUDE)

model_of_ai = "claude-3-5-sonnet-20240620"

MAX_TOKENS = os.getenv('MAX_TOKENS')


tools = {
    
}

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


def StockSummary():
    response = client.messages.create(model= model_of_ai,
                                    max_tokens= MAX_TOKENS,    
                                    messages=[{"role":"user","content":"Summarize AAPL stock news"}],
        # Create a max tokens for users, MAKE SURE TO ADD THE MAX TOKEN VALUE IN ENV
    )







