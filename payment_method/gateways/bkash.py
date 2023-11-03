import os
import sys

from django.urls import reverse
from .base import PaymentGatewayBase

class bKashPaymentGateway(PaymentGatewayBase):
    def __init__(self):
        # Implement the bKash-specific initialization logic here
        # ...
        pass
    
    def allowed_amount(self):
        min = 0
        max = 10000
        any = False
        return min, max, any
    
    def allowed_countries(self):
        countries = ['BD']
        any = False
        return countries, any
    
    def get_help_text(self):
        return f'bKash Manual'
    
    def get_gateway_instruction(self):
        message = f'This is gateway Message'
        return message
    
    @property
    def get_required_dict(self):
        dict = {
            'order_id': ''
        }
        return dict       

    def create_payment(self, **kwargs):        
        if not super().kwargs_is_valid(**kwargs):
            raise ValueError('Passed kwargs are not the same or have missing values!') 
        
        order_id = kwargs['order_id']        
        
        return reverse('payment_method:bkash_manual', args=[int(order_id)])
    
    def process_payment(self, payment_data):
        pass
    
    def get_supported_currencies(self):
        pass
    
    def get_payment_details(self, payment_id):
        pass
    
    