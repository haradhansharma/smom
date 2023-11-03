from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from book.forms import PaymentForm
from book.models import BookOrder

# Create your views here.
def bkash_manual(request, order_id):
    from payment_method.gateways.bkash import bKashPaymentGateway
    gateway = bKashPaymentGateway()
    gatway_instruction = gateway.get_gateway_instruction()
    template = 'payment_method/bkash_manual.html'
    order = get_object_or_404(BookOrder, id = order_id)
    payment_form = PaymentForm()
    if request.method == 'POST':  
        payment_form = PaymentForm(request.POST, request.FILES)
        if payment_form.is_valid():
            transaction = payment_form.save(commit=False)            
            transaction.order = order
            transaction.gateway = gateway.get_gateway_name()            
            transaction.save()
            
            order.order_status = 'processing'
            order.save()
            
            return HttpResponse('Order Placed Success Fully!')
        else:
            context = {
                'order' : order,       
                'payment_form' : payment_form,
                'gatway_instruction' : gatway_instruction
                
            }
            return render(request, template, context)
        
    context = {
        'order' : order, 
        'payment_form' : payment_form,
        'gatway_instruction' : gatway_instruction
        
    }

    
    return render(request, template, context)


# Create your views here.
def rocket_manual(request, order_id):
    from payment_method.gateways.rocket import RocketPaymentGateway
    gateway = RocketPaymentGateway()
    gatway_instruction = gateway.get_gateway_instruction()
    template = 'payment_method/rocket_manual.html'
    order = get_object_or_404(BookOrder, id = order_id)
    payment_form = PaymentForm()
    if request.method == 'POST':  
        payment_form = PaymentForm(request.POST, request.FILES)
        if payment_form.is_valid():
            transaction = payment_form.save(commit=False)            
            transaction.order = order
            transaction.gateway = gateway.get_gateway_name()            
            transaction.save()
            
            order.order_status = 'processing'
            order.save()
            
            return HttpResponse('Order Placed Success Fully! Payment rocket')
        else:
            context = {
                'order' : order,       
                'payment_form' : payment_form,
                'gatway_instruction' : gatway_instruction
                
            }
            return render(request, template, context)
        
    context = {
        'order' : order, 
        'payment_form' : payment_form,
        'gatway_instruction' : gatway_instruction
        
    }

    
    return render(request, template, context)



def exim_bd(request, order_id):
    from payment_method.gateways.eximbd import EximBdPaymentGateway
    gateway = EximBdPaymentGateway()
    gatway_instruction = gateway.get_gateway_instruction()
    template = 'payment_method/eximbd.html'
    order = get_object_or_404(BookOrder, id = order_id)
    payment_form = PaymentForm()
    if request.method == 'POST':  
        payment_form = PaymentForm(request.POST, request.FILES)
        if payment_form.is_valid():
            transaction = payment_form.save(commit=False)            
            transaction.order = order
            transaction.gateway = gateway.get_gateway_name()            
            transaction.save()
            
            order.order_status = 'processing'
            order.save()
            
            return HttpResponse('Order Placed Success Fully! Payment Exim Bank BD')
        else:
            context = {
                'order' : order,       
                'payment_form' : payment_form,
                'gatway_instruction' : gatway_instruction
                
            }
            return render(request, template, context)
        
    context = {
        'order' : order, 
        'payment_form' : payment_form,
        'gatway_instruction' : gatway_instruction
        
    }

    
    return render(request, template, context)