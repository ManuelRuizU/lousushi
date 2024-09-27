# Appmenu/sevices.py
import urllib.parse
from .models import SubCategoria, Producto

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
    numero_telefono = "+56997075934"  # Número de WhatsApp del emprendimiento
    enlace_whatsapp = f"https://wa.me/{numero_telefono}?text={url_encoded_mensaje}"
    return enlace_whatsapp



def obtener_productos_por_subcategoria():
    subcategorias = SubCategoria.objects.prefetch_related('productos').all()
    subcat_productos = {}
    
    for subcategoria in subcategorias:
        productos = subcategoria.productos.all()
        subcat_productos[subcategoria] = productos

    return subcat_productos
