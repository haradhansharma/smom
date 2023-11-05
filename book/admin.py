from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from book.models import Book, BookOrder, BookOrderItem, OrderTransaction
from payment_method.utils import get_payment_method_class
from payment_method.views import create_pdf_invoice
from django.utils import timezone

class BookAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('description',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'is_active',)
admin.site.register(Book, BookAdmin)


class BookOrderItemInline(admin.TabularInline):
    model = BookOrderItem 
    readonly_fields = ('item','sale_price', 'quantity', 'total_amount',)

class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('id','amount', 'customer', 'order_status', 'created_at')
    search_fields = ('id', 'customer__email')
    readonly_fields = ('amount', 'customer', 'order_status','delivery_address',)
    inlines = [BookOrderItemInline]    
admin.site.register(BookOrder, BookOrderAdmin)



class OrderTransactionAdmin(admin.ModelAdmin):
    '''
    ########## it is for manual payment checking only. so this process should be implemented separately if automatic payment gateway implementing later############
    '''
    list_display = ('order','amount','gateway','trxID','mobile','check_and_confirmed', 'created_at')  # Add any other fields you want to display

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        gateway = get_payment_method_class(obj.order.invoice.gateway) 
        
        if obj.check_and_confirmed:            
            
            obj.order.invoice.paid = True
            obj.order.invoice.paid_on = timezone.now()
            obj.order.invoice.save()
            
            if obj.order.pending_amount <= 0:
                obj.order.order_status = 'confirm'
                obj.order.save()
            else:
                obj.order.order_status = 'payment_pending'
                obj.order.save()
                
             
            create_pdf_invoice(request, obj.order, gateway())
            
        if obj.check_and_reject:
            
            obj.order.order_status = 'payment_reject'
            obj.order.save()
             
            create_pdf_invoice(request, obj.order, gateway())

admin.site.register(OrderTransaction, OrderTransactionAdmin)

