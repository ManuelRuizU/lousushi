# lourdessushi/Appmenu/templatetags/navbar_tags.py


from django import template
from ..models import Categoria  # Asegúrate de que esta línea esté correcta

register = template.Library()

@register.simple_tag
def mostrar_navbar():
    categories = Categoria.objects.all()
    return categories
