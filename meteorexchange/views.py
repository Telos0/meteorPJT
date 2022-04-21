from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView

from meteorvendor.models import Owner, OwnerProduct

import json
from web3 import Web3
import datetime

from azure.storage.blob import BlobServiceClient


#블록체인 접속정보
ganache_url = "http://52.231.178.69:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

defaultaccount = "0x1d6d0ea6103825ABF19898A7d5c4F00B6bEa2fDe"
# Create your views here.

#CBV
class ExchangeHome(LoginRequiredMixin, TemplateView):
    template_name = 'meteorexchange/exchange_home.html'

    def get_context_data(self, **kwargs):

        context = super(ExchangeHome, self).get_context_data()

        try:
            owner = Owner.objects.get(user=self.request.user)
            context['owner_list'] = owner
            context['haschainaccountYN'] = 'Y'
        except Owner.DoesNotExist:
            context['owner_list'] = None
            context['haschainaccountYN'] = 'N'

        return context
#FBV