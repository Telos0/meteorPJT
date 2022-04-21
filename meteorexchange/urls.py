from django.urls import path
from . import views

app_name = 'meteorexchange'

urlpatterns = [
    path('', views.ExchangeHome.as_view(), name='exchange_home'),
]