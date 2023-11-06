from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from accounts.models import Address
from django.core.validators import FileExtensionValidator
from django.db.models import Sum
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
    
    @property
    def get_discount_list(self):
        discounts = self.discounts.all().order_by('quantity').values_list('quantity', 'percent') #sorting is essential or discounts.sort(key=lambda x: x[0])
        if discounts.exists():
            return discounts
        else:
            return {}
        
    
  
    def cal_price(self, quantity):
        discounts = self.get_discount_list       
        
        discount_percent = 0.0
        
        for tier_quantity, tier_discount in discounts:
            if int(quantity) >= tier_quantity:
                discount_percent = tier_discount
            else:
                break          
        
        
        discounted_price = self.price - (self.price*int(discount_percent))/100  
        
        return discounted_price
        
        
    
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
    
class Discount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='discounts')
    quantity = models.IntegerField()
    percent = models.FloatField()
    
    def __str__(self):
        return f'#{self.book}--{self.percent}% for more then {self.percent}'
    
class BookOrder(models.Model):
    
    ORDER_STATUS = settings.ORDER_STATUS
    
    amount = models.FloatField()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_orders')    
    delivery_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='order_delivery_address', null=True, blank=True)
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    @property
    def order_item(self):
        return self.book_order_items.all().first().item.title
    
    @property
    def inv(self):
        try:
            invoice = self.invoice        
        except Exception as e:
            invoice = None
            
        return invoice
    
    @property
    def trans_amount(self):
        total_amount = self.order_trans.filter(check_and_confirmed = True).aggregate(total=Sum('amount'))['total']     
        if total_amount is not None:     
            t_amount = total_amount
        else:
            t_amount = 0
            
        return t_amount
    
    @property
    def pending_amount(self):
        result = self.amount - self.trans_amount
        return max(result, 0)
    
    
    @property
    def has_transactions(self):
        return self.order_trans.all().exists()
            
    
    
    def __str__(self):
        return f'{self.id}'
    
class BookOrderItem(models.Model):
    item = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='item_orders')
    order = models.ForeignKey(BookOrder, on_delete=models.CASCADE, related_name='book_order_items')
    sale_price = models.FloatField()
    quantity = models.IntegerField()
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    
    def __str__(self):
        return f'{self.item.title}'
    
class OrderInvoice(models.Model):
    order = models.OneToOneField(BookOrder, on_delete=models.CASCADE, primary_key=True, related_name="invoice")
    filepath = models.FileField(upload_to=settings.INVOICE_UPLOAD_TO)
    validity = models.DateTimeField()
    gateway = models.CharField(max_length=50, default='')
    paid = models.BooleanField(default=False)
    paid_on = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.order}'
    
    @property
    def update_payment_url(self):
        return reverse('book:update_payment', args=[int(self.order.id)])
    
class OrderTransaction(models.Model):    
    order = models.ForeignKey(BookOrder, on_delete=models.PROTECT, related_name='order_trans')
    amount = models.FloatField()
    gateway = models.CharField(max_length=50)
    trxID = models.TextField()    
    mobile = models.CharField(max_length=50, null=True, blank=True)
    check_and_confirmed = models.BooleanField(default=False)
    check_and_reject = models.BooleanField(default=False)
    
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
    
    
    
    
