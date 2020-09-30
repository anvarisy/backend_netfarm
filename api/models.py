from django.db import models

# Create your models here.
class category(models.Model):
    category_id = models.CharField(max_length=20, primary_key=True)
    category_name = models.CharField(max_length=120)
    show_homepage = models.BooleanField()

class tenant(models.Model):
    tenant_id =  models.CharField(max_length=20, primary_key=True)
    tenant_name = models.CharField(max_length=70)
    tenant_address = models.TextField()
    tenant_owner = models.CharField(max_length=100)

class product(models.Model):
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=70)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='product')
    