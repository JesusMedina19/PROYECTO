from django.contrib import admin
from .models import (
    Usuario,
    Cliente,
    Categoria,
    Producto,
    Venta
)
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Venta)