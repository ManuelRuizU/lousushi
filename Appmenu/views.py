# lourdessushi/Appmenu/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Emprendedor, Emprendimiento, Producto, Carrito, CarritoItem, CuponDescuento, Categoria, SubCategoria
from .services import obtener_productos_por_subcategoria, agregar_producto_al_carrito_db, obtener_carrito_no_autenticado
from django.views.decorators.http import require_http_methods
import uuid

def home(request):
    emprendimiento = Emprendimiento.objects.first()
    if emprendimiento:
        nombre_emprendimiento = emprendimiento.nombre
        id_emprendimiento = emprendimiento.id
        logo_emprendimiento = emprendimiento.logo.url if emprendimiento.logo else None
    else:
        nombre_emprendimiento = "Nombre por defecto"
        id_emprendimiento = "id por defecto"
        logo_emprendimiento = None
    subcat_productos = obtener_productos_por_subcategoria()
    carrito_items = CarritoItem.objects.all()
    totales = [item.producto.precio * item.cantidad for item in carrito_items]
    total_general = sum(totales)
    categories = Categoria.objects.all()
    context = {
        'nombre_emprendimiento': nombre_emprendimiento,
        'id_emprendimiento': id_emprendimiento,
        'logo_emprendimiento': logo_emprendimiento,
        'subcat_productos': subcat_productos,
        'carrito_items': carrito_items,
        'totales': totales,
        'total_general': total_general,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Categoria, id=category_id)
    context = {
        'category': category,
    }
    return render(request, 'category_detail.html', context)

def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(SubCategoria, id=subcategory_id)
    return render(request, 'subcategory_detail.html', {'subcategory': subcategory})

def login_view(request):
    return render(request, "registration/login.html", {})

def obtener_emprendimiento_id(request):
    emprendimiento = Emprendimiento.objects.first()
    emprendimiento_id = emprendimiento.id if emprendimiento else None
    return JsonResponse({'emprendimiento_id': emprendimiento_id})

@require_http_methods(['POST'])
@csrf_exempt
def crear_carrito(request, emprendimiento_id):
    if request.method == 'POST':
        nuevo_carrito = Carrito.objects.create(emprendimiento_id=emprendimiento_id)
        return JsonResponse({'id': nuevo_carrito.id})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_productos(request):
    productos = Producto.objects.all().values('id', 'nombre', 'precio')
    return JsonResponse(list(productos), safe=False)

def agregar_al_carrito(request):
    print(request.body)
    try:
        data = json.loads(request.body)
        producto_id = data.get('productoId')
        cantidad = data.get('cantidad')

        if not isinstance(cantidad, int) or cantidad <= 0:
            return JsonResponse({'error': 'Cantidad inválida'}, status=400)

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)

        emprendimiento_id = producto.emprendimiento.id

        carrito = Carrito.objects.get_or_create(emprendimiento_id=emprendimiento_id)
        carrito_item, creado = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
        carrito_item.cantidad = cantidad
        carrito_item.save()

        return JsonResponse({'mensaje': 'Producto agregado al carrito.', 'carrito_id': carrito.id}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obtener_carrito(request):
    carrito = obtener_carrito_no_autenticado(request)
    items = [
        {
            'nombre': item.producto.nombre,
            'cantidad': item.cantidad,
            'total': item.get_total_item()
        }
        for item in carrito.items.all()
    ]
    return JsonResponse({'items': items})

def carrito_view(request):
    carrito = obtener_carrito_no_autenticado(request)
    carrito_items = carrito.items.all()
    context = {
        'carrito': carrito,
        'carrito_items': carrito_items,
    }
    return render(request, 'carrito_siderbar.html', context)


