from .models import tenant, product, category, product_check_halal
from rest_framework import serializers
from api.models import bookmark, order, order_detail, product_category, product_images, promo, user
from django.contrib.auth import get_user_model
UserModel = get_user_model()
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = tenant
        fields = ('id','tenant_name','tenant_address','tenant_image','tenant_owner')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = category
        fields = ('id','category_name','category_image','show_homepage')

class ProductCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name')
    class Meta:
        model = product_category
        fields = ('category_id','category_name')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_images
        fields = ('product_img',)

class ProductSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.tenant_name')
    # categories = ProductCategorySerializer(many=True, read_only=True)
    categories = serializers.SerializerMethodField()
    image_collections = ProductImageSerializer(many=True)
    class Meta:
        model = product
        fields = ('id','product_name','product_price','product_date','product_image','product_description','tenant_id',
        'tenant_name','image_collections','categories')
    def get_categories(self, product_instance):
        query_datas = product_category.objects.filter(product=product_instance)
        return [ProductCategorySerializer(category).data for category in query_datas]
        
class FavouriteSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = order_detail
        fields = ('product_id','product')
    def get_product(self, product_instance):
        query = product.objects.filter(id=product_instance['product_id'])
        return[ProductSerializer(product).data for product in query]

class BookmarkSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = bookmark
        fields = ('id','user_id','bookmark_date','product')
    def get_product(self, product_instance):
        query = product.objects.filter(id=product_instance.product_id)
        return[ProductSerializer(product).data for product in query]  

class HalalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = product_check_halal
        fields = ('id','product_id','halal','no_halal','date_accepted','date_expired')
 
class RecursiveReferral(serializers.ModelSerializer):
    class Meta:
        model = user
        
class UclientSerializer(serializers.HyperlinkedModelSerializer):
    referral = RecursiveReferral()
    class Meta:
        model = user
        fields = ('email','full_name','address','kecamatan','kabupaten','post_code',
                  'phone','password','referral','level')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('email','full_name','phone','referal_id','level')

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
    data_ = None
    class Meta:
        model = order
        fields = ('order_id','user_id','tenant_id','total','date_update','status','details')
    
    def FillData(self, datas):
        self.data = datas
        self.data_ = datas
        return self.data
    
    def create(self, validated_data):
        detail_order = self.data.pop('details')
        o = order.objects.create(**self.data)
        for item in detail_order:
            order_detail.objects.create(order_id=self.data['order_id'],**item)
        return (o,detail_order)
    
class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = promo
        fields = ('date_start','date_end','tenant_id','name','image','url','position')

