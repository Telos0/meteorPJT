from django.db import models

# Create your models here.

class Vendor(models.Model):
    vendorname = models.CharField(max_length=30)

    def __str__(self):
        return self.vendorname

class Product(models.Model):
    productid = models.CharField(max_length=30)
    productnickname = models.CharField(max_length=30, null=True)
    productimageurl = models.URLField(max_length=200, null=True)
    productqty = models.IntegerField(default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    insdttm = models.DateTimeField(auto_now_add=True)
    upddttm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.productid}'
