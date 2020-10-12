from django.contrib import admin
from api.models import category, order, order_detail, product, product_check_halal, tenant, user_client
# Register your models here.
admin.site.register([category,product,tenant,product_check_halal,user_client,order,order_detail])