from django.contrib import admin
from .models import Vendor, Product, Owner, OwnerProduct, OwnerProductHistory
# Register your models here.


admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Owner)
admin.site.register(OwnerProduct)
admin.site.register(OwnerProductHistory)