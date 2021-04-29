from django.db import models

from djongo.models import JSONField
from djongo.models import ObjectIdField


class Snippet(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)


class Product(models.Model):
    _id = ObjectIdField()
    color = models.CharField(max_length=50)
    parameters = JSONField()
    stuff = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    brand_name = models.CharField(max_length=50)
    product_sku = models.TextField(unique=True)
    price = models.FloatField()
    season = models.CharField(max_length=25)
    category = models.CharField(max_length=25)


class Stock(models.Model):
    _id = ObjectIdField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=25)
    product_sku = models.TextField(unique=True)
    sold = models.BooleanField()
    product_category = models.CharField(max_length=25)

    def __str__(self):
        return self.created_by


class TransferredStock(models.Model):
    _id = ObjectIdField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    seller = models.CharField(max_length=25)
    vendor = models.CharField(max_length=25)
    product_sku = models.TextField()
