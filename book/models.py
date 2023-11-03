from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from accounts.models import Address
from django.core.validators import FileExtensionValidator

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    main_image = models.ImageField(upload_to='book/main/')
    description = models.TextField()
    pre_order_open = models.BooleanField(default=True)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    avialable_at = models.DateTimeField()
    stock = models.IntegerField(default=1)
    avialable_country = CountryField(multiple=True, default='BD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def get_buy_link(self):
        return reverse('book:buy_book', args=[int(self.id)])
    
    def get_absolute_url(self):        
        return reverse('book:book_details', args=[self.slug])
    
    def __str__(self):
        return f'{self.title}'
    
    def post_save_signal_for_images(self):
        # If this method exists then signal will save image record for model
        img_fields = ['main_image']
        
        return img_fields
    
class BookOrder(models.Model):
    ORDER_STATUS =(
        ('pending', 'Pending'),  
        ('processing', 'Processing'),
        ('confirm', 'confirm'),
        ('shipped', 'Shipped'),        
        ('completed', 'Completed'),  
        ('canceled', 'Canceled')       
    )
    amount = models.FloatField()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_orders')    
    delivery_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='order_delivery_address', null=True, blank=True)
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return f'{self.id}'
    
class BookOrderItem(models.Model):
    item = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='item_orders')
    order = models.ForeignKey(BookOrder, on_delete=models.PROTECT, related_name='book_order_items')
    sale_price = models.FloatField()
    quantity = models.IntegerField()
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f'{self.item.title}'
    
class OrderTransaction(models.Model):    
    order = models.ForeignKey(BookOrder, on_delete=models.PROTECT, related_name='order_trans')
    amount = models.FloatField()
    gateway = models.CharField(max_length=50)
    trxID = models.TextField()    
    mobile = models.CharField(max_length=50, null=True, blank=True)
    screenshoot = models.FileField(
        upload_to='transactions/screenshoot', 
        validators=[ 
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf'], message='Only image (jpg, jpeg, png, gif) and PDF files are allowed.')
            ]
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f'{self.order.id}'
    
    
    
    
