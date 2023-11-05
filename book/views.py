import random
import string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.urls import reverse
from accounts.forms import AddressForm
from accounts.models import Address, User
from core.agent_helper import get_location_info
from core.context_processor import site_data
from payment_method.gateways.base import PaymentGatewayBase
from payment_method.utils import get_payment_method_class
from payment_method.views import create_pdf_invoice
from .forms import AddressSelectionForm, PaymentForm, PaymentGatewayForm, QuantityForm
from book.models import Book, BookOrder, BookOrderItem, OrderTransaction
from payment_method.gateways import active_payment_methods
from django.contrib import messages
from django.utils import timezone

def home(request):
    template = 'book/home.html'
    books = Book.objects.filter(is_active = True).order_by('-updated_at')    
    quantity_form = QuantityForm(request=request, book=None)
  
    site = site_data()
    site['title'] = 'All Books'
    
    site['description'] = 'Explore your registered book list - your curated collection of books. Easily manage, track, and organize your literary treasures in one place. Get organized with your reading journey.'

    context = {      

        'site_data' : site,   
        'books' : books,
        'quantity_form' : quantity_form   

        
    }  
    
    response = render(request, template, context=context)
    response['X-Robots-Tag'] = 'index, follow'
    return response 
    
  

def book_details(request, slug):
    template = 'book/book_details.html'
    book = get_object_or_404(Book, slug=slug)
    quantity_form = QuantityForm(request=request, book=book)
    site = site_data()
    site['title'] = book.title
    truncated_string = strip_tags(book.description)[:160]
    site['description'] = truncated_string
    site['og_image'] = request.build_absolute_uri(book.main_image.url)
    context = {      

        'site_data' : site,   
        'book' : book,
        'quantity_form' : quantity_form   
        
    } 
    
    response = render(request, template, context=context)
    response['X-Robots-Tag'] = 'index, follow'
    return response  
    
  

def create_unique_username(email):
    # Extract the username part (before @) from the email
    username = email.split('@')[0]
    # Append a counter to the username to make it unique
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{email.split('@')[0]}_{counter}"
        counter += 1
    return username

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def get_or_create_user(email, phone):
    site = site_data()
    try:
        # Check if a user with the same email already exists
        existing_user = User.objects.get(email=email)       
        return existing_user  # User already exists, return the existing user
    
    except User.DoesNotExist:
        # Generate a unique username and a random password
        unique_username = create_unique_username(email)
        random_password = generate_random_password()

        # Create the user
        user = User.objects.create(username=unique_username, email=email, phone=phone)
        user.set_password(random_password)
        user.save()
        site_name = site.get('name')
        domain = site.get('domain')
        
        # Send an email to the user
        subject = f'{site_name} | Your New Account Information'
        message =   f'Hello {user.email},\n\n'
        message +=  f'Your account has been created successfully with an order successfully placed on {domain}. \n\n' 
        message +=  f'Your initial password is: {random_password}. \n\n' 
        message +=  f'Please change this password! Alternatively you may keep record of this password.\n\n'                     
        message +=  f'Please login to your account and change your password immediately for security reasons.\n\n' 
        message +=  f'Best Regards...\n\n' 
        message +=  f'SINCEHENCE TEAM\n\n' 

        from_email = settings.DEFAULT_FROM_EMAIL     
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        
        return user

def buy_book(request, id):
    book = get_object_or_404(Book, pk=id)
    quantity_form = QuantityForm(request=request, book=book)

    template = 'book/buy_book.html'
    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        
        quantity_form = QuantityForm(request=request, book=book, data=request.POST)
        
        if form_name == 'quantity_form':
            if quantity_form.is_valid():
                quantity = quantity_form.cleaned_data['quantity']
                email = quantity_form.cleaned_data['email']
                phone = quantity_form.cleaned_data['phone']                
                user = get_or_create_user(email, phone)              
                    
             
                order = BookOrder.objects.create(
                    amount = int(quantity) * book.price,
                    customer = user,
                    order_status = 'pending'                       
                )
                
                BookOrderItem.objects.create(
                    item = book,
                    order = order,
                    sale_price = book.price,
                    quantity = int(quantity),
                    total_amount = int(quantity) * book.price,                    
                )
                return redirect(reverse('book:book_order_payment', args=[int(order.id)]))
                
                
            else:
                return render(request, template, context={ 'quantity_form' : quantity_form, 'book' : book})
    
    
    context = {
        'book' : book,
        'quantity_form' : quantity_form
        
    }
    return render(request, template, context)

def get_valid_payment_gateways(request, amount):
    location_data = get_location_info(request)
    ip = location_data.get('ip')    
    if ip == '127.0.0.1':
        user_country = 'BD'
    else:
        user_country = location_data.get('country')
        
    payment_gateways = {}
    for payment_method in active_payment_methods:
        
        if isinstance(payment_method, PaymentGatewayBase): 
            allowed_amount_min, allowed_amount_max, allowed_amount_any = payment_method.allowed_amount()
            allowed_countries, allowed_any_country = payment_method.allowed_countries()
            # Check if the order amount is within the allowed range
            if allowed_amount_min <= amount <= allowed_amount_max or allowed_amount_any:
                # Check if the user is browsing from an allowed country
                if user_country in allowed_countries or allowed_any_country:  
                    payment_gateways[payment_method.get_gateway_name()] = payment_method.get_help_text()
         
              
    return payment_gateways

def book_order_payment(request, id):
    template = 'book/book_order_payment.html'
    
    order = get_object_or_404(BookOrder, id=id)
    
    books_avialable_countries = order.book_order_items.all().values_list('item__avialable_country', flat=True)

    
    
    payment_gateways = get_valid_payment_gateways(request, order.amount)   
    payment_gateways_form = PaymentGatewayForm(payment_gateways=payment_gateways)  
    
    if order.customer.has_address:
        address_form = AddressSelectionForm(order.customer)
    else:
        address_form = AddressForm()
    
    
    if request.method == 'POST':       
        if 'selected_address' in request.POST:
            address_form = AddressSelectionForm(order.customer, request.POST)
            context = {
                'order' : order,
                'address_form' : address_form,
                'payment_gateways_form' : payment_gateways_form
                
            }
            if address_form.is_valid():
                address_id = address_form.cleaned_data['selected_address']
                address = Address.objects.get(id = int(address_id))
                
                if address.country not in books_avialable_countries:
                    messages.warning(request, 'This book is not avialable in selected country! Please select diferent address.')
                    return render(request, template, context)
            else:                
                return render(request, template, context)
        else:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = order.customer
                address.save()
            else:
                context = {
                        'order' : order,
                        'address_form' : address_form,
                        'payment_gateways_form' : payment_gateways_form
                        
                    }
                return render(request, template, context)   
   
        order.delivery_address = address    
        order.save()
        
        
        
        payment_gateways_form = PaymentGatewayForm(payment_gateways=payment_gateways, data=request.POST)       
        
        
        if payment_gateways_form.is_valid():
            selected_gateway = payment_gateways_form.cleaned_data['payment_gateway']      
        else:
            context = {
                'order' : order,
                'address_form' : address_form,
                'payment_form' : payment_gateways_form
                
            }
            return render(request, template, context)
        
        cls = get_payment_method_class(selected_gateway)   
        
        gateway_dict = cls().get_required_dict                
        gateway_dict['order_id'] = order.id          
            
        payment_url = cls().create_payment(**gateway_dict)

        
        return redirect(payment_url)
        
    
    context = {
        'order' : order,
        'address_form' : address_form,
        'payment_gateways_form' : payment_gateways_form
        
    }
    return render(request, template, context)


def get_add_address_form(request):
    template = 'book/get_add_address_form.html'
    address_form = AddressForm()
    context = {
        'address_form' : address_form,       
    }
    return render(request, template, context)

def get_select_address_form(request, id):
    template = 'book/get_add_address_form.html'
    user = get_object_or_404(User, id=id)
    address_form = AddressSelectionForm(user)
    context = {
        'address_form' : address_form,       
    }
    return render(request, template, context)


def update_payment(request, id):
    template = 'book/update_payment.html'
    order = get_object_or_404(BookOrder, id=id)
    
    if order.customer == request.user:
        pass
    else:
        raise Http404
    
    invoice = order.invoice
     
    if int(order.trans_amount) >= int(order.amount):
        invoice.paid = True
        invoice.save()
        return HttpResponse('<p class="text-danger">It appears that the payment for your order has been successfully processed. If you believe this is in error or have any concerns, please do not hesitate to contact our sales team at sales@sankarmath.org. Your honesty and feedback are greatly appreciated, and we are here to assist you promptly. </p>')
    
    
    payment_form = PaymentForm()    
    if request.method == 'POST':  
        payment_form = PaymentForm(request.POST, request.FILES)
        if payment_form.is_valid():
            invoice.paid = True
            invoice.paid_on = timezone.now()
            invoice.save()
            
            transaction = payment_form.save(commit=False)            
            transaction.order = order
            transaction.gateway = invoice.gateway           
            transaction.save()
            
            order.order_status = 'processing'
            order.save()
            
                     
            
            
            return HttpResponse('<p class="text-success">Invoice Payment Updated!</p>')
        else:
        
            context = {
                'order' : order,       
                'payment_form' : payment_form,  
                
            }
            return render(request, template, context)
        
    context = {
        'order' : order, 
        'payment_form' : payment_form,   
        
    }

    
    return render(request, template, context)
    
    
     

