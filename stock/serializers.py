from rest_framework import serializers

from stock.models import Snippet, Product, Stock, Season, ProductType, TransferredStock
from stock.models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['title', 'code', 'linenos']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['color', 'size', 'stuff', 'type', 'brand_name',
                  'no_of_pieces', 'product_IMIE', 'product_type', 'season']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['created_at', 'updated_at', 'created_by', 'product_IMIE', 'sold', 'product']


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['season']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['product_name']


class TransferredStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferredStock
        fields = ['created_at', 'updated_at', 'seller', 'vendor', 'stock']
