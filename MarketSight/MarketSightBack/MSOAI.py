from alpaca.trading.client import TradingClient
from alpaca.data.historical  import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca_trade_api.rest import REST




from anthropic import AnthropicVertex
from alpaca.common.exceptions import APIError # This is to ensure to check stocks (which will lead to API Error when a Stock is not valid)
import os
from dotenv import load_dotenv
from anthropic import Anthropic

from yahooquery import Ticker

import pandas as pd

load_dotenv()



API_KEY = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')


CLAUDE = os.getenv('CLAUDE')


alpaca_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY)





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
    financial_data = stock.financial_data.get
    financial_data = stock.financial_data.get(symbol, {})
    return financial_data



def StockSummary(stock: str) -> str:
    stock = stock.upper()
    # Check if stock exist,  if it deos pass response and return it
    if check_stock(stock):
        information_of_stock = StockInfo(stock)
        financial_info = client.messages.create(
            model=MODEL_AI,
            max_tokens=int(MAX_TOKENS),
            messages=[
                {"role": "user", 
                 "content": f"Summarize  stock information {information_of_stock} and the updates it should have such as that it has it properly formmated such as that we're able to have it organized prompt, and we want it to be formmated and useable in Django (NO CODE, BUT THIS IS  A REFERENCE TO JUST FORMAT IT HAHA. DO NOT ADD THE REMAINING FORMALITY, JUST ADD INFORMATION ONLY!). What does the stock infomration entail the company and what should investors do when investing in {stock}. Format it in a way that is good for Django (Do not write code, just format the words and summary really well that it's compatible in HTML). Using the information in {information_of_stock} Please generate it such as that it's organized that would fit as a paragraph in django, and I want it to be really great formatted. So whatever you had in the {information_of_stock} Will be formatted perfectly with the best of your ability, just add it and no formalities... Make sure it's detailed and dumb down for retail investors such as I in what information entails per each subject and how does it impact future growth and stock. Make sure the information is DUMBED enough for retail investors, why is it important, etc. Ensure that infomration is detailed for each subject such as Profitability Metrics, etc "}
            ],
        )

            # Create a max tokens for users, MAKE SURE TO ADD THE MAX TOKEN VALUE IN ENV
        return financial_info.content[0].text.strip()
    else:
        return f"The Stock {stock} Does not Exist, Please Try Again!"
    


    
    

def news(stock: str) -> str:
    stock = stock.upper()
    api_rest = REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

    news_article = api_rest.get_news(symbol=stock, start="2025-10-01", end="2025-10-31", include_content=True)

    # Empty dict that will be appended

    news_info = {}

    for articles in news_article:
        news_info['Headline'] = f"{articles.headline}"
        news_info['Content']= f"{articles.content}"
    

    return news_info







print(StockSummary('AAPL'), news('AAPL'))
