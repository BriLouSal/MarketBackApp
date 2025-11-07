
# Main Django library

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm



# User authentication library from Django


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from .backend import EmailBackend

# # Error checker
# import sys
# print(sys.executable)
# # email

from django.core.mail import send_mail
from django.conf import settings
# from .alpaca_market_test import stock, check_stock
# Investment Endeavors Library

from django.contrib import messages

import pandas as pd
import matplotlib.pyplot as plt
import csv as cs
from .trading_classes import get_asset_info, get_losers



from .models import Profile, Portfolio
# from alpaca.data.historical import CryptoHistoricalDataClient


from .MSOAI import check_stock, StockSummary


import yfinance as yf



# Side Library



#  This is the views.py file where we will handle the logic for our application
#  We will create views for home, portfolio room, stock, login, signup, and assistance

user = "Brain"


#  This is a list of stocks that we will use to display in the portfolio room
ticker = []

# This will be used as a feature to store recent_search of a user stock
recent_search = {}










def search(request):
    # This is the index view where we will display the home page/search page
    # Now we need to find how to redirect the search html -> stock.html
    if request.method == "GET":
        # AAPL, etc
        search_stock = request.GET.get("search")
        search_stock = str(search_stock )


    # ask for check_stock
        stock_checked = check_stock(stock=search_stock.upper())

        if stock_checked is None:
            messages.error(request, "Please Try Again, This Stock Does not Exist")
            return render(request, 'base/search.html')


        # This will give the stock the i = stock_checked. Since it's existing right?
        else:
            return redirect('stock', stock_tick=search_stock)
        # Now check if the stock exists

    # Display top and worst performer
    return render(request, 'base/search.html')

def home(request):
    return render(request, 'base/home.html')


def portfolio_room(request):
    context = {'ticker': ticker}
    return render(request, 'portfolio_room.html', context)

def stock(request, stock_tick):

    # This will happen when the user has: Search.html -> Stock Checker ->
    # We don't need to add none, as it's required for stocks to exist (return a value)
    stock_info = None
    for i in ticker:
        
        if i['id'] == str(stock_tick):
            
            stock_info = i
            summarized_stock = StockSummary(stock=stock_info)

    context = {'ticker': ticker}

    return render(request, 'base/stock.html', context)


def portfolio(request):
    return render(request, 'portfolio_room.html')

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



# def stock_portfolio(request):
#     # We will fetch user's stock portfolio from database and display it here
#     context = {}
#     return render(request, 'MarketSightBack/stock_portfolio.html', context)




