from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vendor, Product, Owner, OwnerProduct, OwnerProductHistory

from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
from .forms import ProductModelForm, OwnerProductModelForm, OwnerProductModelUpdateForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalUpdateView

import json
from web3 import Web3
import datetime

from azure.storage.blob import BlobServiceClient


#블록체인 접속정보
ganache_url = "http://52.231.178.69:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

defaultaccount = "0x1d6d0ea6103825ABF19898A7d5c4F00B6bEa2fDe"
makeproductaddress = "0x958B5f2536fe36E2579A736189c5037f8e91225A"
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
				"name": "_vendorname",
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
	}
]"""

# Create your views here.

class ProductList(LoginRequiredMixin, ListView):
    model = Product


class OwnerProductList(LoginRequiredMixin, ListView):
    model = OwnerProduct

    def get_context_data(self, **kwargs):
        context = super(OwnerProductList, self).get_context_data()

        print(self.request.user)
        try:
            owner = Owner.objects.get(user=self.request.user)
        except Owner.DoesNotExist:
            owner = None
        print(owner)

        if owner == None:
            context['haschainaccountYN'] = 'N'
            context['ownerchainaccount'] = 'Not exist'
            context['vendorYN'] = False
        else:
            context['haschainaccountYN'] = 'Y'
            context['ownerchainaccount'] = owner.ownerchainaccount
            context['vendorYN'] = owner.vendorYN


        context['ownerproduct_list'] = OwnerProduct.objects.filter(ownerid=owner)
        #블록체인 상태 확인
        #blockchainstate = web3.isConnected()
        #context['blockchainstate'] = blockchainstate

        return context

#모달로 변경 --> OwnerProductCreateModal
class OwnerProductCreate(CreateView):
    model = OwnerProduct
    fields = ['ownerid', 'productid']

    def form_valid(self, form):

        ownerid = Owner.objects.get(id=self.request.POST.get('ownerid')).ownerid
        ownername = Owner.objects.get(ownerid=ownerid).ownername
        productid = Product.objects.get(id=self.request.POST.get('productid')).productid
        productname = Product.objects.get(productid=productid).productnickname

        web3.eth.defaultAccount = defaultaccount  # 'web3.eth.accounts[0]'
        abi = json.loads(abi_makeProduct_contract)
        address = web3.toChecksumAddress(makeproductaddress)
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


class OwnerProductCreateModal(LoginRequiredMixin, BSModalCreateView):
    template_name = 'meteorvendor/ownerproduct_form_modal.html'
    form_class = OwnerProductModelForm
    success_message = 'Success: Product was created.'
    success_url = reverse_lazy('meteorvendor:OwnerProductList')

    def form_valid(self, form):
        if not self.request.is_ajax():
            ownerid = Owner.objects.get(id=self.request.POST.get('ownerid')).ownerid
            ownername = Owner.objects.get(ownerid=ownerid).ownername
            productid = Product.objects.get(id=self.request.POST.get('productid')).productid
            productname = Product.objects.get(productid=productid).productnickname

            web3.eth.defaultAccount = defaultaccount  # 'web3.eth.accounts[0]'
            abi = json.loads(abi_makeProduct_contract)
            address = web3.toChecksumAddress(makeproductaddress)
            contract = web3.eth.contract(address=address, abi=abi)
            tx_hash = contract.functions.makeProduct(productname, productid, ownername, "11").transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            logs = contract.events.Transfer().processReceipt(tx_receipt)
            #print(logs)

            ownerproductchainaccount = logs[0]['args']['pAddress']

            temp_form = form.save(commit=False)
            temp_form.ownerproductchainaccount = ownerproductchainaccount
            temp_form.save()

        return HttpResponseRedirect(self.success_url)


class OwnerProductUpdateModal(LoginRequiredMixin, BSModalUpdateView):
    model = OwnerProduct
    template_name = 'meteorvendor/ownerproductupdate_form_modal.html'
    form_class = OwnerProductModelUpdateForm
    success_message = 'Success: Product was updated.'
    success_url = reverse_lazy('meteorvendor:OwnerProductList')

    def form_valid(self, form):
        if not self.request.is_ajax():
            ownerproductchainaccount = self.request.POST.get('ownerproductchainaccount')
            toownerchainaccount = self.request.POST.get('toownerchainaccount')
            print(toownerchainaccount)
            try:
                toownerid = Owner.objects.get(ownerchainaccount=toownerchainaccount)
            except Owner.DoesNotExist:
                #redirect로 나중에 변경
                return HttpResponseRedirect('Error')

            web3.eth.defaultAccount = defaultaccount  # 'web3.eth.accounts[0]'
            abi = json.loads(abi_product_contract)
            contract = web3.eth.contract(address=ownerproductchainaccount, abi=abi)
            tx_hash = contract.functions.changeOwner(toownerchainaccount).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            temp_form = form.save(commit=False)
            temp_form.ownerid = toownerid
            temp_form.save()

        return HttpResponseRedirect(self.success_url)

#모달로 변경 --> ProductCreateModal
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

class ProductCreateModal(LoginRequiredMixin, BSModalCreateView):
    template_name = 'meteorvendor/product_form_modal.html'
    form_class = ProductModelForm
    success_message = 'Success: Product was created.'
    success_url = reverse_lazy('meteorvendor:ProductList')

    #form get시 쿼리셋 추가
    def get_form(self, *args, **kwargs):
        form = super(ProductCreateModal, self).get_form(*args, **kwargs)
        form.fields['vendorid'].queryset = Vendor.objects.filter(vendorid=Owner.objects.get(user=self.request.user).ownerid)
        return form

    def form_valid(self, form):
        if not self.request.is_ajax():
            image = self.request.FILES['chooseFile']
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

class OwnerProductReadModal(LoginRequiredMixin, BSModalReadView):
    model = OwnerProduct
    template_name = 'meteorvendor/ownerproductmodal.html'


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

def makechainaccount(request):

    user = request.user
    ownerid = user.username
    ownername = user.username
    owneremail = user.email

    ganache_url = "http://52.231.178.69:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    # make new account
    new_account = web3.parity.personal.new_account('the-passphrase')


    ownerchainaccount = new_account

    owner = Owner(ownerid=ownerid, ownername=ownername, ownerchainaccount=ownerchainaccount, user=user)
    owner.save()

    success_url = reverse_lazy('single_pages:landing')
    return HttpResponseRedirect(success_url)