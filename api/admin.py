from django.contrib import admin
from api.models import category,product,tenant,product_check_halal
# Register your models here.
admin.site.register([category,product,tenant,product_check_halal])