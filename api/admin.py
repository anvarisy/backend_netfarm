from django.contrib import admin
from api.models import category,product,tenant
# Register your models here.
admin.site.register([category,product,tenant])