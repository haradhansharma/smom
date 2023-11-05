from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django_cron import CronJobBase, Schedule
from book.models import BookOrder, OrderInvoice
from core.helper import build_full_url, custom_send_mail, custom_send_mass_mail
# from shop.models import Order, Quotation
# from shcurrency.models import Currency
import requests
import json
from django.db import models
from django.template.loader import render_to_string
from django.db.models import F
from django.utils.safestring import mark_safe
from django.core.mail import send_mass_mail
import logging
log =  logging.getLogger('log')
      
def delete_due_orders():
    try:
        # Get a list of order IDs to delete
        order_ids_to_delete = [
            invoice.order.id
            for invoice in OrderInvoice.objects.filter(validity__gt=timezone.now() + timezone.timedelta(days=3))
            if not invoice.order.has_transactions
        ]

        # Bulk delete orders using their primary keys
        total_deleted = BookOrder.objects.filter(id__in=order_ids_to_delete).delete()

        return total_deleted[0]  # Return the number of orders deleted
    except Exception as e:
        log.warning(f'Bulk delete failed due to error: {e}')
        return 0
    
def send_payment_reminder():
    
    
    today = timezone.now()
    three_days_from_now = today + timezone.timedelta(days=3)
    
    invoices = OrderInvoice.objects.filter(validity__gte=today, validity__lte=three_days_from_now)[:150]
    print(invoices)
    # Prepare email messages and recipients
    

    from_email = settings.DEFAULT_FROM_EMAIL

    email_data = []
    for invoice in invoices:
        
        recipient = invoice.order.customer.email
        
        subject = "Friendly Payment Reminder for Invoice #[Your Invoice Number]"
        message = f"""
        Dear {invoice.order.delivery_address.name},

        I hope this email finds you well. We sincerely appreciate your business and would like to remind you about an upcoming payment that is due in just three days.

        Order Number: {invoice.order.id}
        Invoice Amount: {invoice.order.amount}    
        Due Date: {invoice.validity}

        Please take a moment to review your records and ensure that the payment is scheduled for on or before the due date to avoid order cancellation.

        You have a simple option for making the payment:
        
        Just go to the link : {invoice.update_payment_url}?search={invoice.order.id}

        There you will find a button named "UPDATE PAYMENT" where you need to provide payment information. Make sure you paid the amount as per instruction of invoice.
        
        To findout the invoice just click on the "VIEW INVOICE" button on that page.

        If you have any questions or need assistance with your payment, please don't hesitate to contact our customer support team at sales@sankarmath,org. We're here to help you!

        Thank you for your prompt attention to this matter. We value your business and look forward to continuing to serve you.

        Warm regards,

        Sankarmath - o - mission
        """        
        
        email_data.append((subject, message, from_email, [recipient]))

    # Send bulk email
    send_mass_mail(email_data, fail_silently=False)
    
    return len(email_data)
            
    
            
            
        

        
        
class RunSmonCronJobs(CronJobBase):    
     
    RUN_EVERY_MINS = 720  #per 12 hrs
    RETRY_AFTER_FAILURE_MINS = 1
    MIN_NUM_FAILURES = 2    
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'core.main_cron_job_12_hrs'   
    
    def do(self):          
        try: 
            due_order_deleted = delete_due_orders()
            log.info(f"Info: {due_order_deleted} - Due Order deleted by cronJOB.")
            
            total_reminder_main = send_payment_reminder()
            log.info(f"Info: {total_reminder_main} - Reminder mail sent by cronJOB.")

        except Exception as e:            
            log.exception(f'An error occurred while running cronjob: {e}')
            
        
        
        
        
 