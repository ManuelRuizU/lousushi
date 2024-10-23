# Appmenu/sevices.py
import urllib.parse
from .models import SubCategoria, Producto, Carrito, CarritoItem, CuponDescuento
from django.shortcuts import get_object_or_404
import uuid

def generar_enlace_whatsapp(carrito):
    if not carrito:
        raise ValueError("El carrito no puede ser nulo o vacío")
    mensaje = (
        f"Nuevo Pedido\n"
        f"Nombre: {carrito.nombre_comprador} {carrito.apellido_comprador}\n"
        f"Teléfono: {carrito.telefono_contacto}\n"
        f"Dirección: {carrito.direccion_despacho}\n"
        f"Items:\n"
    )
    for item in carrito.items.all():
        mensaje += f"- {item.producto.nombre} x {item.cantidad}\n"
    mensaje += (
        f"Descuento: ${carrito.descuento}\n"
        f"Envío: ${carrito.valor_envio}\n"
        f"Total: ${carrito.get_total()}\n"
    )
    url_encoded_mensaje = urllib.parse.quote(mensaje)
    numero_telefono = carrito.emprendimiento.emprendedor.telefono.replace(" ", "").replace("-", "") # Número de WhatsApp Dinamico
    enlace_whatsapp = f"https://wa.me/{numero_telefono}?text={url_encoded_mensaje}"
    return enlace_whatsapp

def agregar_producto_al_carrito_db(carrito, producto, cantidad=1):
    print("Agregar producto al carrito DB")
    """Agrega o actualiza un producto en el carrito"""
    item, creado = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero")
    item.save()
    return item

def obtener_carrito_no_autenticado(emprendimiento_id):
    # Busca un carrito existente para el emprendimiento
    carrito = Carrito.objects.filter(emprendimiento_id=emprendimiento_id, completo=False).first()
    if carrito:
        return carrito
    # Si no existe, crea uno nuevo
    carrito_id = str(uuid.uuid4())
    carrito = Carrito.objects.create(
        id=carrito_id,
        direccion_despacho=None,
        emprendimiento_id=emprendimiento_id
    )
    return carrito

def agregar_producto_al_carrito(request, producto_id, cantidad=1):
    """Agrega un producto al carrito (usuario autenticado o no)"""
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_carrito_no_autenticado(producto.emprendimiento.id)  # Revisión: pasar emprendimiento_id
    return agregar_producto_al_carrito_db(carrito, producto, cantidad)



def obtener_productos_por_subcategoria():
    subcategorias = SubCategoria.objects.prefetch_related('productos').all()
    subcat_productos = {}
    for subcategoria in subcategorias:
        productos = subcategoria.productos.all()
        subcat_productos[subcategoria] = productos
    return subcat_productos

def remover_producto_del_carrito(carrito, producto):
    """Elimina un producto específico del carrito"""
    try:
        item = CarritoItem.objects.get(carrito=carrito, producto=producto)
        item.delete()
        return True
    except CarritoItem.DoesNotExist:
        return False

def vaciar_carrito(carrito):
    """Vacía todos los productos del carrito después de finalizar el pedido"""
    carrito.items.all().delete()
    carrito.completo = True
    carrito.save()

def calcular_costo_total(carrito):
    """Calcula el costo total del carrito, considerando descuentos y envío"""
    total_items = sum(item.get_total_item() for item in carrito.items.all())
    total = total_items - carrito.descuento + carrito.valor_envio
    if carrito.cupon and carrito.cupon.es_valido():
        total = carrito.cupon.aplicar_descuento(total, carrito.valor_envio)
    return total

def generar_resumen_pedido(carrito):
    """Genera un resumen legible del pedido en formato de texto"""
    resumen = (
        f"Pedido de {carrito.nombre_comprador} {carrito.apellido_comprador}\n"
        f"Teléfono: {carrito.telefono_contacto}\n"
        f"Dirección de despacho: {carrito.direccion_despacho}\n"
        f"Items:\n"
    )
    for item in carrito.items.all():
        resumen += f"- {item.producto.nombre} x {item.cantidad} = ${item.get_total_item()}\n"
    resumen += (
        f"Descuento: ${carrito.descuento}\n"
        f"Envío: ${carrito.valor_envio}\n"
        f"Total: ${carrito.get_total()}\n"
    )
    return resumen

def verificar_carrito_completo(carrito):
    """Verifica que el carrito tenga productos y dirección válida"""
    if not carrito.items.exists():
        raise ValueError("El carrito está vacío")
    if not carrito.direccion_despacho:
        raise ValueError("La dirección de despacho no es válida")
    if not carrito.telefono_contacto:
        raise ValueError("El teléfono de contacto no es válido")
    return True
