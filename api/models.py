from django.db import models
from django.contrib.auth.models  import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from unittest.util import _MAX_LENGTH
from pyasn1.compat.octets import null

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
    tenant_city_code = models.IntegerField(default=0)
    tenant_owner = models.CharField(max_length=100)
    tenant_image = models.ImageField(upload_to='tenant')
    def __str__(self):
        return self.tenant_name

class product(models.Model):
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)
    categories = models.ManyToManyField(category, through='product_category')
    product_name = models.CharField(max_length=160)
    product_price = models.IntegerField()
    product_weight = models.IntegerField(default=1)
    product_image = models.ImageField(upload_to='product')
    product_date = models.DateField(default=timezone.now)
    is_bpom = models.BooleanField(default=False)
    is_sibaweh = models.BooleanField(default=False)
    point_demand = models.IntegerField(default=0)
    point_favourite =  models.IntegerField(default=0)
    product_description = models.TextField(blank=True, null=True)
    def __str__(self):
        return "%s - %s " % (self.id, self.product_name) 

class product_category(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.product_name + " - " + self.category.category_name

class product_images(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE,related_name='image_collections')
    product_img = models.ImageField(upload_to='product')

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
    
class UserManager(BaseUserManager):
    def create_user(self,email,full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class user(AbstractBaseUser):
    email = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=35,blank=True)
    address = models.TextField(blank=True)
    kecamatan = models.CharField(max_length=50,blank=True)
    kabupaten = models.CharField(max_length=50,blank=True)
    post_code = models.CharField(max_length=5,blank=True)
    phone = models.CharField(max_length=14,blank=True)
    is_client = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    date_joined = models.DateField(default=timezone.now)
    referal = models.ForeignKey('self',null=True, blank=True, related_name='referral',on_delete=models.CASCADE)
    level = models.IntegerField()
    
    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    def __str__(self):
        return self.email
    # class Meta:
    #     verbose_name = _('user')
    #     verbose_name_plural = _('users')
    #     db_table = 'users'
        
    # def clean(self):
    #     super().clean()
    #     self.email = self.__class__.objects.normalize_email(self.email)


    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     send_mail(subject, message, from_email, [self.email], **kwargs)
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class bookmark(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    bookmark_date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.product.product_name + " - " + self.user.email

class order(models.Model):
    order_id = models.CharField(max_length=14, primary_key=True)
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    total = models.BigIntegerField()
    date_update = models.DateField()
    status = models.CharField(max_length=30)

class payment_status(models.Model):
    order = models.ForeignKey(order,related_name='ostatus', on_delete=models.CASCADE)
    transaction_time = models.DateField(default=timezone.now)
    transaction_status = models.CharField(max_length=30)
    payment_type = models.CharField(max_length=120)

class order_detail(models.Model):
    order = models.ForeignKey(order, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(product, related_name='product_order', on_delete=models.CASCADE)
    count_product = models.IntegerField()
    total = models.BigIntegerField()
    date_update = models.DateField()

class promo(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE, blank= True, null=True)
    name = models.TextField()
    image = models.ImageField(upload_to='promo')
    url = models.CharField(max_length=160)
    position = models.IntegerField()

class paycod(models.Model):
    order = models.ForeignKey(order,on_delete=models.CASCADE)
    pay_date = models.DateField(default=timezone.now)

class paycod_attachment(models.Model):
    paycod = models.ForeignKey(paycod, on_delete=models.CASCADE, related_name='attachments')  
    attachment = models.FileField(upload_to='cod_attachment')