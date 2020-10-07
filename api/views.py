from django.shortcuts import render
from rest_framework import generics, renderers
from .models import category, tenant, product, product_check_halal
from .serializer import CategorySerializer, TenantSerializer, ProductSerializer, HalalSerializer

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
        return queryset 


class ApiAllTenant(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = TenantSerializer
    def get_queryset(self):
        queryset = tenant.objects.all()
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