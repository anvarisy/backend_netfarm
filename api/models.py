from django.db import models

# Create your models here.
class category(models.Model):
    id_category = models.CharField(max_length=20, primary_key=True)
    name_category = models.CharField(max_length=120)
    show_homepage = models.BooleanField()

class tenant(models.Model):
    id_tenant =  models.CharField(max_length=20, primary_key=True)
    name_tenant = models.CharField(max_length=70)
    address_tenant = models.TextField()
    owner_tenant = models.CharField(max_length=100)
