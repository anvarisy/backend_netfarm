from django.shortcuts import render
from rest_framework import viewsets
from .models import category, tenant, product
from .serializer import CategorySerializer, TenantSerializer, ProductSerializer

# Create your views here.
class ApiAllCategory(viewsets.ModelViewSet):
    queryset  = category.objects.all()
    serializer_class = CategorySerializer

class ApiAllProduct(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

class ApiAllTenant(viewsets.ModelViewSet):
    queryset = tenant.objects.all()
    serializer_class = TenantSerializer