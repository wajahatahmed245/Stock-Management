from datetime import datetime

from django.db import models

# Create your models here.

from stock.utils import getImei


class Snippet(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)


class ProductType(models.Model):
    product_name = models.CharField(max_length=50)


class Season(models.Model):
    season = models.CharField(max_length=50)


class Product(models.Model):
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    stuff = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    brand_name = models.CharField(max_length=50)
    no_of_pieces = models.IntegerField(max_length=20)
    product_IMIE = models.IntegerField(max_length=20, unique=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)



class Stock(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
    created_by = models.CharField(max_length=25)
    product_IMIE = models.IntegerField(max_length=15, unique=True)
    sold = models.BooleanField
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class TransferredStock(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
    seller = models.CharField(max_length=25)
    vendor = models.CharField(max_length=25)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
