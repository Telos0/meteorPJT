from .models import Product, OwnerProduct
from bootstrap_modal_forms.forms import BSModalModelForm

class ProductModelForm(BSModalModelForm):
    class Meta:
        model = Product
        fields = ['productid', 'productnickname', 'vendorid']