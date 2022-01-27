from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class Landing(TemplateView):
    template_name = 'single_pages/landing.html'