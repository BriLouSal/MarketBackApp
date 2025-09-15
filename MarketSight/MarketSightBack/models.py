from django.db import models

from django.utils import timezone


import yfinance as yf
# Create your models here.

#  Creating Users 
class Profile(models.Model):
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    money_owned = models.IntegerField(default=100000) # We want to have money for the Users to simulate stock trading. We'll do it in Model to remain dynamic and not remain static in views.
    def __str__(self):
        return self.username
    

class Chat(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateField(default = timezone.now)
    upvotes = models.IntegerField(default = 0)
    downvotes = models.IntegerField(default = 0)
    replies_count = models.IntegerField(default=0)
    def relevancy_algo(self):
        s = self.upvotes - self.downvotes
        

# User's owner of that Portfolio
# Requirements: Name and the Ticker of the Stock. The Book Cost, and the Total Return of that stock. 

#  In order to find the 
class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)

    
    def __str__(self):
        return f"{self.name} ({self.ticker})"















