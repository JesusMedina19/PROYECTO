from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('menu/',views.menu_view,name="menu"),
    path('categorias/', views.categorias_view, name='categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/modificar/<int:id_categoria>/', views.modificar_categoria, name='modificar_categoria'),
    path('categorias/eliminar/<int:id_categoria>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('productos/<int:id_categoria>/', views.ver_productos, name='productos'), 
    path('editar_producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
    path('agregar_al_carrito/<str:nombre>/<str:precio>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('mostrar_carrito/', views.mostrar_carrito, name='mostrar_carrito'),
    path('recibo_compra/', views.recibo_compra, name='recibo_compra'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
