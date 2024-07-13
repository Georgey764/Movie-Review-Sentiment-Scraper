from django.urls import path
from restAPI import views

urlpatterns = [
    path('stocks_list/', views.stocks_list),
    path('get_sentiment/', views.get_sentiment),
]