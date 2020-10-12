from django.shortcuts import render
from rest_framework import generics, renderers
from .models import category, tenant, product, product_check_halal
from .serializer import CategorySerializer, TenantSerializer, ProductSerializer, HalalSerializer
from api.serializer import CartSerializer
from api.models import order

# Create your views here.
class ApiAllCategory(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = CategorySerializer
    def get_queryset(self):
        queryset = category.objects.all()
        status = self.request.query_params.get('homepage', None)
        if status is not None:
            queryset = queryset.filter(show_homepage=status)
        return queryset


class ApiAllProduct(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = product.objects.all()
        pid = self.request.query_params.get('pid', None)
        if pid is not None:
            queryset = queryset.filter(id=pid)
        return queryset 


class ApiAllTenant(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = TenantSerializer
    def get_queryset(self):
        queryset = tenant.objects.all()
        tid = self.request.query_params.get('tid', None)
        if tid is not None:
            queryset = queryset.filter(id=tid)
        return queryset


class ApiCheckHalal(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = HalalSerializer
    def get_queryset(self):
        queryset = product_check_halal.objects.all()
        product = self.request.query_params.get('product', None)
        if product is not None:
            queryset = queryset.filter(product_id=product)
        return queryset


class ApiCart(generics.ListAPIView):
    serializer_class = CartSerializer
    def get_queryset(self):
        queryset = order.objects.all()
        oid = self.request.query_params.get('oid', None)
        if oid is not None:
            queryset = queryset.filter(order_id=oid)
        return queryset