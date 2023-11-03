from django.http import HttpResponse
from django.shortcuts import redirect, render
from book.forms import QuantityForm

from core.context_processor import site_data
from home.forms import FeatureRequestForm
from home.models import FeatureRequest
from book.models import Book

def home(request):
    template = 'home/home.html'
    features = FeatureRequest.objects.all().order_by('-requested')[:15]
    books = Book.objects.filter(is_active = True).order_by('-updated_at')
    quantity_form = QuantityForm(request=request, book=None)
    if request.method == 'POST':
        form = FeatureRequestForm(request.POST)
        if form.is_valid():
            form.save()
            features = FeatureRequest.objects.all().order_by('-requested')[:15]
            return render(request, 'includes/feature_list.html', context={'features' : features, 'form' : FeatureRequestForm()})
        else:      
            return render(request, 'includes/feature_list.html', context={'features' : features, 'form' : form})
    else:
        form = FeatureRequestForm()
    
    site = site_data()
    site['title'] = 'Home'    
    site['description'] = "Embark on a spiritual journey with SankarMath - o - Mission, dedicated to spreading the teachings of Babamani. Explore profound wisdom, pre-order spiritual books, and support our mission's growth. Join us on a path of enlightenment and positive change"

    context = {      
        'features' : features,
        'site_data' : site,   
        'form' : form,
        'books' : books,
        'quantity_form' : quantity_form
    }  
    
    response = render(request, template, context=context)
    response['X-Robots-Tag'] = 'index, follow'
    return response  
    



