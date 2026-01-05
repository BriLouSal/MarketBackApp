
# Main Django library

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm



# User authentication library from Django


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
# Used for Performance
from django.core.cache import cache

from .backend import EmailBackend

# # Error checker
# import sys
# print(sys.executable)
# # email

from django.core.mail import send_mail
from django.conf import settings


from functools import cache
# Investment Endeavors Library

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus

from datetime import datetime
from yahooquery import Ticker, search



from django.contrib import messages

import pandas as pd
import matplotlib.pyplot as pl





import markdown


from .models import Profile, Portfolio
# from alpaca.data.historical import CryptoHistoricalDataClient

from .MSOAI import (
    FinancialReport,
    Company_Analysis,
    Revenue_Analysis,
    Returns_Efficiency_Ratios,
    Growth_Analysis_Outlook,
    Growth_of_Stock,
    Company_Debt,
    StockInfo,
    html_to_paragraph_text,
    news

    
    
)
# Performance
from asgiref.sync import sync_to_async, async_to_sync
import asyncio
from django.core.cache import cache


# Stock backup (INCASE IT'S NEEDED FOR VIEWS.PY IN ORDER FOR IT TO BE SEAMLESS)
import yfinance as yf
import yahooquery as yq
import ta


import json
import os 
from dotenv import load_dotenv




load_dotenv()






#  This is the views.py file where we will handle the logic for our application
#  We will create views for home, portfolio room, stock, login, signup, and assistance

user = "Brain"


#  This is a list of stocks that we will use to display in the portfolio room
ticker = []

# This will be used as a feature to store recent_search of a user stock
recent_search = {}

def news_parser(stock: str):
    # News gives an output for html tags
    pass





async def build_stock_analyzer(stock_url, info) -> dict:
    cache_key = f"analysis:{stock_url}"
    
    
    cached = cache.get(cache_key)
    if cached:
        return cached

    
    stock_info = await asyncio.gather(
        sync_to_async(FinancialReport)(stock_url, info),
        sync_to_async(Company_Analysis)(stock_url, info),
        sync_to_async(Revenue_Analysis)(stock_url, info),
        sync_to_async(Growth_Analysis_Outlook)(stock_url, info),
        sync_to_async(Growth_of_Stock)(stock_url, info),
        sync_to_async(Returns_Efficiency_Ratios)(stock_url, info),
        sync_to_async(Company_Debt)(stock_url, info),
    )
    

    results = {
        "Financial Reports": html_to_paragraph_text(markdown.markdown(stock_info[0])),
        "Company Analysis": html_to_paragraph_text(markdown.markdown(stock_info[1])),
        "Profitability Metrics": html_to_paragraph_text(markdown.markdown(stock_info[2])),
        "Profit Analysis Outlook": html_to_paragraph_text(markdown.markdown(stock_info[3])),
        "Growth of Stock": html_to_paragraph_text(markdown.markdown(stock_info[4])),
        "Returns Efficiency": html_to_paragraph_text(markdown.markdown(stock_info[5])),
        "Company Debt": html_to_paragraph_text(markdown.markdown(stock_info[6])),
    }
    cache.set(cache_key, results, timeout=60 * 30)
    return results



def json_data_api(date_api:str, stock: str) -> dict:
    # Grab stock information for our graphs and also exchangeNames and CompanyNames for
    # our UI
    """ This will prepare our data from YahooQuery in to create a graph, Long Names, and Exchanges for better UI/UX. 
    Arguments(): Data API will be used for us to connect with the buttons to change the graph of the stock via intervals. We'll be using date_api statements to create an interval.
    Stock is mostly reliant from our stock views. We can neglect stock checker
    

    """
    
    stock = stock.upper()
    ticker = Ticker(symbols=stock)
    summary = ticker.price.get(stock, {})
    company_name = summary.get("shortName") or summary.get("longName")
    exchange =  summary.get("exchangeName")
    date = summary.get("regularMarketTime")
    


    if date_api == '1D':
        period = '1d'
        interval = '1m'
        interval_format = '%a %H:00'
        
    elif date_api == '1W':
        period = '1wk'
        interval = '30m'
        interval_format = '%a %H:%M'
    elif date_api == '1M':
        period = '1mo'
        interval = '1h'
        interval_format = '%b %d'
        
    # Do years
    else:
       period = '1y'
       interval = '1wk'
       interval_format = '%y-%W'

    stock_bars = ticker.history(period=period, interval=interval)
    
    stock_bars = stock_bars.reset_index()

    stock_bars['date'] = pd.to_datetime(stock_bars['date'])
 

    graph_label = stock_bars['date'].dt.strftime(interval_format).tolist()
    graph_price = stock_bars['close'].tolist()


    return {
        'chart_label': graph_label,
        'chart_price': graph_price,
        'name': company_name,
        'exchange': exchange,
        'date': date,
    }

# Output: {'maxAge': 1, 'preMarketSource': 'FREE_REALTIME', 'postMarketChangePercent': -0.00018197265, 'postMarketChange': -0.049316406, 'postMarketTime': '2026-01-02 17:59:55', 'postMarketPrice': 270.9607, 'postMarketSource': 'FREE_REALTIME', 'regularMarketChangePercent': -0.00312652, 'regularMarketChange': -0.849976, 'regularMarketTime': '2026-01-02 14:00:00', 'priceHint': 2, 'regularMarketPrice': 271.01, 'regularMarketDayHigh': 277.8248, 'regularMarketDayLow': 269.02, 'regularMarketVolume': 37746172, 'regularMarketPreviousClose': 271.86, 'regularMarketSource': 'FREE_REALTIME', 'regularMarketOpen': 272.05, 'exchange': 'NMS', 'exchangeName': 'NasdaqGS', 'exchangeDataDelayedBy': 0, 'marketState': 'CLOSED', 'quoteType': 'EQUITY', 'symbol': 'AAPL', 'underlyingSymbol': None, 'shortName': 'Apple Inc.', 'longName': 'Apple Inc.', 'currency': 'USD', 'quoteSourceName': 'Nasdaq Real Time Price', 'currencySymbol': '$', 'fromCurrency': None, 'toCurrency': None, 'lastMarket': None, 'marketCap': 4021894250496}

# Grab the Autocomplete Stock

# async def get_stock_suggestion(request):
#     query = request.GET.get('term', '')


# Grab name and ztock price used for our html. The difference is that we can do async call from Javascript in order to update it constantly

@sync_to_async
def grab_current_price(stock: str) -> dict:
    stock = stock.upper()
    result_search = Ticker(stock)
    price = result_search.history(period="1d")["close"].iloc[-1]
    if price > 10:
        return float(round(price, 1))
    elif price > 4.5:
        return float(round(price, 2))
    else:
        return float(round(price, 3))
    
async def latest_price(request, stock):
    price = await grab_current_price(stock=stock)
    return JsonResponse({"price": price})



# This will be for our autocomplete stuff


API_KEY = os.getenv('ALPACA')


SECRET_KEY = os.getenv('SECRET_KEY')


CLAUDE = os.getenv('CLAUDE')


alpaca_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY)

@sync_to_async
def autocomplete(data: str):
    # Do multi-key sort

    # Ensure add caching in order to make the performance better of this autocomplete program
    # It's valid as the stock market wouldn't change by a lot and the existing stocks would ensure that caching 
    # will be the best choice for the memory management.

    cache_key = f"autocomplete:{data}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    ASSET_CACHE_KEY = "alpaca_all_assets"

    cache_asset = cache.get(ASSET_CACHE_KEY)

    TOP_EXCHANGE = {
        'NASDAQ': 0,
        'NYSE': 0,
        

    }
    
    data = data.upper()
    try:
        stock_param = GetAssetsRequest(
            status= AssetStatus.ACTIVE,
            asset_class= AssetClass.US_EQUITY,

        )
        asset = alpaca_client.get_all_assets(stock_param)
        cache_asset.set(ASSET_CACHE_KEY, asset, 86400)
       
       
        # Stock rec using  list comp
            
        # We want to short via marketCapshare for the trendiest stock to be int he top of the autocomplete.
        # For better User Experience
        # Filter out Leverage ETF, and OTC.


        RESTRICTED_WORD = 'ETF'
        stock_rec = [a for a in asset if a.symbol.upper().startswith(data.upper()) and a.tradable and (a.exchange.value != 'OTC') 
                     and (a.exchange.value != 'BATS') and RESTRICTED_WORD not in (a.name or '').upper() ][:80]
        
        
        
        stock_ticker = Ticker(symbols=stock_rec)

        data_price = stock_ticker.price
        # Needed for popularity of stock sorting

        def grab_market_cap(esc):
            return data_price.get(esc, {}).get("marketCap", 0) or 0
        def grab_top_exchange_rate(a):
            return TOP_EXCHANGE.get(a.exchange, 1)
        def grab_volume(sym):
            return data_price.get(sym, {}).get('regularMarketVolume',  0) or 0
        
        
        stock_rec.sort(
            key=lambda a: (
                grab_top_exchange_rate(a),
                grab_volume(a.symbol),
                grab_market_cap(a.symbol),
            ),
            reverse=True
        )

        result = stock_rec[:11]
        cache.set(cache_key, result, timeout=60 * 5)
        
        return result


    
    
        # We want to short via marketCapshare for the trendiest stock to be int he top of the autocomplete.

    except Exception as e:
        return(f"Status: {e}")

# Output: [{'exchange': 'NYQ', 'shortname': 'Agilent Technologies, Inc.', 'quoteType': 'EQUITY', 'symbol': 'A', 'index': 'quotes', 'score': 10046500.0, 'typeDisp': 'Equity', 'longname': 'Agilent Technologies, Inc.', 'exchDisp': 'NYSE', 'sector': 'Healthcare', 'sectorDisp': 'Healthcare', 'industry': 'Diagnostics & Research', 'industryDisp': 'Diagnostics & Research', 'dispSecIndFlag': False, 'isYahooFinance': True}, {'exchange': 'NYM', 'shortname': 'Platinum Apr 26', 'quoteType': 'FUTURE', 'symbol': 'PL=F', 'index': 'quotes', 'score': 3003200.0, 'typeDisp': 'Futures', 'exchDisp': 'NY Mercantile', 'isYahooFinance': True}, {'exchange': 'CMX', 'shortname': 'Aluminum Futures,Mar-2026', 'quoteType': 'FUTURE', 'symbol': 'ALI=F', 'index': 'quotes', 'score': 3000600.0, 'typeDisp': 'Futures', 'exchDisp': 'New York Commodity Exchange', 'isYahooFinance': True}, {'exchange': 'NGM', 'quoteType': 'EQUITY', 'symbol': 'SVAQU', 'index': 'quotes', 'score': 100004.0, 'typeDisp': 'Equity', 'longname': 'Silicon Valley Acquisition Corp.', 'exchDisp': 'NASDAQ', 'sector': 'Financial Services', 'sectorDisp': 'Financial Services', 'industry': 'Shell Companies', 'industryDisp': 'Shell Companies', 'isYahooFinance': True}, {'exchange': 'NCM', 'quoteType': 'EQUITY', 'symbol': 'NBRGU', 'index': 'quotes', 'score': 100002.0, 'typeDisp': 'Equity', 'longname': 'Newbridge Acquisition Limited', 'exchDisp': 'NASDAQ', 'sector': 'Financial Services', 'sectorDisp': 'Financial Services', 'industry': 'Shell Companies', 'industryDisp': 'Shell Companies', 'isYahooFinance': True}, {'exchange': 'NGM', 'quoteType': 'EQUITY', 'symbol': 'IGACR', 'index': 'quotes', 'score': 100001.0, 'typeDisp': 'Equity', 'longname': 'Invest Green Acquisition Corporation', 'exchDisp': 'NASDAQ', 'isYahooFinance': True}, {'exchange': 'CCY', 'shortname': 'AUD/USD', 'quoteType': 'CURRENCY', 'symbol': 'AUDUSD=X', 'index': 'quotes', 'score': 30109.0, 'typeDisp': 'Currency', 'longname': 'AUD/USD', 'exchDisp': 'CCY', 'isYahooFinance': True}]


# Bullish Indicator





def bullish_indicator(stock: str, period='6mo', interval="1d"):
    # Grab RSI indicators,  Moving Average Trend, etc. Weight it accordingly to create it for bullish indicator and connect it to my stock. 
    # Use pandas and pandas_ta for this endeavour

    # First grab the ticker itself, and ensure that we rename the keys into a lowercase

    # THe score should be out of 100
    score = 0

    stock = stock.upper()
    ticker_of_stock = Ticker(symbols=stock)

    df = ticker_of_stock.history(period=period, interval=interval)


    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
        
    })
    closing = df["close"]

    # For our RSI strength

    # RSI Range & Key Levels
    # 0 to 100: The fundamental range for the RSI oscillator.
    # Overbought: Above 70 (or 80/90).
    # Oversold: Below 30 (or 20/10).
    # Neutral Zone: Between 30 and 70. 

    # if Oversold it should be higher score, as it's a great sign for a breakout:


    df["rsi"] = ta.momentum.rsi(closing, windows=14)

    value_rsi = df["rsi"].iloc[-1]

    if value_rsi > 30:
        point += 20
    elif 30 <= value_rsi >= 70:
        point += 10
    else:
        point += 0

    # Grab SMA averages for 50 days and 200 days and aggergate it towards the score

    df["50SMA"]= ta.trend.sma_indicator(closing, window="50")
    df["200SMA"]= ta.trend.sma_indicator(closing, window="200") # Fixed the bug

    sma_average_fifty = df["50SMA"].iloc[-1]
    sma_average_two_hundred = df["200SMA"].iloc[-1]

    # Aggregates for strong recent growth
    if sma_average_fifty > sma_average_two_hundred:
        point += 30
    else:
        point = 0

    

    




    







async def information_letter(request, letters):
    quotes = await autocomplete(letters)
    results = []
    for q in quotes:
        results.append({
        'symbol': q.symbol ,
        'name': q.name or '',
        'exchange': q.exchange,
    })


    return JsonResponse({'results': results})




def check_stock(stock):
    try:
        ticker = yf.Ticker(stock)
        # We can do is if something doesn't return, we can do return None 
        # and in Search
        info = ticker.info
        
        day_stock_data = ticker.history(period='1d')

        stock_info = {
            'ticker': stock,
            'price': day_stock_data,
        }
    
    

        if not info or 'regularMarketPrice' not in info:
                return messages.error("The stock does not exist. Please try again")

            
        return stock_info

    # except (ValueError, ConnectionAbortedError, ConnectionError, KeyError, IndexError):
    #     return None
    except Exception as e:
    # Catch JSONDecodeError and any unexpected error
        print(f"Error fetching stock {stock}: {e}")
        return None






def search(request):
    # This is the index view where we will display the home page/search page
    # Now we need to find how to redirect the search html -> stock.html
    if request.method == "GET":
        # AAPL, etc
        search_stock = request.GET.get("search")
        
        if search_stock:
            search_stock = str(search_stock.upper())

        # ask for check_stocks
            stock_checked = check_stock(stock=search_stock)

            if stock_checked is None:
                messages.error(request, "Please Try Again, This Stock Does not Exist")
                return render(request, 'base/search.html')


            # This will give the stock the i = stock_checked. Since it's existing right?
            else:
                return redirect('stock', stock_tick=search_stock)
        # Now check if the stock exists
    return render(request, 'base/search.html')

def home(request):
    return render(request, 'base/home.html')


# Order for Stocks and will add portfolio
def order(request):
    if request.method == 'POST':
        get_order = request.POST.get('buy')
        if get_order == 'buy':
            pass



def portfolio_room(request):
    context = {'ticker': ticker}
    return render(request, 'base/portfolio_room.html', context)




def stock(request, stock_tick:str):

    # This will happen when the user has: Search.html -> Stock Checker ->
    money_owned = Profile.objects.all()
    
    

    stock_url = stock_tick.upper()

    info = StockInfo(stock_url)

    date_time = request.GET.get('interval', '1D')
    
    
    for i in ticker:
        
        if i['id'] == str(stock_tick):
            
            stock_url = i

    stock_url = stock_tick.upper()     


    if request.method == 'POST':
        get_order = request.POST.get('buy')
        if get_order == 'buy':
            pass



    

    # Gather Json data API
    # Not needed for Async.
    data_json =  json_data_api(date_api=date_time, stock=stock_url)


    label_graph = json.dumps(data_json['chart_label'])
    label_price = json.dumps(data_json['chart_price'])

    exchange = data_json["exchange"]
    stock_name = data_json["name"]
    date = data_json["date"]


    # needed
    data_stock = async_to_sync(build_stock_analyzer)(stock_url=stock_url, info=info)



    # Button

    
    # Create a matplotlib graph of stocks or any graphs

    context = {'ticker': ticker, 'information_of_stock': data_stock, 'stock_graph': label_graph, 'stock_price':
               label_price, "exchange": exchange, "longName": stock_name, 'date': date,}

    return render(request, 'base/stock.html', context)


def portfolio(request):
    return render(request, 'base/portfolio_room.html')

def signup(request):

    # We need to gather information, and we also need to check if the username exists in the database. If it does not, it shall proceed towards the signup, if not then we'll add a message_flash to warn user that the username exists in the database.
    if request.method == 'POST':
        email = request.POST.get('email')

        
        username = request.POST.get('username')
        
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists, please try again!")
            return render(request, 'base/authentication/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email already exists in the database, please try again!")
            return render(request, 'base/authentication/signup.html')
        else:
        
            user = User.objects.create_user(username=username, password=password, email=email)
        
            messages.success(request, "Successfully Signed up, please use login page!")
       
        redirect("base/authentication/login.html")

    return render(request, 'base/authentication/signup.html')





def loginpage(request):

    if request.user.is_authenticated:
        messages.error(request, "You're already authenticated!, No need to login again!")
        return render(request, 'base/search.html')
      
    # Check if user exists in the database, if not we can do a 

    if request.method == "POST":
        email = request.POST.get('email')
       

        password = request.POST.get('password')

        # This will check if user authentication will exist
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "This user does not exist, please signup or try again!")
            return render(request, 'base/authentication/login.html')


      
        else:
            login(request, user)
            messages.success(request, "Login successful! Enjoy MarketSight!")
            return render(request, 'base/search.html')
        
    return render(request, 'base/authentication/login.html')

def logout_page(request):
    
    logout(request)
    
    return render(request, 'base/authentication/logout.html')




def assistance(request):

    # We want user to be in the database: Email, and  Username

    # If it doesn't exist, we want it to have an error 

    if request.method == "POST":
        name = request.POST.get('name')
        
        email = request.POST.get('email')

        user_message  = request.POST.get('message')

        subject = request.POST.get('subject')
        
        user = authenticate(request, email=email, username=name)

        send_mail (
            subject = f"New Contact Message from {subject}",
            message= f"from {name} \n {user_message }",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER], 


        )
        messages.success(request, "Login successful! Enjoy MarketSight!")
        return render(request, 'base/search.html')


    return render(request, 'base/Assistance.html')









#  Create the login html, I will be using password redirects later



def stock_portfolio(request):
    # We will fetch user's stock portfolio from database and display it here
    context = {}

    # Check if there's nothing inside the portfolio (which would say, "Please Buy some Stocks for a deep analysis")
    return render(request, 'MarketSightBack/stock_portfolio.html', context)

