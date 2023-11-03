from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class ExtendSiteOfSite(admin.StackedInline):
    model = ExSite
    can_delete = False   

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    inlines = [ExtendSiteOfSite]    
admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)


# admin.site.register(OurService)


# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ('name', 'phone_number', 'email', 'created_at' )  
#     search_fields = ('name', 'phone_number', 'email', 'message' )    
#     ordering = ('-created_at',)
    
    
# class PageAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
#     summernote_fields = ('body',)
#     prepopulated_fields = {'slug': ('title',)}
    
#     def save_model(self, request, obj, form, change):
#         # set the flag indicating saving from admin
#         obj.creator = request.user
#         obj._saving_from_admin = True        
#         super().save_model(request, obj, form, change)
#         obj._saving_from_admin = False   

# admin.site.register(Page, PageAdmin)
    
    
# class BlogAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
#     summernote_fields = ('body',)
#     prepopulated_fields = {'slug': ('title',)}
#     list_display = ('title', 'status',)
    
#     def save_model(self, request, obj, form, change):       
#         # set the flag indicating saving from admin
#         obj.creator = request.user
        
#         obj._saving_from_admin = True        
#         super().save_model(request, obj, form, change)
#         obj._saving_from_admin = False      
    
    
#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)

       
    

# admin.site.register(Blog, BlogAdmin)




# class CategoryAdmin(admin.ModelAdmin):     
    
#     prepopulated_fields = {'slug': ('title',)}
#     list_filter = ['title', 'parent__title']
#     search_fields = ['title' ]
#     list_display = ('title', 'id',)
    
#     def save_model(self, request, obj, form, change):       
#         # set the flag indicating saving from admin
#         obj.creator = request.user        
#         obj._saving_from_admin = True        
#         super().save_model(request, obj, form, change)
#         obj._saving_from_admin = False      
        
#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
        
# admin.site.register(Category, CategoryAdmin)
