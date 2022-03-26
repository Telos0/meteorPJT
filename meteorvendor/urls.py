from django.urls import path
from . import views


urlpatterns = [
    path('', views.OwnerProductList.as_view()),
    path('makenft/', views.OwnerProductCreate.as_view()),
]