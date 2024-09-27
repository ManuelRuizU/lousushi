
# Appmenu/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from Appmenu.views import home, login_view, index, carrito_view, obtener_carrito

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('login/', login_view, name='login'),   
    path('carrito/', carrito_view, name='carrito'),
    path('api/carrito', obtener_carrito, name='obtener_carrito'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
