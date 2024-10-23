# lourdessushi/Appmenu/templatetags/mis_filtros.py
from django import template

register = template.Library()

@register.filter
def calcular_total(item):
    return item.producto.precio * item.cantidad

