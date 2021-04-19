from django.urls import path

from . import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('', views.index, name='index'),
    path('product/add/', views.product_list),
    path('stock/', views.stock_list)

]
