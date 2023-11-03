from django.db import models

import uuid
from django.db import models
from django.urls import reverse
from PIL import Image
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Resize, ProcessorPipeline
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.templatetags.static import static
from django_countries.fields import CountryField
from django.utils import timezone


class Workshop(models.Model):
    name = models.CharField(max_length=255)
    featured_image = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.name

class QIUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The Email field must be set.")
        
        if not username:
            username = email.split('@')[0]
            
        email = self.normalize_email(email)   
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return super(QIUserManager, self).create_user(username, email, password, **extra_fields)

    def create_superuser(self, username = None, email=None, password=None, **extra_fields):
        return super(QIUserManager, self).create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    
    INTERESTED_IN = (
        ('donation', 'Donation'),
        ('volunteering', 'Volunteering'),
    )
    
    
    username_validator = UnicodeUsernameValidator()
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    
    username = models.CharField(
        _("username"),      
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
   
    email = models.EmailField('E-Mail Address', unique=True)
    phone = PhoneNumberField('Phone', blank=True, null=True)
    organization = models.CharField(max_length=252, null=True, blank=True)
    interest_in = models.CharField(max_length=20, choices=INTERESTED_IN, null=True, blank=True)       
    in_workshops = models.ManyToManyField(Workshop, related_name='interest_workshops', blank=True)
    
    
    objects = QIUserManager()    

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        if not self.username:
            # Set the username based on the part of the email address before '@'
            base_username = self.email.split('@')[0]
            username = base_username
            count = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{count}"
                count += 1
            self.username = username
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
    
    def get_absolute_url(self):        
        return reverse('accounts:user_link', args=[str(self.id)])    
    
    @property
    def avatar(self):    
        if self.is_authenticated and hasattr(self, 'profile') and self.profile.avatar:  
            profile = self.profile   
            img = profile.avatar.url
        else:
            img = static('no_image.png')           

        return img
    
    @property
    def has_address(self):
        return self.user_addresses.all().exists()
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_addresses')
    
    # Add address fields
    name = models.CharField(max_length=120)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone = PhoneNumberField('Address Phone', blank=True, null=True)
    country = CountryField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} - {self.phone} - {self.street_address} - {self.city} - {self.country}'
    
         
        
    
class CustomResizeToFill(Resize):
    def process(self, img):
        if self.height is None:
            self.height = img.height

        if self.width is None:
            self.width = img.width

        img.thumbnail((self.width, self.height), Image.BICUBIC)

        return img

    
class Profile(models.Model):
    # It is beeing created autometically during signup by using signal.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    avatar = ProcessedImageField(upload_to='profile_photo',
                    processors=ProcessorPipeline([CustomResizeToFill(200, 200)]),
                    format='JPEG',
                    options={'quality': 60}, blank=True, null=True)
    about = models.TextField('About Me', max_length=500, blank=True, null=True)
    
    
    location = models.CharField('My Location', max_length=30, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)  
    
    def __str__(self):
        return 'Profile for ' +  str(self.user.email)  
    


