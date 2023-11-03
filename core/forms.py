from django import forms
# from .models import ContactMessage
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, RegionalPhoneNumberWidget, PhonePrefixSelect
import re

from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField

# class BlogSearchForm(forms.Form):
#     search_query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':"Search ..."}))
    


# class ContactUsForm(forms.ModelForm):   
#     captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox)  
    
#     class Meta:
#         model = ContactMessage
#         fields = ['name', 'phone_number', 'email', 'subject', 'message']                
#         widgets = {                      
#             'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Name', 'aria-label':'Name',  }),  
#             'phone_number' : PhoneNumberPrefixWidget(initial='GB', attrs={'placeholder': 'Enter phone number', 'aria-label':'phone_number'}, number_attrs ={'class':'form-control'} , country_attrs={'class': 'input-group-text'}) ,
#             'email': forms.EmailInput(attrs={'class':'form-control','placeholder': 'Email Address',  'aria-label':'email' , }),                
#             'subject': forms.TextInput(attrs={'class':'form-control','placeholder': 'Subject',  'aria-label':'subject',  }),            
#             'message': forms.Textarea(attrs={'class':'form-control','rows':'5','placeholder': 'Message', 'aria-label':'message', }), 
#         }        
#         PhoneNumberPrefixWidget(attrs={'placeholder': 'Enter phone number'})
        
#     def clean_message(self):
#         """
#         Custom validation for the 'message' field.
#         """
#         message = self.cleaned_data.get('message')
        
        
#         # Find all URLs using a comprehensive regex pattern
#         urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message)

        
        
#         # Add your custom validation logic here.    
#         if len(urls) > 0:
#             raise forms.ValidationError("Please remove URL from the message.")
#         return message