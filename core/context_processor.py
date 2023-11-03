import re
from django.conf import settings
from .models import ExSite    
from django.core.cache import cache
from .models import *
from .menus import (
    # category_menus,
    # page_menus,
    footer_menu,
    header_menu,
    user_menu

)
# from .helper import get_consent_pages, get_currencies

def site_data():
    data = cache.get('site_data')
    if data is not None:
        return data

    site = ExSite.on_site.get()
    data = {
        'name' : site.site.name,
        'domain' : site.site.domain,
        'description': site.site_description,
        'author' : 'Haradhan Sharma',
        'meta_tag' : site.site_meta_tag,
        'favicon': site.site_favicon.url,
        'mask_icon': site.mask_icon.url,
        'logo': site.site_logo.url,
        'trademark': site.trademark.url,       
        'slogan': site.slogan,
        'og_image': site.og_image.url,
        'facebook_link': site.facebook_link,
        'twitter_link': site.twitter_link, 
        'linkedin_link': site.linkedin_link,  
        'instagram_link': site.instagram_link,         
        'email': site.email,   
        'location': site.location,   
        'phone': site.phone,   
         
    }

    cache.set('site_data', data, timeout=3600)

    return data


def str_list_frm_path(request):   
    path = request.path

    # Split the path at each special character using a regular expression
    path_segments = re.split(r'[-_&/]', path)

    # Remove any empty strings from the list of path segments
    path_segments = [s for s in path_segments if s]
    return path_segments


def check_consent(request, consent_urls):
  
    if 'concent_given' not in request.session:
        request.session['concent_given'] = 'False'
         
    if request.session.get('concent_given') == 'True':        
        consent_given = True        
    elif request.path in consent_urls:
        consent_given = True                     
    else:        
        consent_given = False        
        
    return consent_given






def core_con(request):  
    # consent_pages = get_consent_pages() 
    
    # consent_urls = []
    
    # for cp in consent_pages:        
    #     consent_urls.append(cp.get_absolute_url())       
        
    
        
    # consent_given = check_consent(request, consent_urls)
    
        
    context = {   
        # 'consent_given' : consent_given,               
        # 'category_menus' : category_menus(request),
        # 'page_menus' : page_menus(request),
        'footer_menu' : footer_menu(request),
        'header_menu' : header_menu(request),
        'site_data' : site_data(),
        # 'consent_pages' : consent_pages,
        # 'currencies' : get_currencies(),
        'user_menu' : user_menu(request)
        
 
     
    }
    
    return context