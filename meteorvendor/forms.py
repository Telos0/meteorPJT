from .models import Product, OwnerProduct, Owner
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

class ProductModelForm(BSModalModelForm):
    class Meta:
        model = Product
        fields = ['productid', 'productnickname', 'vendorid']

class OwnerProductModelForm(BSModalModelForm):
    class Meta:
        model = OwnerProduct
        fields = ['ownerid', 'productid', 'issuedyn']

class OwnerProductModelUpdateForm(BSModalModelForm,forms.Form):
    toownerchainaccount = forms.CharField(max_length=200, label='toownerchainaccount', error_messages= { 'required': 'Need chain account' })
    class Meta:
        model = OwnerProduct
        fields = ['ownerproductchainaccount']

    def clean(self):
        clean_data = super().clean()

        toownerchainaccount = clean_data.get('toownerchainaccount')
        try:
            toownerid = Owner.objects.get(ownerchainaccount=toownerchainaccount)
        except Owner.DoesNotExist:
            self.add_error('toownerchainaccount', 'No such user.')
