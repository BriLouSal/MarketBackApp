from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from . import views
import yfinance as yf



#  Append stock list when users add stock


#  We wanna get user information based on stocks


urlpatterns = [
    path('', views.search, name='search'),
    path('home/',  views.home, name='home'),
    path('room/',  views.portfolio_room, name='room'),
    path('stock/<str:stock_tick>/', views.stock, name='stock'),
    # path("api/stock/<str:stock_tick>/", views.json_api, name="stock_json"), Not sure about this one, I will add this if I need to create an API gateway for graph
    path('logout/', views.logout_page, name='logout_page'),
    path('login/', views.loginpage, name='login'),
    path('signup/',views.signup, name='signup'),
    path('support/',views.assistance, name='assistance'),
    path('logout/', views.logout_page, name='logout_page'),
    # Create a autoupdating stock path for Javascript
    path("api/latest-price/<str:stock>/", views.latest_price, name="latest_price"),

]




if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]




# room/<str:room_number> - This will match URLs like /room/1, /room/2, and so on. The <str:room_number> part of the URL captures the room number as a string.

