# lourdessushi/Appmenu/templatetags/custom_filters.py
from django import template
from babel.numbers import format_currency

register = template.Library()

@register.filter
def punto_miles(value):
    return format_currency(value, 'CLP', locale='es_CL')
