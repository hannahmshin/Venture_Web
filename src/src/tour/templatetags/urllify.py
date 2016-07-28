#urllify
from urllib import quote_plus
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def urlify(value):
    return quote_plus(value)

@register.filter
@stringfilter
def get_delete_url(value): #value will be obj.get_absolute_url
    return "/tourist/tours/" + value + "/delete"

@register.filter
@stringfilter
def get_edit_url(value):
    return "/tourist/tours/" + value + "/edit"


