import pymongo as pymongo
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock.models import Snippet
from stock.models import Stock
from stock.models import TransferredStock
from stock.models import Product

from stock.serializers import SnippetSerializer
from stock.serializers import ProductSerializer
from stock.serializers import StockSerializer
from stock.serializers import TransferredStockSerializer

from stock.utils import get_sku

from utils.jwt_setter import TokenManagement


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def product_list(request):
    if request.method == "POST":
        try:
            authentication_token = request.headers.get("Authentication")
            sold = request.data["sold"]
            product_type = request.data["product_type"]
            color = request.data["color"]
            stuff = request.data["stuff"]
            type = request.data["type"]
            brand_name = request.data["brand_name"]
            season = request.data["season"]
            price = request.data["price"]
            product_size = request.data["product_size"]
            product_data = dict(
                color=color,
                product_size=product_size,
                stuff=stuff,
                type=type,
                brand_name=brand_name,
                product_type=product_type,
                season=season,
                product_sku=get_sku(type, stuff, color),
                price=price
            )
            product = ProductSerializer(data=product_data)
            if product.is_valid():
                product.save()

                token_management = TokenManagement()
                data = authentication_token
                user_info = token_management.get_info(authentication_token=data)
                stock_data = dict(
                    created_by=user_info[0],
                    product_sku=product.instance.product_sku,
                    sold=sold,
                )
                stock = StockSerializer(data=stock_data)
                if stock.is_valid():
                    stock.save()
                    data = dict(product_data=product.data, stock_data=stock.data)
                return Response(data, status=status.HTTP_201_CREATED)

        except Exception as error:
            return dict(message=str(error), success=False), 404


@api_view(["GET"])
def stock_list(request):
    if request.method == "GET":
        try:
            token = request.headers.get("Authentication")
            token_management = TokenManagement()
            user_info = token_management.get_info(authentication_token=token)
            stock_get = Stock.objects.filter(created_by=user_info[0])
            stock = StockSerializer(stock_get, many=True)
            product_sku = Stock.objects.values_list('product_sku', flat=True).filter(created_by=user_info[0])
            shirt_product = Product.objects.filter(product_type='shirt').filter(product_sku__in=product_sku)
            shirt_data = ProductSerializer(shirt_product, many=True)
            pant_product = Product.objects.filter(product_type='pant').filter(product_sku__in=product_sku)
            pant_data = ProductSerializer(pant_product, many=True)
            coat_product = Product.objects.filter(product_type='coat').filter(product_sku__in=product_sku)
            coat_data = ProductSerializer(coat_product, many=True)

            data = dict(
                product_data=dict(shirts_data=shirt_data.data, pants_data=pant_data.data, coats_data=coat_data.data),
                stock_data=stock.data)
            return Response(data)
        except Exception as error:
            return dict(message=str(error), success=False), 404


@api_view(["POST"])
def stock_transfer(request):
    if request.method == "POST":
        try:
            transfer_stock = TransferredStockSerializer(data=request.data)
            if transfer_stock.is_valid():
                transfer_stock.save()
                return Response(transfer_stock.data, status=status.HTTP_201_CREATED)
            return Response(transfer_stock.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return dict(message=str(error), success=False), 404


@api_view(["GET"])
def get_stock_transfer(request):
    if request.method == "GET":
        try:
            token = request.headers.get("Authentication")
            token_management = TokenManagement()
            user_info = token_management.get_info(authentication_token=token)
            stock_get = TransferredStock.objects.filter(seller=user_info[0])
            if stock_get:
                transferred_stock = TransferredStockSerializer(stock_get, many=True)
                return Response(transferred_stock.data)

            transfer_stock = TransferredStock.objects.filter(vendor=user_info[0])
            transferred_stock = TransferredStockSerializer(transfer_stock, many=True)
            return Response(transferred_stock.data)
        except Exception as error:
            return dict(message=str(error), success=False), 404
