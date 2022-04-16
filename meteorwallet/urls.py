from django.urls import path
from . import views

app_name='meteorwallet'
urlpatterns = [

    path('', views.WalletHome.as_view(), name='wallet_home'),
    path('ownerproductmodal/<int:pk>/', views.OwnerProductReadModal.as_view(), name='OwnerProductReadModal'),
]