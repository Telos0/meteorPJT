from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Vendor, Product, Owner, OwnerProduct, OwnerProductHistory

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


class OwnerProductList(ListView):
    model = OwnerProduct

    def get_context_data(self, **kwargs):
        context = super(OwnerProductList, self).get_context_data()
        print(context)
        productaccountList = []
        productinfoblockchainList = []

        inproduct = OwnerProduct.objects.all()
        for x in inproduct:
            productaccountList.append(x.ownerproductchainaccount)

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

class OwnerProductCreate(CreateView):
    model = OwnerProduct
    fields = ['ownerid', 'productid']

    def form_valid(self, form):





        ownerid = Owner.objects.get(id=self.request.POST.get('ownerid')).ownerid
        ownername = Owner.objects.get(ownerid=ownerid).ownername
        productid = Product.objects.get(id=self.request.POST.get('productid')).productid
        productname = Product.objects.get(productid=productid).productnickname

        web3.eth.defaultAccount = '0x1d6d0ea6103825ABF19898A7d5c4F00B6bEa2fDe'  # 'web3.eth.accounts[0]'
        abi = json.loads(abi_makeProduct_contract)
        address = web3.toChecksumAddress('0xd39842cef042a084408dc0b9328ad4ff9bcbb220')
        contract = web3.eth.contract(address=address, abi=abi)
        tx_hash = contract.functions.makeProduct(productname, productid, ownername, "11").transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        logs = contract.events.Transfer().processReceipt(tx_receipt)
        print(logs)

        ownerproductchainaccount = logs[0]['args']['pAddress']

        temp_form = form.save(commit=False)
        temp_form.issuedyn = False
        temp_form.ownerproductchainaccount = ownerproductchainaccount
        temp_form.save()


        response = super(OwnerProductCreate, self).form_valid(form)

        return response


