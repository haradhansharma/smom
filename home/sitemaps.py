from django.contrib import sitemaps
from django.urls import reverse

from asrams.models import Asram
from book.models import Book
from .models import *
from django.conf import settings
from django.utils import timezone
from django.db.models import Count


class StaticSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'home:home', 
            'accounts:home', 
            'accounts:signup', 
            'accounts:login', 
            'asrams:home', 
            'book:home', 
            ] 
    
    def lastmod(self, obj):
        return timezone.now()
        
    def location(self, item):
        return reverse(item)   
    
class AsramSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.9    

    def items(self):
        return Asram.objects.filter(is_active = True)[:10]
    
    def lastmod(self, obj):
        return obj.created_at
        
    def location(self, obj):
        return obj.get_absolute_url()
    
class BookSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 1    

    def items(self):
        return Book.objects.filter(is_active = True)[:10]
    
    def lastmod(self, obj):
        return obj.created_at
        
    def location(self, obj):
        return obj.get_absolute_url()
    

    

    

    

    

    

               
    