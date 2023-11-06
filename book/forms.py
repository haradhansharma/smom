from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, RegionalPhoneNumberWidget, PhonePrefixSelect

from accounts.models import Address
from book.models import OrderTransaction


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, 
        initial=1, 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg', 
                'placeholder': 'e.g.: Enter required Quantity.'
                }
            ), 
        help_text=f'<small class="text-success">Quantity you want to buy. There is quantitywise discounts.</small>', 
        label='Quantity'
        )
    
    def __init__(self, request, book, *args, **kwargs):        
        super(QuantityForm, self).__init__(*args, **kwargs)
        self.book = book
        self.request = request 
           
        if book is not None:
            discount_dict = dict(self.book.get_discount_list)
            modified_discount_dict = dict()
            for key, value in discount_dict.items():   
                modified_key = f'Quantity over {key}'
                modified_value = f'Discount {value}%'
                modified_discount_dict[modified_key] = modified_value
                        
        
            # Update the help_text for the quantity field
            self.fields['quantity'].help_text = f'<small class="text-success">Quantity you want to buy. There is quantitywise discounts: {modified_discount_dict}</small>'
        
        
        # Check if the user is not logged in
        if not self.request.user.is_authenticated or (self.request.user.is_authenticated and not self.request.user.email):
            self.fields['email'] = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'e.g.: example@email.com'}), help_text=f'<small class="text-success">Your email address. Using this email will create an account if not exists.</small>', label='Email')

        if not self.request.user.is_authenticated or (self.request.user.is_authenticated and not self.request.user.phone):
            self.fields['phone'] = PhoneNumberField(required=True, widget=PhoneNumberPrefixWidget(initial='BD', attrs={'placeholder': 'Enter phone number after country code', 'aria-label': 'phone_number'}, number_attrs={'class': 'form-control'}, country_attrs={'class': 'input-group-text'}), help_text=f'<small class="text-success">Your phone number. Select country code first.</small>', label='Mobile Phone')
            
    def clean_quantity(self):
        from book.views import get_valid_payment_gateways
        quantity = self.cleaned_data.get('quantity')
        if self.book is not None:
            if quantity is not None:
                total_price = int(quantity) * self.book.cal_price(quantity)            
                valid_gateways = get_valid_payment_gateways(self.request, total_price)            
                if valid_gateways:
                    pass
                else:
                    raise forms.ValidationError("Sorry, we can't process your order right now due to payment limitations. We're working to improve this. Please reduce the quantity or try again later.")
        return quantity
 
    
class AddressSelectionForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(AddressSelectionForm, self).__init__(*args, **kwargs)
        user_addresses = user.user_addresses.all()
        self.fields['selected_address'] = forms.ChoiceField(
            choices=[(address.id, address) for address in user_addresses],
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='Select Delivery Address'
        )
        

class PaymentGatewayForm(forms.Form):
    payment_gateway = forms.ChoiceField(
        choices=[], 
        widget=forms.RadioSelect(), 
        required=True, 
        error_messages={'required': 'Please select a Payment Gateway'},
        label='' 
    )

    def __init__(self, payment_gateways, *args, **kwargs):
        super(PaymentGatewayForm, self).__init__(*args, **kwargs)
        self.fields['payment_gateway'].choices = [(key, value) for key, value in payment_gateways.items()]    
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = OrderTransaction
        fields = ['amount', 'trxID', 'mobile', 'screenshoot']
        
        widgets = {
            'amount' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Paid Amount'}),
            'trxID' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Transacion ID you receive', 'row': 5}),
            'mobile' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter  mobile number that amount paid from'}),
            'screenshoot' : forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Enter screenshoot'}),
            
            
        }
        labels = {
            'amount' : 'Paid Amount',
            'trxID' : 'TrxID',
            'mobile' : 'Mobile Number',
            'screenshoot' : 'Add Photo or PDF for transaction receipt!'
            
        }
        
