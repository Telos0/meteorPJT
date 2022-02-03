from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Vendor, Product

# Create your views here.

class ProductList(ListView):
    model = Product




