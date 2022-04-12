from django.urls import path
from . import views


urlpatterns = [

    path('', views.WalletHome.as_view(), name='wallet_home'),
]