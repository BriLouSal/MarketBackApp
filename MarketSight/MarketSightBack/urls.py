from django.urls import path
from django.http import HttpResponse
from . import views
import yfinance as yf



#  Append stock list when users add stock


#  We wanna get user information based on stocks


urlpatterns = [
    path('', views.search, name='search'),
    path('home/',  views.home, name='home'),
    path('room/',  views.portfolio_room, name='room'),
    path('stock/<str:stock_tick>/', views.stock, name='stock'),
    path('login/', views.loginpage, name='login'),
    path('signup/',views.signup, name='signup'),
    path('support/',views.assistance, name='assistance'),
    path('logout/', views.logout_page, name='logout_page'),
]









# room/<str:room_number> - This will match URLs like /room/1, /room/2, and so on. The <str:room_number> part of the URL captures the room number as a string.

