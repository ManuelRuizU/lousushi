# lourdessushi/lourdessushi/urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from Appmenu.views import home, login_view, agregar_al_carrito, obtener_carrito, carrito_view, category_detail, subcategory_detail, obtener_emprendimiento_id, crear_carrito, obtener_productos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include([
        path('', home, name='home'),
        path('emprendimiento/<uuid:emprendimiento_id>/', home, name='home_emprendimiento'),
        path('category/<int:category_id>/', category_detail, name='category_detail'),
        path('subcategory/<int:subcategory_id>/', subcategory_detail, name='subcategory_detail'),
        path('login/', login_view, name='login'),
        path('api/emprendimiento/<uuid:emprendimiento_id>/agregar-al-carrito/', agregar_al_carrito, name='agregar-al-carrito'),
        path('api/emprendimiento/obtener-id/', obtener_emprendimiento_id, name='obtener_emprendimiento_id'),
        path('api/obtener-carrito/', obtener_carrito, name='obtener_carrito'),
        path('api/obtener-productos/', obtener_productos, name='obtener_productos'),
        path('carrito/', carrito_view, name='carrito_view'),
        path('crear-carrito/<uuid:emprendimiento_id>/', crear_carrito, name='crear_carrito'),
    ])),
]

# Configuración para el manejo de archivos estáticos en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
