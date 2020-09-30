from .models import tenant, product, category
from rest_framework import serializers

class TenantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tenant
        fields = ('tenant_id','tenant_name','tenant_address','tenant_owner')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = category
        fields = ('category_id','category_name','show_homepage')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = product
        fields = ('id','product_name','product_price','product_image','tenant_id','category_id')
