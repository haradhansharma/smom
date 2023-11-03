from django import forms
from django_countries.fields import CountryField

from asrams.models import Asram

class AsramForm(forms.ModelForm):

    class Meta:
        model = Asram
        fields = ['name', 'banner', 'street_address', 'city', 'postal_code', 'country', 'about']
        
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asram Name. eg: Sankarmath O Mission'}),
            'street_address' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address. eg: 45, abcd road, xyz block'}),
            'city' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City. Eg: Dhaka'}),
            'postal_code' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code. EG: 1100'}),
            'country' : forms.Select(attrs={'class': 'form-select'}),            
            'banner' : forms.FileInput(attrs={'class': 'form-control'}),
            'about' : forms.Textarea(attrs={'style': 'height:150px;', 'class': 'form-control'}),
            
            
            
        }
        labels = {
            'name' : 'Asram Name',
            'street_address' : 'Street address',
            'city' : 'City',
            'postal_code' : 'Postal Code',
            'country' : 'Country',            
            'banner' : 'Banner',
            'about' : 'About the asram',
            
            
        }
        
