from django import template

from book.forms import QuantityForm

register = template.Library()

@register.filter
def get_edited_form(request, book):
    edited_form = QuantityForm(request=request, book=book)
    return edited_form