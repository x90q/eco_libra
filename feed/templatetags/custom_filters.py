from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def simple_timesince(value):
    if not value:
        return ""
    return timesince(value).split(',')[0]