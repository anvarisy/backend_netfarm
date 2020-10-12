from .models import tenant, product, category, product_check_halal
from rest_framework import serializers
from api.models import order, order_detail, user_client

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = tenant
        fields = ('id','tenant_name','tenant_address','tenant_image','tenant_owner')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = category
        fields = ('id','category_name','category_image','show_homepage')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = product
        fields = ('id','product_name','product_price','product_image','tenant_id','category_id')

class HalalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = product_check_halal
        fields = ('id','product_id','halal','no_halal','date_accepted','date_expired')
        
class UclientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_client
        fields = ('email','full_name','address','kecamatan','kabupaten','post_code'
                  'phone','password','is_login')

class OrderDetail(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name')
    product_image = serializers.CharField(source='product.product_image')
    class Meta:
        model = order_detail
        fields = ('product_id','product_name','product_image','count_product','total','date_update')
        
class CartSerializer(serializers.ModelSerializer):
    details = OrderDetail(many=True)
    tenant_name = serializers.CharField(source='tenant.tenant_name')
    class Meta:
        model = order
        fields = ('order_id','user_id','tenant_id','tenant_name','total','date_update','status','details')
    
    def create(self, validated_data):
        detail_order = validated_data.pop('details')
        o = order.objects.create(**validated_data)
        for item in detail_order:
            order_detail.objects.create(order=o, **item)
        return o

class PostOrderDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = order_detail
        fields = ('product_id','count_product','total','date_update')
    
class PostCartSerializer(serializers.HyperlinkedModelSerializer):
    details = PostOrderDetail(many=True)
    data =None
    class Meta:
        model = order
        fields = ('order_id','user_id','tenant_id','total','date_update','status','details')
    
    def FillData(self, datas):
        self.data = datas
        return self.data
    
    def create(self, validated_data):
        detail_order = self.data.pop('details')
        o = order.objects.create(**self.data)
        for item in detail_order:
            order_detail.objects.create(order_id=self.data['order_id'],**item)
        return o