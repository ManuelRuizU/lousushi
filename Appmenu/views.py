# Appmenu/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Producto, Carrito, CarritoItem
from .services import obtener_productos_por_subcategoria
from django.views.decorators.http import require_POST

def index(request):
    producto_abierto_id = request.GET.get('producto_abierto_id', None)
    context = {
        'subcat_productos': obtener_productos_por_subcategoria(),
        'producto_abierto_id': producto_abierto_id,
    }
    return render(request, 'index.html', context)

def home(request):
    subcat_productos = obtener_productos_por_subcategoria()
    context = {
        'subcat_productos': subcat_productos
    }
    return render(request, 'home.html', context)

def login_view(request):
    return render(request, "registration/login.html", {})

def get_or_create_carrito(request):
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        return get_object_or_404(Carrito, id=carrito_id)
    else:
        carrito = Carrito.objects.create()
        request.session['carrito_id'] = str(carrito.id)
        return carrito

def carrito_view(request):
    carrito = get_or_create_carrito(request)
    return render(request, 'carrito.html', {'carrito': carrito})

@require_POST
def agregar_al_carrito(request):
    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))

    # Obtener el carrito actual o crear uno nuevo
    carrito = get_or_create_carrito(request)

    # Buscar el producto
    producto = get_object_or_404(Producto, id=producto_id)

    # Buscar si el producto ya está en el carrito
    carrito_item, creado = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado:
        # Si ya existe, solo actualizamos la cantidad
        carrito_item.cantidad += cantidad
    else:
        carrito_item.cantidad = cantidad

    carrito_item.save()

    # Retornar una respuesta en JSON para actualizar el frontend
    return JsonResponse({
        'mensaje': 'Producto agregado al carrito',
        'total_items': carrito.items.count()
    })

# Appmenu/views.py

from django.http import JsonResponse

def obtener_carrito(request):
    carrito = get_or_create_carrito(request)
    items = []
    total = 0

    for item in carrito.items.all():
        items.append({
            'producto': {
                'nombre': item.producto.nombre,
                'precio': item.producto.precio,
            },
            'cantidad': item.cantidad,
        })
        total += item.producto.precio * item.cantidad

    return JsonResponse({'items': items, 'total': total, 'valor_envio': carrito.valor_envio})

