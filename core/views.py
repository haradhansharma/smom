from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from core.context_processor import site_data
from django.utils.html import strip_tags
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from core.agent_helper import get_client_ip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.views.generic.edit import CreateView
from django.db.models import Count, Q
from core.helper import (
    custom_send_mail, 
    custom_send_mass_mail, 
    # get_blogs, 
    # get_services,
    # get_category_with_count,
    # get_top_views,
    # get_blog_archive
    )
from .models import *
from .forms import *
import calendar
from django.views.decorators.cache import cache_control

import logging
log =  logging.getLogger('log')


# Create your views here.

# def home(request):
#     template_name = 'core/home.html'    
        
#     site = site_data()
#     site['title'] = site.get('slogan')      
    
#     # stripe.api_key = settings.STRIPE_SECRET_KEY
#     # products = stripe.Product.list()
#     # print(products)
    
   
#     latest_news = get_blogs()[:3]
    
#     about_us_link = Page.objects.get(slug = 'about-us').get_absolute_url
    
#     services = get_services()
    
#     context = {    
#         'site_data' : site,
#         'latest_news' : latest_news,
#         'about_us_link': about_us_link,
#         'services' : services
#     }
#     return render(request, template_name, context=context)


# def contact(request):
    
#     template_name = 'core/contact.html' 
#     form = ContactUsForm()
        
#     if request.method == 'POST':
#         form = ContactUsForm(request.POST)
#         if form.is_valid():
#             form.save()            
#             messages.success(request, 'Your message has been sent. We will get back to you soon.')
        
#             email_messages = []
            
#             from_email = settings.DEFAULT_FROM_EMAIL               
            
#             # Send email to the site admin
#             admin_subject = f'SINCEHENCE LTD - New contact form submission'
#             admin_message = f"Name: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\n\nMessage: {form.cleaned_data['message']}"        
#             admin_reply_to = [form.cleaned_data['email']]        
#             admin_mail = [site_data().get('email')]
            
            
#             email_messages.append((admin_subject, admin_message, from_email, admin_mail , '',  admin_reply_to, ''))
            
#             visitor_subjct = f"SINCEHENCE LTD - Greetings from {form.cleaned_data['name']}!" 
#             visitor_message = f"Dear {form.cleaned_data['name']},\n\nThank you for reaching out to us through our website." 
#             visitor_message += f"We appreciate your interest in {site_data().get('name')}!\n\n"
#             visitor_message += f"This email is to acknowledge that we have received your contact form submission. Please note that this is a no-reply email, "
#             visitor_message += f"so there's no need to reply to it.\n\nOur team is currently reviewing your message, and we will get back to you soon with a response. "
#             visitor_message += f"We strive to provide excellent service and address your inquiry promptly.\n\nOnce again, we thank you for getting in touch with us. "
#             visitor_message += f"We look forward to connecting with you!\n\nBest regards,\nThe {site_data().get('name')} Team"
#             visitor_mail = [form.cleaned_data['email']]
            
#             email_messages.append((visitor_subjct, visitor_message, from_email, visitor_mail, '', '', ''))        

#             custom_send_mass_mail(email_messages, fail_silently=False)
            
            
#         else:   
#             messages.error(request, 'There was an error with your submission. Please try again.')
            
    
       
        
#     site = site_data()
#     site['title'] = 'Our Contact Address Here.'
#     site['description'] = f'Contact {site.get("name")} for any inquiries, feedback, or collaboration opportunities. Our dedicated team is here to assist you. Reach out to us through the provided contact details or fill out the contact form on our page. We look forward to hearing from you and providing the support you need.'
    
    
#     context = {
#         'form' : form,
#         'site_data' : site
#     }
#     return render(request, template_name, context=context)

# def get_3_parameter():
#     categories = get_category_with_count()   
    
#     top_views = get_top_views()    
    
#     blog_archive =  get_blog_archive()
    
#     return categories, top_views, blog_archive
    
    
# def archive_detail(request, year, month):
#     template_name = 'core/category_details.html'  
    
#     search_form = BlogSearchForm()
#     if 'search_query' in request.GET:
#         search_form = BlogSearchForm(request.GET)        
#         if search_form.is_valid():
#             search_query = search_form.cleaned_data['search_query']    
#             blogs = Blog.published.filter(
#                 (Q(title__icontains=search_query) | Q(body__icontains=search_query)), updated_at__year=year, updated_at__month=month
#             )          
#     else:   
#         blogs = Blog.published.filter(updated_at__year=year, updated_at__month=month)
    
         

#     categories, top_views, blog_archive = get_3_parameter()

#     paginator = Paginator(blogs, 10) 

#     page_number = request.GET.get('page')
    
#     try:
#         blogs = paginator.page(page_number)
#     except PageNotAnInteger:
#         blogs = paginator.page(1)
#     except EmptyPage:
#         blogs = paginator.page(paginator.num_pages) 
        
        
#     site = site_data()
#     site['title'] = f'Latest blogs of {calendar.month_name[month]}, {year}'
#     site['description'] = f'Browse through a collection of insightful blog articles from {site.get("name")}. Explore our blog archive for valuable information, industry trends, and expert advice on wholesale trade, IT consultancy, data processing, and more. Stay informed and enhance your knowledge with our comprehensive blog content.'
    
     
#     context = {
#         'search_form': search_form,
#         'blogs': blogs,
#         'site_data' : site,
#         'categories' : categories,
#         'top_views' : top_views,
#         'blog_archive' : blog_archive,

#     }
    
#     return render(request, template_name, context=context)


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)   
# def category_detail(request, slug):
    
#     template_name = 'core/category_details.html'  

#     category = get_object_or_404(Category.objects.prefetch_related('blogs_category'), slug=slug)   
#     search_form = BlogSearchForm()
    
#     if 'search_query' in request.GET:
#         search_form = BlogSearchForm(request.GET)        
#         if search_form.is_valid():
#             search_query = search_form.cleaned_data['search_query']    
#             blogs = category.blogs_category.filter(
#                 (Q(title__icontains=search_query) | Q(body__icontains=search_query)),
#                 status = 'published'
#             )          
#     else:        
#         blogs = category.blogs_category.filter(status = 'published')       
 
    
#     categories, top_views, blog_archive = get_3_parameter()     
    

#     paginator = Paginator(blogs, 10) 

#     page_number = request.GET.get('page')
    
#     try:
#         blogs = paginator.page(page_number)
#     except PageNotAnInteger:
#         blogs = paginator.page(1)
#     except EmptyPage:
#         blogs = paginator.page(paginator.num_pages) 
        
        
#     site = site_data()
#     site['title'] = f'Latest Blogs of Category: {category.title}'
#     truncated_string = strip_tags(category.description)
#     site['description'] = truncated_string
    
     
#     context = {
#         'search_form': search_form,
#         'category' : category,
#         'blogs': blogs,
#         'site_data' : site,
#         'categories' : categories,
#         'top_views' : top_views,
#         'blog_archive' : blog_archive
#     }
    
#     return render(request, template_name, context=context)

# def user_blogs(request, username):
    
#     template_name = 'core/category_details.html'  
    
#     search_form = BlogSearchForm()
    
#     if 'search_query' in request.GET:
#         search_form = BlogSearchForm(request.GET)        
#         if search_form.is_valid():
#             search_query = search_form.cleaned_data['search_query']    
#             blogs = Blog.published.filter(
#                 (Q(title__icontains=search_query) | Q(body__icontains=search_query)), 
#                 creator__username = username
#             )          
#     else:
#         blogs = Blog.published.filter(creator__username = username) 
 
    
#     categories, top_views, blog_archive = get_3_parameter()     
    

#     paginator = Paginator(blogs, 10) 

#     page_number = request.GET.get('page')
    
#     try:
#         blogs = paginator.page(page_number)
#     except PageNotAnInteger:
#         blogs = paginator.page(1)
#     except EmptyPage:
#         blogs = paginator.page(paginator.num_pages) 
        
        
#     site = site_data()
#     site['title'] = f'Latest Blogs of Creator: {username}'    
#     site['description'] = f"Welcome to {username}'s blog, where you'll find a wealth of valuable insights and personal experiences. Explore a diverse range of topics, including {username}'s areas of expertise or interests, and gain unique perspectives on relevant industry or subject. Expand your knowledge and engage with thought-provoking content on {username}'s blog."
    
     
#     context = {
#         'search_form': search_form,
#         'blogs': blogs,
#         'site_data' : site,
#         'categories' : categories,
#         'top_views' : top_views,
#         'blog_archive' : blog_archive
#     }
    
#     return render(request, template_name, context=context)


# def latest_blogs(request):
    
#     template_name = 'core/category_details.html'
    
#     search_form = BlogSearchForm()
    
#     if 'search_query' in request.GET:
#         search_form = BlogSearchForm(request.GET)        
#         if search_form.is_valid():
#             search_query = search_form.cleaned_data['search_query']
#             blogs = Blog.published.filter(
#                 Q(title__icontains=search_query) | Q(body__icontains=search_query)
#             )             
#     else:
#         blogs = get_blogs()
    
#     categories, top_views, blog_archive = get_3_parameter()     
    

#     paginator = Paginator(blogs, 10) 

#     page_number = request.GET.get('page')
    
#     try:
#         blogs = paginator.page(page_number)
#     except PageNotAnInteger:
#         blogs = paginator.page(1)
#     except EmptyPage:
#         blogs = paginator.page(paginator.num_pages) 
        
        
#     site = site_data()
#     site['title'] = f'Latest Published Blogs' 
#     site['description'] = 'Stay informed with the latest insights and updates from SINCEHENCE LTD. Explore our blog to discover valuable information, industry trends, and expert advice on wholesale trade, IT consultancy, data processing, and more. Stay connected and enhance your knowledge with our informative blog posts.'
    
     
#     context = {
#         'search_form': search_form,
#         'blogs': blogs,
#         'site_data' : site,
#         'categories' : categories,
#         'top_views' : top_views,
#         'blog_archive' : blog_archive
#     }
    
#     return render(request, template_name, context=context)

# def page_detail(request, slug):
#     template_name = 'core/page_detail.html'
    
#     page = get_object_or_404(Page, slug=slug) 
    
#     page.view(request)     
    
#     site = site_data()
#     site['title'] = page.top_tagline
#     site['description'] = page.meta_description
#     site['og_image'] = page.top_banenr.url
    
    
    
    
#     context = {
#         'page' : page,
#         'site_data' : site
#     }
    
#     return render(request, template_name, context=context)   


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)   
# def blog_detail(request, slug):
#     template_name = 'core/blog_detail.html'
    
#     blog = get_object_or_404(Blog.published.prefetch_related('categories'), slug=slug)   
     
#     blog.view(request)    
 
        
#     site = site_data()
#     site['title'] = blog.title[:45]
#     truncated_string = strip_tags(blog.body)[:160]
#     site['description'] = truncated_string
#     site['og_image'] = blog.feature.url
    
    
#     context = {      
#         'blog' : blog,   
#         'site_data' : site,      
#     }   
    
#     return render(request, template_name, context=context)

    



    