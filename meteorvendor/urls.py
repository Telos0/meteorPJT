from django.urls import path
from . import views

app_name = 'meteorvendor'

urlpatterns = [
    path('', views.OwnerProductList.as_view(), name='meteorvendormain'),
    path('makenft/', views.OwnerProductCreate.as_view()),
    path('productlist/', views.ProductList.as_view(), name='ProductList'),
    path('productlist/makeproduct/', views.ProductCreateModal.as_view(), name='ProductCreateModal'),

    path('ownerproductmodal/<str:address>/', views.ownerproductmodal, name='ownerproductmodal'),
    path('ownerproductblockinfo/<str:address>/', views.ownerproductblockinfo, name='ownerproductblockinfo'),
]