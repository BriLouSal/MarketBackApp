from django.db import models

from django.utils import timezone


import yfinance as yf

import time
from .MSOAI import check_stock

MAX_LENGTH_OF_TITLE = 255


MAX_CASH = 100000
# This should be the most important part of determining relevancy
# as it should carry more weigh
ACTIVITY_PARAMETERS = 1.25

DURATION_DECAY = 0.5

DEFAULT_VOTE = 0
class Profile(models.Model):
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    money_owned = models.IntegerField(default=MAX_CASH) # We want to have money for the Users to simulate stock trading. We'll do it in Model to remain dynamic and not remain static in views.

    def __str__(self):
        return self.username
    

class Chat(models.Model):
    title = models.CharField(max_length=MAX_LENGTH_OF_TITLE)
    
    body = models.TextField()


    
    
    created_at = models.DateField(default=timezone.now)
    
    upvotes = models.IntegerField(default=DEFAULT_VOTE)
   
    downvotes = models.IntegerField(default=DEFAULT_VOTE)
   
    replies_count = models.IntegerField(default=DEFAULT_VOTE)
    # We need to convert self_created_at into integer in order to make my algorithim to work


    # This algorithim will ensure the relevancy is accurate
    def relevancy_algo(self):
        time_now = timezone.now
        time_decay = (time_now - self.created_at).total_second() / 86400
        return (self.upvotes - self.downvotes) + (self.replies_count * ACTIVITY_PARAMETERS) + (time_decay * DURATION_DECAY)



        

# User's owner of that Portfolio
# Requirements: Name and the Ticker of the Stock. The Book Cost, and the Total Return of that stock. 

#  In order to find the 
class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)

    convert_ticker_string = str(ticker)


    if check_stock(convert_ticker_string.upper()):
        pass
    

    
    def __str__(self):
        return f"{self.name} ({self.ticker})"












