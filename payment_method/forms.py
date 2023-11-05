from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, RegionalPhoneNumberWidget, PhonePrefixSelect

from accounts.models import Address
from book.models import OrderTransaction


class ConfirmForm(forms.Form):      
    agree = forms.BooleanField(label="I am agree to pay acording to the instruction to selected gateway!", label_suffix='', required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    
    