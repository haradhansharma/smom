from django.http import JsonResponse 
from core.context_processor import site_data

import logging
log = logging.getLogger('log')

    
def webmanifest(request):
    site = site_data()      
    icons = []    
    ic192 = {
        "src": site.get('og_image'),
        "sizes": "192x192",
        "type": "image/png"        
    }
    
    icons.append(ic192)   
    ic512 = {
        "src": site.get('og_image'),
        "sizes": "512x512",
        "type": "image/png"        
    }
    icons.append(ic512)    
    data = {
        'name' : site['name'],
        'short_name' : site['name'],
        'icons' : icons,        
        "theme_color": "#000000",
        "background_color": "#000000",
        "display": "standalone"        
    }
    
    return JsonResponse(data, safe=False)

