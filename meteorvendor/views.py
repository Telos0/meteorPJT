from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Vendor, Product, Owner, OwnerProduct, OwnerProductHistory

from django.urls import reverse_lazy
from .forms import ProductModelForm
from bootstrap_modal_forms.generic import BSModalCreateView

import json
from web3 import Web3
import datetime

from azure.storage.blob import BlobServiceClient


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


class ProductCreate(CreateView):
    model = Product
    fields = ['productid', 'productnickname', 'vendorid']

    def form_valid(self, form):

        image = self.request.FILES['chooseFile']
        print(image)
        img_name = None
        BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=blobstorageforpydev;AccountKey=ZJFb+5et4ROFCebrFvpNhWV9eT4cN68Uwa2wwjXPMeKsRhXTHmfDHKAbUO9wEr1gaDVQY+JKj8YGzwAEm+NINw==;EndpointSuffix=core.windows.net"
        BLOB_CONTAINER_NAME = "devmeteor"

        if self.request.FILES['chooseFile']:
            img = self.request.FILES['chooseFile']
            img_name = "ProductCreate_image_" + str(img) + str(datetime.datetime.now())

            blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
            blob_client = container_client.get_blob_client(img_name)
            blob_client.upload_blob(img, blob_type="BlockBlob")


        temp_form = form.save(commit=False)
        temp_form.productimageurl = f'https://blobstorageforpydev.blob.core.windows.net/devmeteor/{img_name}'
        temp_form.save()


        response = super(ProductCreate, self).form_valid(form)

        return response

class ProductCreateModal(BSModalCreateView):
    template_name = 'meteorvendor/product_form_modal.html'
    form_class = ProductModelForm
    success_message = 'Success: Product was created.'
    success_url = reverse_lazy('meteorvendor:ProductList')

    def form_valid(self, form):
        if not self.request.is_ajax():
            image = self.request.FILES['chooseFile']
            print(image)
            img_name = None
            BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=blobstorageforpydev;AccountKey=ZJFb+5et4ROFCebrFvpNhWV9eT4cN68Uwa2wwjXPMeKsRhXTHmfDHKAbUO9wEr1gaDVQY+JKj8YGzwAEm+NINw==;EndpointSuffix=core.windows.net"
            BLOB_CONTAINER_NAME = "devmeteor"

            if self.request.FILES['chooseFile']:
                img = self.request.FILES['chooseFile']
                img_name = "ProductCreate_image_" + str(img) + str(datetime.datetime.now())

                blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
                container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
                blob_client = container_client.get_blob_client(img_name)
                blob_client.upload_blob(img, blob_type="BlockBlob")


            temp_form = form.save(commit=False)
            temp_form.productimageurl = f'https://blobstorageforpydev.blob.core.windows.net/devmeteor/{img_name}'
            temp_form.save()


            #response = super(ProductCreateModal, self).form_valid(form)

        return HttpResponseRedirect(self.success_url)


#FBV

#사용보류
def ownerproductmodal(request, address):
    template_url = 'meteorvendor/ownerproductmodal.html'
    context = {}
    print('x')
    return HttpResponse(render(request, template_url, context))


def ownerproductblockinfo(request, address):
    template_url = 'meteorvendor/ownerproductblockinfo.html'

    abi = json.loads(abi_product_contract)
    address = web3.toChecksumAddress(address)
    contract = web3.eth.contract(address=address, abi=abi)
    productinfo = contract.functions.getProductInfo().call()

    owner = productinfo[0]
    product_name = productinfo[1]
    product_id = productinfo[2]
    vendor = productinfo[3]
    product_description = productinfo[4]

    context = {'owner' : owner, 'product_name' : product_name, 'product_id' : product_id, 'vendor' : vendor, 'product_description' : product_description}

    return HttpResponse(render(request, template_url, context))