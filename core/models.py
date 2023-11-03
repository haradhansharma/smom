from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.sites.managers import CurrentSiteManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import activate, gettext_lazy as _

from django.core.validators import FileExtensionValidator
from django.contrib.sites.models import Site

# from core.mixins import (
#     TitleAndSlugModelMixin, 
#     CreatorModelMixin,    
#     SitesModelMixin,
#     IsActiveModelMixin,
#     MenuModelMixin,
#     SaveFromAdminMixin,
#     DateFieldModelMixin,
#     ) 

from .agent_helper import get_client_ip

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.db import models

from django.db.models.signals import post_save, post_delete

# class UserActivityLog(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     action = models.CharField(max_length=10)  # 'Added', 'Updated', 'Deleted'
#     model_name = models.CharField(max_length=100)
#     object_id = models.PositiveIntegerField()
#     details = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.action} {self.model_name} ({self.object_id})"

#     class Meta:
#         ordering = ['-timestamp']



class ImageRecords(models.Model):
    obj_id = models.BigIntegerField()
    obj_model = models.CharField(max_length=150)
    obj_field = models.CharField(max_length=150)
    obj_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) 





# Create your models here.
class ExSite(models.Model):    
    site = models.OneToOneField(Site, primary_key=True, verbose_name='site', on_delete=models.CASCADE)   
    site_description = models.TextField(max_length=500)
    site_meta_tag =models.CharField(max_length=255)
    site_favicon = models.ImageField(upload_to='site_image/')
    site_logo = models.ImageField(upload_to='site_image/')
    trademark = models.ImageField(upload_to='site_image/')
    slogan = models.CharField(max_length=150, default='')
    og_image = models.ImageField(upload_to='site_image/')
    mask_icon = models.FileField(upload_to='site_image/', validators=[FileExtensionValidator(['svg'])])    
    facebook_link = models.URLField()
    twitter_link = models.URLField()
    linkedin_link = models.URLField()    
    instagram_link = models.URLField()      
    email = models.EmailField()
    location = models.TextField()
    phone = models.CharField(max_length=16)
    
    
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()  
    
    
# class ContactMessage(models.Model):   
#     name = models.CharField(max_length=255)
#     phone_number = PhoneNumberField()
#     email = models.EmailField()
#     subject = models.CharField(max_length=251)  
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.name} ({self.email})'
    
    
# class Action(models.Model):
#     VIEW = 'view'
#     LIKE = 'like'
#     ACTION_TYPES = (
#         (VIEW, 'View'),
#         (LIKE, 'Like')
#     )
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,db_index=True)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')   
#     user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
#     ip_address = models.GenericIPAddressField(null=True, blank=True)
#     action_type = models.CharField(max_length=4, choices=ACTION_TYPES, default=VIEW,db_index=True)
#     timestamp = models.DateTimeField(auto_now_add=True, null=True)  
    
    
# class Category(
#     TitleAndSlugModelMixin, 
#     CreatorModelMixin,    
#     SitesModelMixin,
#     IsActiveModelMixin,
#     MenuModelMixin,
#     DateFieldModelMixin,
#     models.Model,
#     SaveFromAdminMixin,    
    
    
#     ):
    
#     icon = models.CharField(_('FA Icon'), max_length=250, help_text=_('HTML Fontawesoome icon'), default='<i class="fa-solid fa-calendar-check"></i>')
#     description = models.TextField()
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Parent'))        
#     add_to_cat_menu = models.BooleanField(default=True)  
    

#     def __str__(self):
#         return self.title
    
#     class Meta:
#         verbose_name = _('Category')
#         verbose_name_plural = _('Categories')    
#         ordering = ['-created_at'] 
        
#     def get_absolute_url(self):
#         return reverse('core:category_detail', args=[str(self.slug)])
    
   
#     @property
#     def have_items(self):
#         if self.blogs_category.filter(status = 'published').exists() or self.pages_category.filter(status = 'published').exists():
#             return True
#         return False
        
    
    






# class UserCMSManager(models.Manager):
#     def foruser(self, user):
#         # Filter pages based on the provided user
#         return self.filter(creator=user)
    

# class OurService(    
#     models.Model,  
#     ):
#     title = models.CharField(max_length=100)
#     image = models.ImageField(_('Feature Image'), upload_to='blog/our_service/')
#     body = models.TextField(verbose_name=_('Body'))
    
#     def __str__(self):
#         return self.title  

#     class Meta:
#         verbose_name = 'Our Service'
#         verbose_name_plural = 'Our Service'        
  
    
    
    
    
# class Page(   
#     TitleAndSlugModelMixin, 
#     IsActiveModelMixin,
#     MenuModelMixin,
#     SitesModelMixin,  
#     CreatorModelMixin, 
#     DateFieldModelMixin,
#     models.Model,   
#     SaveFromAdminMixin,    
    
    
#     ):  
    
#     STATUS_CHOICES = (
#         ('draft', _('Draft')),
#         ('published', _('Published')),
#         ('unpublished', _('UnPublished')),        
#     )    
#     top_banenr = models.ImageField(_('Top Banner'), upload_to='blog/top_banenr/', null=True, blank=True)
#     top_tagline = models.CharField(max_length=40)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Parent'))
#     body = models.TextField(verbose_name=_('Body'))
#     meta_description = models.TextField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')   
#     actions = GenericRelation(Action)
#     consent_required = models.BooleanField(default=False)
#     objects = models.Manager()  # Fallback manager to query all pages
  
    
#     # Manager for filtering pages based on user to call Page.userpages.foruser(request.user)
#     userpages = UserCMSManager()
    
#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('core:page_detail', args=[str(self.slug)])

#     class Meta:
#         verbose_name = 'Page'
#         verbose_name_plural = 'Pages'        
#         ordering = ['-created_at']           
            
#     def view(self, request):
#         # create a new action object for this view
#         Action.objects.create(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             user=request.user if request.user.is_authenticated else None,
#             ip_address=get_client_ip(request),
#             action_type=Action.VIEW
#         )       


#     def like(self, request):
#         Action.objects.create(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             user=request.user if request.user.is_authenticated else None,
#             ip_address=get_client_ip(request),
#             action_type=Action.LIKE
#         )
        
#     def dislike(self, request):
#         Action.objects.get(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             user=request.user if request.user.is_authenticated else None,
#             ip_address=get_client_ip(request),
#             action_type=Action.LIKE
#         ).delete()
        
#     @property
#     def total_view(self):
#         total = Action.objects.filter(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             action_type=Action.VIEW
#         ).count()
#         return total
    
#     @property
#     def total_like(self):
#         total = Action.objects.filter(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             action_type=Action.LIKE
#         ).count()
#         return total
    
       
        
    
        
        
# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager, self).get_queryset().filter(status='published')
    
# class UnPublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(UnPublishedManager, self).get_queryset().filter(status='unpublished')
    
# class DraftManager(models.Manager):
#     def get_queryset(self):
#         return super(DraftManager, self).get_queryset().filter(status='draft').order_by('-updated_at')
        
        
# class Blog(
#     TitleAndSlugModelMixin,
#     MenuModelMixin,
#     SitesModelMixin,
#     CreatorModelMixin, 
#     DateFieldModelMixin,
#     models.Model,
#     SaveFromAdminMixin,    
    
    
#     ):
#     STATUS_CHOICES = (
#         ('draft', _('Draft')),
#         ('published', _('Published')),
#         ('unpublished', _('UnPublished')),        
#     )
    
#     feature = models.ImageField(_('Feature Image'), upload_to='blog/feature_image/', null=True, blank=True)
    
    
#     categories = models.ManyToManyField(
#         Category,
#         blank=True,
#         db_index=True,
#         verbose_name=_('Categories'),
#         related_name='blogs_category'
      
#     )  
    
#     body = models.TextField(verbose_name=_('Body'))  
        
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)   
#     actions = GenericRelation(Action)
    
    
    

    
    
#     def view(self, request):
#         # create a new action object for this view
#         Action.objects.create(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             user=request.user if request.user.is_authenticated else None,
#             ip_address=get_client_ip(request),
#             action_type=Action.VIEW
#         )       


#     def like(self, request):
#         Action.objects.create(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             user=request.user if request.user.is_authenticated else None,
#             ip_address=get_client_ip(request),
#             action_type=Action.LIKE
#         )
        
#     def dislike(self, request):
#         Action.objects.get(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             user=request.user if request.user.is_authenticated else None,
#             ip_address=get_client_ip(request),
#             action_type=Action.LIKE
#         ).delete()
        
        
#     @property
#     def total_view(self):
#         total = Action.objects.filter(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             action_type=Action.VIEW
#         ).count()
#         return total
    
#     @property
#     def total_like(self):
#         total = Action.objects.filter(
#             content_type=ContentType.objects.get_for_model(self),
#             object_id=self.pk,
#             action_type=Action.LIKE
#         ).count()
#         return total      
    
    
      
#     @property  
#     def get_content_type(self):
#         return ContentType.objects.get_for_model(self)
    
    
#     objects = models.Manager()#default manager
#     published = PublishedManager()#Cutom Manager
#     unpublished = UnPublishedManager()#Cutom Manager    
#     draft = DraftManager()#Cutom Manager
    
#     # Manager for filtering pages based on user to call Blog.userblogs.foruser(request.user)
#     userblogs = UserCMSManager()
    
#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('core:blog_details', args=[str(self.slug)])       

#     def like_or_dislike_url(self):
#         return reverse('core:like_or_dislike', args=[int(self.get_content_type.id), str(self.id)])        
    
#     class Meta:
#         verbose_name = 'Blog'
#         verbose_name_plural = 'Blogs'
#         ordering = ['-created_at']
        


       
  
# def validate_file_size(value):
#     filesize= value.size

#     if filesize > 5*1024*1024:
#         raise ValidationError(_("The maximum file size that can be uploaded is 5MB"))
      
        
