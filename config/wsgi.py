# Import necessary modules
import os
import sys

# Check the operating system name
if os.name != 'nt':
    # On non-Windows systems, configure the Python path and Django settings
    sys.path.insert(0, '/home/veerera/smomenv/lib/python3.9/site-packages')
    from django.core.wsgi import get_wsgi_application
    sys.path.insert(1, '/home/veerera/sankarmath_html')
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
    application = get_wsgi_application()        
else:   
    # On Windows systems, configure Django settings 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
