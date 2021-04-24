from django.db import models


# Create your models here.


class Snippet(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)


class Product_type(models.Model):
    product_name = models.CharField(max_length=20)


class Product(models.Model):
    color = models.CharField(max_length=50)
    product_size = models.TextField(max_length=50)
    stuff = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    brand_name = models.CharField(max_length=50)
    no_of_pieces = models.IntegerField()
    product_sku = models.TextField(unique=True)
    price = models.FloatField()
    season = models.CharField(max_length=25)
    product_type = models.ForeignKey(Product_type, on_delete=models.CASCADE)



class Stock(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=25)
    product_sku = models.TextField(unique=True)
    sold = models.BooleanField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.created_by


class TransferredStock(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    seller = models.CharField(max_length=25)
    vendor = models.CharField(max_length=25)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
