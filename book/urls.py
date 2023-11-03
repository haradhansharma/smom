
from django.urls import path, include
from .views import *
# from django.contrib.sitemaps.views import sitemap
# from .sitemaps import *
from django.views.generic.base import TemplateView

app_name = 'book'


urlpatterns = [
    # path('sitemap.xml', sitemap, {'sitemaps': sitemap_list}, name='django.contrib.sitemaps.views.sitemap'),      
    path('', home, name='home'),
    path('<str:slug>', book_details, name='book_details'),    
    path('buy/<int:id>/', buy_book, name='buy_book'),
    path('buy/payment/<int:id>/', book_order_payment, name='book_order_payment'),
    path('get-add-address-form/', get_add_address_form, name='get_add_address_form'),
    path('get-select-address-form/<uuid:id>', get_select_address_form, name='get_select_address_form'),
    
    
    
    
    
    # path('contact/', contact, name='contact'),    
    # path('b/<str:slug>', blog_detail, name='blog_details'),
    # path('latest/blogs/', latest_blogs, name='latest_blogs'),       
    # path('<str:username>/blogs/', user_blogs, name='user_blogs'), 
    # path('category/<str:slug>', category_detail, name='category_detail'),    
    # path('archive/<int:year>/<int:month>', archive_detail, name='archive_detail'),   
    # path('p/<str:slug>', page_detail, name='page_detail'),   
    
]
