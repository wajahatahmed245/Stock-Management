from django.db.models.signals import post_save

from django.dispatch import receiver

from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock.models import Snippet
from stock.models import Product
from stock.models import Stock
from stock.models import TransferredStock

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


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        global authentication_token, sold
        authentication_token = request.headers.get("Authentication")
        sold = request.data["sold"]
        product_type = request.data["product_type"]
        color = request.data["color"]
        size = request.data["size"]
        stuff = request.data["stuff"]
        type = request.data["type"]
        product_data = dict(
            color=color,
            size=size,
            stuff=stuff,
            type=type,
            brand_name=request.data["brand_name"],
            no_of_pieces=request.data["no_of_pieces"],
            product_type=product_type,
            season=request.data["season"],
            product_sku=get_sku(type, size, stuff, color),
        )
        product = ProductSerializer(data=product_data)
        if product.is_valid():
            product.save()
            post_save.connect(product_list, sender=Product)
            return Response(product.data, status=status.HTTP_201_CREATED)
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=Product)
def insert_stock(sender, instance, **kwargs):
    token_management = TokenManagement()
    data = authentication_token
    user_info = token_management.get_info(authentication_token=data)
    stock_data = dict(
        created_by=user_info[0],
        product_sku=instance.product_sku,
        product_id=instance.id,
        sold=sold,
    )
    stock = StockSerializer(data=stock_data)
    if stock.is_valid():
        stock.save()
        return stock.data
    return Response(stock.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def stock_list(request):
    if request.method == "GET":
        token = request.headers.get("Authentication")
        token_management = TokenManagement()
        user_info = token_management.get_info(authentication_token=token)
        stock_get = Stock.objects.filter(created_by=user_info[0])
        stock = StockSerializer(stock_get, many=True)
        return Response(stock.data)


@api_view(["POST"])
def stock_transfer(request):
    if request.method == "POST":
        transfer_stock = TransferredStockSerializer(data=request.data)
        if transfer_stock.is_valid():
            transfer_stock.save()
            return Response(transfer_stock.data, status=status.HTTP_201_CREATED)
        return Response(transfer_stock.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_stock_transfer(request):
    if request.method == "GET":
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
