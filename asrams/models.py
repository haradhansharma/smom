
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
# Create your models here.

class Asram(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    banner = models.ImageField(null=True, blank=True, upload_to='asrams/banner') # After saving here should save in child model

    about = models.TextField()
    street_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    asram_phone = PhoneNumberField('Ashram Phone', blank=True, null=True, help_text='Phone number will be public where vokto will call for any necessity!')
    country = CountryField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) 
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        Get the absolute URL of the blog post for reverse lookup.
        """
        return reverse('asrams:asram_detail', args=[self.slug])
    
    @property
    def avatar(self):
        principle = self.sanyasies.filter(is_head = True).order_by('-updated_at')
        if principle.exists():
            pic = principle.first().avatar.url if principle.first().avatar else '/static/blank_asram.png'
        else:
            pic = '/static/blank_asram.png'            
        return pic
        
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # If the slug field is not provided, create a slug from the name field
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while Asram.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super(Asram, self).save(*args, **kwargs)      
  
    def post_save_signal_for_images(self):
        # If this method exists then signal will save image record for model
        img_fields = ['banner']
        
        return img_fields
        

    
class Sanyashi(models.Model):
    name = models.CharField(max_length=152)
    asram = models.ForeignKey(Asram, on_delete=models.DO_NOTHING, related_name='sanyasies')
    avatar = models.ImageField(null=True, blank=True, upload_to='sanyashi/avatar') # After saving here should save in child model  
    is_head = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) 
    
    def post_save_signal_for_images(self):
        # If this method exists then signal will save image record for model
        img_fields = ['avatar']
        
        return img_fields
        
        
    def save(self, *args, **kwargs):
        if self.is_head:
            # If the current instance is set as the head, find and update the existing head.
            Sanyashi.objects.filter(asram=self.asram, is_head=True).update(is_head=False)

        super(Sanyashi, self).save(*args, **kwargs)
        
        

        

    

    

    