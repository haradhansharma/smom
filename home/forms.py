from django import forms
from .models import FeatureRequest
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField

class FeatureRequestForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='') 
    class Meta:
        model = FeatureRequest
        fields = ['wated_title', 'wanted', 'wanted_name', 'wanted_by']
        widgets = {
            'wated_title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write a title'}),
            'wanted': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder':'Write what features do you want. e.g: Ashrom searching facilities'}),
            'wanted_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your name'}),
            'wanted_by': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Write your email eg: example@email.com'}),
        }
        labels = {
            'wated_title' : '',
            'wanted' : '',
            'wanted_name' : '',
            'wanted_by' : ''           
        }