from django.contrib import admin

# Register your models here.
from stock.models import Product, Stock, TransferredStock

admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(TransferredStock)


