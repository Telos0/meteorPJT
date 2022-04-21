from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
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

#abis
abi_product_contract = """\
[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_toOwner",
				"type": "address"
			}
		],
		"name": "changeOwner",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [],
		"name": "productIssue",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_owner",
				"type": "address"
			},
			{
				"name": "_product_name",
				"type": "string"
			},
			{
				"name": "_product_id",
				"type": "string"
			},
			{
				"name": "_vendorname",
				"type": "string"
			},
			{
				"name": "_product_description",
				"type": "string"
			}
		],
		"name": "setProduct",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getAddressList",
		"outputs": [
			{
				"name": "",
				"type": "address[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getProductAddress",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getProductInfo",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]"""

# Create your views here.

#CBV
class WalletHome(LoginRequiredMixin, ListView):
    model = Owner
    template_name = 'meteorwallet/wallet_home.html'

    def get_context_data(self, **kwargs):

        context = super(WalletHome, self).get_context_data()

        try:
            owner = Owner.objects.get(user=self.request.user)
            context['owner_list'] = owner
            context['ownerproduct_list'] = OwnerProduct.objects.filter(ownerid=owner)
            context['haschainaccountYN'] = 'Y'
        except Owner.DoesNotExist:
            context['owner_list'] = None
            context['ownerproduct_list'] = None
            context['haschainaccountYN'] = 'N'

        return context

class OwnerProductReadModal(LoginRequiredMixin, BSModalReadView):
    model = OwnerProduct
    template_name = 'meteorwallet/ownerproductmodal.html'


    def get_context_data(self, **kwargs):
        context = super(OwnerProductReadModal, self).get_context_data()
        #print(context['ownerproduct'])


        address = str(context['ownerproduct'])
        abi = json.loads(abi_product_contract)
        address = web3.toChecksumAddress(address)
        contract = web3.eth.contract(address=address, abi=abi)
        productinfo = contract.functions.getProductInfo().call()
        ownerchangelist = contract.functions.getAddressList().call()

        owner = productinfo[0]
        ownername = Owner.objects.get(ownerchainaccount=owner).ownername
        product_name = productinfo[1]
        product_id = productinfo[2]
        vendorname = productinfo[3]
        product_description = productinfo[4]

        context['owner'] = owner
        context['ownername'] = ownername
        context['product_name'] = product_name
        context['product_id'] = product_id
        context['vendorname'] = vendorname
        context['product_description'] = product_description
        context['ownerchangelist'] = ownerchangelist

        return context
#FBV
