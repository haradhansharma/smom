from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from book.models import Book, BookOrder, BookOrderItem, OrderTransaction


class BookAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('description',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'is_active',)
admin.site.register(Book, BookAdmin)


class BookOrderItemInline(admin.TabularInline):
    model = BookOrderItem 

class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('amount', 'customer', 'order_status', 'created_at')
    search_fields = ('id', 'customer__email')
    inlines = [BookOrderItemInline]    
admin.site.register(BookOrder, BookOrderAdmin)

admin.site.register(OrderTransaction)

