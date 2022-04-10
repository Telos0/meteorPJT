from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Vendor(models.Model):
    vendorid = models.CharField(max_length=30, unique=True)
    vendorpassword = models.CharField(max_length=30)
    vendorname = models.CharField(max_length=30)
    vendorchainaccount = models.CharField(max_length=200, unique=True)
    insdttm = models.DateTimeField(auto_now_add=True)
    upddttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendorname

class Owner(models.Model):
    ownerid = models.CharField(max_length=30, unique=True)
    ownerpassword = models.CharField(max_length=30, null=True)
    ownername = models.CharField(max_length=30)
    oweneremail = models.EmailField(max_length=128, null=True)
    ownerchainaccount = models.CharField(max_length=200, unique=True)
    insdttm = models.DateTimeField(auto_now_add=True)
    upddttm = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.ownername

class Product(models.Model):
    productid = models.CharField(max_length=30, unique=True)
    productnickname = models.CharField(max_length=30)
    productimageurl = models.URLField(max_length=200, null=True)
    vendorid = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    insdttm = models.DateTimeField(auto_now_add=True)
    upddttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.productnickname}'

    def get_absolute_url(self):
        return f'/meteorvendor/'

class OwnerProduct(models.Model):
    ownerid = models.ForeignKey(Owner, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)
    ownerproductchainaccount = models.CharField(max_length=200, unique=True)
    issuedyn = models.BooleanField(default='N')
    insdttm = models.DateTimeField(auto_now_add=True)
    upddttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.ownerproductchainaccount}'

    def get_absolute_url(self):
        return f'/meteorvendor/'

class OwnerProductHistory(models.Model):
    ownerproductchainaccount = models.ForeignKey(OwnerProduct, on_delete=models.CASCADE)
    changeseq = models.IntegerField(default=0)
    fromownerchainaccount = models.CharField(max_length=200, null=True)
    toownerchainaccount = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.ownerproductchainaccount} : {self.changeseq}'