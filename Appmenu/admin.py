# admin.py
from django.contrib import admin
from .models import Emprendedor, Emprendimiento, Pais, Region, Comuna, Calle, Direccion,  Categoria, SubCategoria, Producto
from .models import Carrito, CarritoItem, Sector
from .models import CuponDescuento

class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'telefono', 'direccion', 'fecha_creacion')
    search_fields = ('user__username', 'rut', 'telefono')


class EmprendimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'emprendedor', 'logo')
    search_fields = ('nombre', 'emprendedor__user__username')


class PaisAdmin(admin.ModelAdmin):   
    list_display = ('nombre',)
    search_fields = ('nombre',)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'numero')
    search_fields = ('nombre', 'pais__nombre')

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region')
    search_fields = ('nombre', 'region__nombre')

class CalleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero', 'comuna')
    search_fields = ('nombre', 'comuna__nombre')

class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'comuna', 'region', 'departamento')
    search_fields = ('calle__nombre', 'comuna__nombre', 'region__nombre', 'departamento')
    
class SectorAdmin(admin.ModelAdmin):   
    list_display = ('nombre',)
    search_fields = ('nombre',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria_nombre',)
    search_fields = ('categoria_nombre',)

class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ('subcategoria_nombre', 'categoria')
    search_fields = ('subcategoria_nombre', 'categoria__categoria_nombre')

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'categoria', 'subcategoria')
    search_fields = ('id', 'nombre', 'categoria__categoria_nombre', 'subcategoria__subcategoria_nombre')
    
class CarritoItemInline(admin.TabularInline):
    model = CarritoItem
    extra = 0

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_comprador', 
        'apellido_comprador', 
        'fecha_creacion', 
        'completo', 
        'metodo_pago',  
        'get_total',
        'get_productos_resumen'  # Mostrar resumen de productos
    )
    inlines = [CarritoItemInline]

    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total'

    # Mostrar un resumen de los productos en la lista de carritos
    def get_productos_resumen(self, obj):
        productos = obj.items.all()
        return ", ".join([f"{item.producto.nombre} ({item.cantidad})" for item in productos])
    get_productos_resumen.short_description = 'Productos'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('get_total',)
        return self.readonly_fields


@admin.register(CuponDescuento)
class CuponDescuentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'porcentaje', 'valor_fijo', 'despacho_gratis', 'fecha_inicio', 'fecha_expiracion')
    search_fields = ('codigo',)
    list_filter = ('fecha_inicio', 'fecha_expiracion', 'despacho_gratis')

# Registra el modelo en el sitio de administración





admin.site.register(Emprendedor, EmprendedorAdmin)
admin.site.register(Emprendimiento, EmprendimientoAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Calle, CalleAdmin)
admin.site.register(Direccion, DireccionAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
