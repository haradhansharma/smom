
from django.urls import path, include
from .views import *


app_name = 'payment_method'

urlpatterns = [
    # path('stripe-webhook/', stripe_webhook,  name='stripe_webhook'),
    path('bkash-manual/<int:order_id>', bkash_manual,  name='bkash_manual'),
    path('rocket-manual/<int:order_id>', rocket_manual,  name='rocket_manual'),
    path('exim-bd/<int:order_id>', exim_bd,  name='exim_bd'),
    
    
    
    
]
