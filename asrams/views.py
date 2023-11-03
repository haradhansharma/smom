from book.forms import QuantityForm
from book.models import Book
from core.context_processor import site_data
from home.forms import FeatureRequestForm
from .forms import AsramForm  # Import your AsramForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import *

def home(request):
    template = 'asrams/home.html'
    asrams = Asram.objects.all().order_by('name')    
    books = Book.objects.filter(is_active = True).order_by('-updated_at')    
    quantity_form = QuantityForm(request=request, book=None)    
        
    site = site_data()
    site['title'] = 'Enlisted Asrams'    
    site['description'] = 'Explore our registered Enlisted Asrams for a supportive and enriching community. Find resources, events, and connections to enhance your spiritual journey.'
    
    context = {         
        'site_data' : site,   
        'asrams' : asrams,
        'books' : books,
        'quantity_form' : quantity_form   
    }  
    
    response = render(request, template, context=context)
    response['X-Robots-Tag'] = 'index, follow'
    return response 



def create_asram(request):
    template = 'asrams/create_asram.html'
    if request.method == 'POST':
        form = AsramForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to create a new Asram instance
            form.save()
            return redirect('asrams:home')
    else:
        form = AsramForm()

    site = site_data()
    site['title'] = 'Enlist Asram'    
    site['description'] = 'Enlist or create Asram with ease. Join our community, share your spiritual journey, and connect with like-minded individuals on your path to self-discovery.'

    context = {        
        'site_data' : site,   
        'form' : form   
    } 
    
    response = render(request, template, context=context)
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response   
    


def asram_detail(request, slug):
    template = 'asrams/asram_detail.html'
    asram = get_object_or_404(Asram, slug=slug)
    books = Book.objects.filter(is_active = True).order_by('-updated_at')    
    quantity_form = QuantityForm(request=request, book=None)
    
    site = site_data()
    site['title'] = asram.name   
    site['description'] = asram.about
    site['og_image'] = asram.avatar
    context = {     
       
        'site_data' : site,   
        'books' : books,
        'quantity_form' : quantity_form   
      
    } 
    
    response = render(request, template, context=context)
    response['X-Robots-Tag'] = 'index, follow'
    return response    
    
  
    