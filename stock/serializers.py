from rest_framework import serializers

from stock.models import Snippet
from stock.models import Product
from stock.models import Stock
from stock.models import TransferredStock


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = (
            "title",
            "code",
            "linenos")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "color",
            "product_parameters",
            "stuff",
            "type",
            "brand_name",
            "product_sku",
            "product_type",
            "season",
            "price"
        ]


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            "_id",
            "created_at",
            "updated_at",
            "created_by",
            "product_sku",
            "sold"
        )


class TransferredStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferredStock
        fields = (
            "created_at",
            "updated_at",
            "seller",
            "vendor",
            "product_sku")
