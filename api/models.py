from django.db import models

# Create your models here.
class category(models.Model):
    # category_id = models.CharField(max_length=6, primary_key=True)
    category_name = models.CharField(max_length=120)
    show_homepage = models.BooleanField()
    category_image = models.ImageField(upload_to='category')
    def __str__(self):
        return self.category_name

class tenant(models.Model):
    # tenant_id =  models.CharField(max_length=6, primary_key=True)
    tenant_name = models.CharField(max_length=70)
    tenant_address = models.TextField()
    tenant_owner = models.CharField(max_length=100)
    tenant_image = models.ImageField(upload_to='tenant')
    def __str__(self):
        return self.tenant_name

class product(models.Model):
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=70)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='product')
    is_bpom = models.BooleanField(default=False)
    is_sibaweh = models.BooleanField(default=False)
    def __str__(self):
        return self.product_name
    
class product_check_halal(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    halal_choice = (
        (None,'-'),
        ('bpom','BPOM'),
        ('sibaweh','SIBAWEH'),
    )
    halal = models.CharField(choices=halal_choice, default=None, blank=True, max_length=10)
    no_halal = models.CharField(max_length=128)
    date_accepted = models.DateField(default=None, blank= True)
    date_expired = models.DateField(default=None, blank=True)
    
class user_client(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=35)
    address = models.TextField()
    kecamatan = models.CharField(max_length=50)
    kabupaten = models.CharField(max_length=50)
    post_code = models.IntegerField()
    phone = models.CharField(max_length=14)
    password = models.CharField(max_length=140)
    is_login = models.BooleanField(default=False)
    def __str__(self):
        return self.email

class order(models.Model):
    order_id = models.CharField(max_length=14, primary_key=True)
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(user_client, on_delete=models.CASCADE)
    total = models.BigIntegerField()
    date_update = models.DateField()
    status = models.CharField(max_length=30)
    
class order_detail(models.Model):
    order = models.ForeignKey(order, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    count_product = models.IntegerField()
    total = models.BigIntegerField()
    date_update = models.DateField()

    
    