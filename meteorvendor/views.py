from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Vendor, Product

import json
from web3 import Web3

#블록체인 접속정보
ganache_url = "http://52.231.178.69:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

#abis
abi_product_contract = """\
[
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
				"name": "_vendor",
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

abi_makeProduct_contract = """\
[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_product_name",
				"type": "string"
			},
			{
				"name": "_product_id",
				"type": "string"
			},
			{
				"name": "_vendor",
				"type": "string"
			},
			{
				"name": "_product_description",
				"type": "string"
			}
		],
		"name": "makeProduct",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getMakeProductAddress",
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
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "pAddress",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "some",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	}
]"""

# Create your views here.

class ProductList(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data()

        productaccountList = []
        productinfoblockchainList = []

        inproduct = Product.objects.all()
        for x in inproduct:
            productaccountList.append(x.productaccount)

        print(productaccountList)
        abi = json.loads(abi_product_contract)
        for i in productaccountList:
            address = web3.toChecksumAddress(i)
            contract = web3.eth.contract(address=address, abi=abi)
            productinfo = contract.functions.getProductInfo().call()
            productinfoblockchainList.append(productinfo)

        context['productinfoblockchainList'] = productinfoblockchainList

        print(productinfoblockchainList)
        return context





