from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from book.forms import AddressSelectionForm, QuantityForm
from book.models import Book
# from shop.models import Order
# from shop.decorators import order_creator_required
from .models import *
from .forms import AddressForm, UserCreationFormFront, PasswordChangeForm, UserForm, ProfileForm, AvatarForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from core.context_processor import site_data
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView

@login_required
def pending_payments(request): 
    site = site_data() 
    site['title'] = f'Pending Payments'
    site['description'] = f'Update Payment information and confirm orders!'
    user = request.user
    
    search_query = request.GET.get('search', '')
    

    invoices = []  
    for order in user.orders:
        if order.trans_amount < order.amount:
            invoice = order.inv if order.inv is not None else None                    
            if invoice is not None:            
                if invoice.validity > timezone.now():
                    invoices.append(invoice)
           
     

    
    
    if search_query:
        filtered_list = [invoice for invoice in invoices if invoice.order.id == int(search_query)]   
    else:
        filtered_list = invoices
        
          
        
   
    context = {
        'user' : user,    
        'site_data' : site ,  
        'invoices' : filtered_list,
        'search_query': search_query,             
    }   
    
    response = render(request, 'registration/pending_payments.html', context = context)
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response 

@login_required
def delete_avatar(request):    
    user = request.user
    profile = user.profile
    profile.avatar.delete()
    profile.avatar = ''
    profile.save()    
    return HttpResponseRedirect(reverse('accounts:profile_setting', args=[user.id]))

@login_required
def profile_setting(request, id):  
    if id == request.user.id:   
        pass
    else:
        raise PermissionDenied      
    
    site = site_data() 
    site['title'] = f'Profile Settings'
    site['description'] = f'Take control of your online presence with our profile settings page. Customize your profile, privacy settings, and communication preferences to tailor your experience. Safeguard your data and manage your interactions effortlessly. Unlock the power of personalization at your fingertips'
   
    context = {
        "user":request.user,         
        'site_data' : site ,               
    }        
     
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)   
        avatar_form = AvatarForm(request.POST, request.FILES, instance=request.user.profile)
        	
        if 'user_form' in request.POST:   
            if user_form.is_valid():                
                user_form.save()
                messages.success(request,('Your profile was successfully updated!'))                
            else:
                messages.error(request, 'Invalid form submission.')  
                context.update({'avatar_form' : avatar_form})                 
              
                
        if 'profile_form' in request.POST:            	    
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request,('Your profile data was successfully updated!'))
            else:
                messages.error(request, 'Invalid form submission.')
                context.update({'profile_form' : profile_form})
               
                
        if 'avatar_form' in request.POST:   
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request,('Avatar Updated successfully!'))
            else:
                messages.error(request, 'Invalid form submission.')
                context.update({'user_form' : user_form})
        
        
                
        return HttpResponseRedirect(reverse('accounts:profile_setting', args=[request.user.id]))
                
    
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)    
    avatar_form = AvatarForm(instance=request.user.profile)     
    
    context.update({'user_form' : user_form})
    context.update({'profile_form' : profile_form})
    context.update({'avatar_form' : avatar_form})   
    
    
    response = render(request, 'registration/account_settings.html', context = context)
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response 

@login_required
def password_change(request):        
    
    site = site_data()     
    site['title'] = 'Change Password'
    site['description'] = 'Securely update your password on our platform. Protect your account with a new, strong password to ensure the safety of your personal information. Change password hassle-free and strengthen your online security today.'
    
    
    context = {
        "user":request.user,
        'site_data' : site ,
    }
    
    if request.method == "POST":        
        password_form = PasswordChangeForm(user=request.user, data=request.POST)        
        if password_form.is_valid():            
            password_form.save()            
            update_session_auth_hash(request, password_form.user)            
            messages.success(request,('Your password was successfully updated!')) 
        else:
            context.update({           
                "form":password_form,               
            })   
                    
        return HttpResponseRedirect(reverse('accounts:user_dashboard'))
    
    password_form = PasswordChangeForm(request.user)   
    context.update({           
                "form":password_form,               
            })
    response = render(request, 'registration/password_change_form.html', context = context)
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response 


class CustomPasswordResetCompleteView(PasswordResetCompleteView):    
   
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books 
        site = site_data()    
        site['title'] = 'Password reset completed'     
        site['description'] = 'Password reset successfully! Your account is now secure. Log in with your new credentials and regain access to your account. Stay protected with our secure password management tools.'     
        
        context['site_data'] = site
        # Create an HttpResponse object with your template
        response = self.render_to_response(context)

        # Set the X-Robots-Tag header in the HttpResponse object
        response['X-Robots-Tag'] = 'noindex, nofollow'
        return context
    

class CustomPasswordResetView(PasswordResetView):
    from .forms import PasswordResetForm
    
    #overwriting form class to take control over default django
    form_class = PasswordResetForm
    success_url = reverse_lazy("accounts:password_reset_done")
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        site = site_data()   
        site['title'] = 'Reset your password'
        site['description'] = 'Reset your password securely and regain access to your account with our user-friendly password reset form. Safeguard your data and follow a simple step-by-step process to create a new password. Experience hassle-free account recovery and ensure the protection of your valuable information. Reset your password now and get back to enjoying our platform with peace of mind'

        context['site_data'] = site
        # Create an HttpResponse object with your template
        response = self.render_to_response(context)

        # Set the X-Robots-Tag header in the HttpResponse object
        response['X-Robots-Tag'] = 'noindex, nofollow'
        return context
    

class CustomPasswordResetDoneView(PasswordResetDoneView):
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        site = site_data()   
        site['title'] = 'Password reset done'
        site['description'] = 'Password Reset Done - Your password has been successfully reset. '

        context['site_data'] = site
        # Create an HttpResponse object with your template
        response = self.render_to_response(context)

        # Set the X-Robots-Tag header in the HttpResponse object
        response['X-Robots-Tag'] = 'noindex, nofollow'
        return context
    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    from .forms import SetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")
    #overwriting form class to take control over default django
    form_class = SetPasswordForm
    
    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books  
        
        site = site_data()   
        site['title'] = 'Password reset confirm'
        site['description'] = 'Confirm your password reset. '

        context['site_data'] = site
        # Create an HttpResponse object with your template
        response = self.render_to_response(context)

        # Set the X-Robots-Tag header in the HttpResponse object
        response['X-Robots-Tag'] = 'noindex, nofollow'
        
        return context
    
class CustomLoginView(LoginView):
    from .forms import LoginForm 
    form_class = LoginForm
    success_url = reverse_lazy('accounts:user_dashboard')  # Replace with your success URL name

    def form_valid(self, form):
        # Handle the "Remember Me" option
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # Set session expiry to 0 seconds to close the session after the browser is closed
            self.request.session.set_expiry(0)
            # Set session as modified to force data updates/cookie to be saved
            self.request.session.modified = True

        # Set the term_accepted session variable
        self.request.session['term_accepted'] = True

        # Call the parent class's form_valid method
        return super(CustomLoginView, self).form_valid(form)

    def form_invalid(self, form):
        # Handle the case when the form is invalid
        # You can add custom logic here if needed    
        messages.error(self.request, 'Invalid form submission.')   
        return super(CustomLoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add your additional context data here, such as 'site_data'
        site = site_data()
        site['title'] = 'Unlock Your World of Possibilities - Log In Now!'
        site['description'] = 'Welcome to our login page - where your online journey begins. Log in to access a world of personalized features and exclusive benefits. Securely manage your account and explore a seamless online experience. Join us today!'
        context['site_data'] = site
      

        # Set the X-Robots-Tag header in the HttpResponse object
        self.response = self.render_to_response(context)
        self.response['X-Robots-Tag'] = 'index, follow'

        return context

    


from django.contrib.messages.views import SuccessMessageMixin  
class SignupView(SuccessMessageMixin, CreateView):
    model = User  # Use your custom User model
    form_class = UserCreationFormFront  # Use Django's built-in UserCreationForm or your custom form
    template_name = 'registration/signup.html'  # Create a template for the signup form
    success_url = reverse_lazy('accounts:login')  # Redirect to the login page upon successful registration
    success_message = 'Please confirm your email to complete registration.'

    def form_valid(self, form):
        # Save the user object and log the user in upon successful registration
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Account activation required!'
        message = render_to_string('emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        user.email_user(subject, message)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle the case when the form is invalid
        # You can add custom logic here and customize the error messages
        messages.error(self.request, 'Invalid form submission.')
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        # Handle the case when a logged-in user tries to access the signup page
        if self.request.user.is_authenticated:
            messages.info(request, 'Already loggedin!')
            return HttpResponseRedirect(reverse_lazy('home:home'))  # Redirect to the dashboard page
        return super().get(request, *args, **kwargs)

    
    
    def get_context_data(self,  **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        

        site = site_data()   
        site['title'] = 'Unlock Your World of Possibilities - Signup Now!'
        site['description'] = 'Welcome to our signup page - where your online journey begins. Sign up to access a world of personalized features and exclusive benefits. Securely manage your account and explore a seamless online experience. Join us today!'

        context['site_data'] = site
        # Create an HttpResponse object with your template
        response = self.render_to_response(context)

        # Set the X-Robots-Tag header in the HttpResponse object
        response['X-Robots-Tag'] = 'index, follow'
        return context
    
   


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, ('Your account have been confirmed.'))
        return HttpResponseRedirect(reverse_lazy('accounts:login'))
    else:
        messages.warning(request, ('Activation link is invalid!'))
        return HttpResponseRedirect(reverse_lazy('core:home'))
    
    
def add_address(request, id):
    template = 'registration/add_address.html'
    
    user = get_object_or_404(User, id=id)
    address_form = AddressForm()
    
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():            
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            address_form = AddressSelectionForm(user)
            
            context = {        
                'address_form' : address_form        
            }
            return render(request, template, context=context)
        else:
            
            context = {        
                'address_form' : address_form        
            }
            return render(request, template, context=context)
        
    context = {        
        'address_form' : address_form        
    }
    return render(request, template, context=context)

@login_required
def dashboard(request):
    template = "registration/dashboard.html"
    
    books = Book.objects.filter(is_active = True).order_by('-updated_at')    
    quantity_form = QuantityForm(request=request, book=None)
    
    site = site_data()
    site['title'] = 'Dashboard'
    
    site['description'] = 'Access your personalized dashboard for real-time insights, data visualization, and account management. Stay informed and in control with our user-friendly dashboard.'

    context = {      

        'site_data' : site,   
        'books' : books,
        'quantity_form' : quantity_form   
        
    }  
    
    response = render(request, template, context=context)
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response 
    

    
    

def home(request):
    template = "registration/home.html"
    # users = User.objects.all().order_by('-date_joined')
    books = Book.objects.filter(is_active = True).order_by('-updated_at')    
    quantity_form = QuantityForm(request=request, book=None)
    
    site = site_data()
    site['title'] = 'All Registered Disciple'
    
    site['description'] = 'Browse our registered user list and discover a vibrant community. Find and connect with fellow members, explore profiles, and expand your network.'
  
    context = {     

        'site_data' : site,   
        'books' : books,
        'quantity_form' : quantity_form   
        
    }  
    response = render(request, template, context=context)
    response['X-Robots-Tag'] = 'index, follow'
    return response 
    

    






    
    
    
    
    
    
    

