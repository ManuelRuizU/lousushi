from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

# Constantes
METODOS_PAGO = [
    ('EFECTIVO', 'Efectivo'),
    ('TRANSFERENCIA', 'Transferencia bancaria'),
    ('TARJETA_CREDITO', 'Tarjeta de crédito'),
    ('TARJETA_DEBITO', 'Tarjeta de débito'),
    ('PAGO_EN_LINEA', 'Pago en línea'),
]


class Emprendedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=10, blank=True)
    direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil', blank=True, null=True)

    def __str__(self):
        return f"{self.user.id} {self.user}"

class Emprendimiento(models.Model):
    # Mantengo UUIDField para Emprendimiento porque puede estar expuesto públicamente
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.emprendedor}"
    
    
class Sector(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    radio_maximo = models.FloatField()
    costo_base = models.DecimalField(max_digits=10, decimal_places=2)
    coeficiente_distancia = models.DecimalField(max_digits=10, decimal_places=2)
    dificultad = models.IntegerField(choices=[(1, 'Muy fácil'), (2, 'Fácil'), (3, 'Medio'), (4, 'Difícil'), (5, 'Muy difícil')], default=3)
    
    def calcular_costo_envio(self, distancia):
        # Calcula el costo de envío basado en la distancia y otros factores
        costo_base = self.costo_base
        coeficiente = self.coeficiente_distancia
        costo_adicional = distancia * coeficiente
        return costo_base + costo_adicional

class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()  # Convertir a mayúsculas
        super(Pais, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Region(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='regiones')
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='comunas')
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Comuna, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Calle(models.Model):
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='calles')
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Calle, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.numero}"

class Direccion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='direcciones_region')
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='direcciones_comuna')
    calle = models.ForeignKey(Calle, on_delete=models.CASCADE, related_name='direcciones_calle')
    departamento = models.CharField(max_length=10, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='direcciones')

    def __str__(self):
        if self.departamento:
            return f"{self.calle.nombre} {self.calle.numero}, Depto {self.departamento}, {self.comuna.nombre}, {self.region.nombre}"
        else:
            return f"{self.calle.nombre} {self.calle.numero}, {self.comuna.nombre}, {self.region.nombre}"

class Categoria(models.Model):
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE, related_name='categorias')
    categoria_nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='img', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.categoria_nombre:
            self.categoria_nombre = self.categoria_nombre.upper()
        super(Categoria, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.categoria_nombre

class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE, related_name='subcategorias')
    subcategoria_nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.subcategoria_nombre:
            self.subcategoria_nombre = self.subcategoria_nombre.upper()
        super(SubCategoria, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.subcategoria_nombre} ({self.categoria.categoria_nombre})"

class Producto(models.Model):
    # Mantengo UUIDField en Producto para seguridad y exposición pública
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, related_name='productos')
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='img', blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    precio = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Producto, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.precio} (Categoria: {self.categoria}, Subcategoria: {self.subcategoria})"



class Carrito(models.Model):
    # Mantengo UUIDField en Carrito para seguridad y protección de privacidad
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE, related_name='carritos')
    nombre_comprador = models.CharField(max_length=100)
    apellido_comprador = models.CharField(max_length=100)
    direccion_despacho = models.ForeignKey(Direccion, null=True, on_delete=models.CASCADE)
    telefono_contacto = models.CharField(max_length=20) 
    nota = models.TextField(blank=True, default='')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_envio = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)
    completo = models.BooleanField(default=False)
    cupon = models.ForeignKey('CuponDescuento', on_delete=models.SET_NULL, null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, default='EFECTIVO')

    def __str__(self):
        return f"Pedido de {self.id} {self.nombre_comprador} {self.apellido_comprador}"

    def get_total(self):
        total_items = sum(item.get_total_item() for item in self.items.all())
        total = total_items - self.descuento + self.valor_envio
        if self.cupon and self.cupon.es_valido():
            total = self.cupon.aplicar_descuento(total, self.valor_envio)
        return total


class CarritoItem(models.Model):
    # No se necesita UUID para CarritoItem, ya que es un modelo de relación interna
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} - Cantidad: {self.cantidad}"

    def get_total_item(self):
        return self.cantidad * self.producto.precio


# Modelo Cupon de Descuento

class CuponDescuento(models.Model):
    cupon_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valor_fijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    despacho_gratis = models.BooleanField(default=False)
    valor_minimo_compra = models.IntegerField(default=0)
    fecha_inicio = models.DateTimeField()
    fecha_expiracion = models.DateTimeField()
    usado = models.BooleanField(default=False)

    def __str__(self):
        return f"Cupon: {self.nombre} - Código: {self.codigo}"

    def es_valido(self):
        now = timezone.now()
        return self.fecha_inicio <= now <= self.fecha_expiracion and not self.usado

    def aplicar_descuento(self, total, valor_envio):
        if not self.es_valido():
            return total
        if self.despacho_gratis:
            return total - valor_envio
        if self.porcentaje:
           return total * (1 - self.porcentaje / 100)
        if self.valor_fijo:
            return total - self.valor_fijo
        return total

