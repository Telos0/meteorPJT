from django.urls import path
from . import views

app_name = 'meteorvendor'

urlpatterns = [
    path('', views.OwnerProductList.as_view(), name='OwnerProductList'),

    #makenft 모달로 변경
    #path('makenft/', views.OwnerProductCreate.as_view()),
    path('makenft/', views.OwnerProductCreateModal.as_view(), name='OwnerProductCreateModal'),

    path('productlist/', views.ProductList.as_view(), name='ProductList'),
    path('productlist/makeproduct/', views.ProductCreateModal.as_view(), name='ProductCreateModal'),

    #info모달 CBV로 변경
    #path('ownerproductmodal/<str:address>/', views.ownerproductmodal, name='ownerproductmodal'),
    path('ownerproductmodal/<int:pk>/', views.OwnerProductReadModal.as_view(), name='OwnerProductReadModal'),
    #모달로 전환
    #path('ownerproductblockinfo/<str:address>/', views.ownerproductblockinfo, name='ownerproductblockinfo'),
]