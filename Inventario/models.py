# Importaciones necesarias de Django para definir modelos
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Clase que define un gestor de usuarios personalizado para manejar la creación de usuarios
class UsuarioManager(BaseUserManager):
    """
    Gestor de usuarios personalizado para crear usuarios y superusuarios.
    """

    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError('El usuario es obligatorio')
        
        user = self.model(
            usuario=usuario,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(usuario, password, **extra_fields)


# Clase que define el modelo personalizado de Usuario
class Usuario(AbstractBaseUser):
    """
    Modelo personalizado de usuario para autenticar a los usuarios en el sistema.
    """
    # Clave primaria autoincremental para el usuario
    id_usuario = models.AutoField(primary_key=True)
    # Nombre completo del usuario
    nombre = models.CharField(max_length=30)
    # Rol del usuario en el sistema, predeterminado a 'empleado'
    rol = models.CharField(max_length=15, default="empleado")
    # Nombre de usuario único para autenticación
    usuario = models.CharField(max_length=50, unique=True)
    # Indica si el usuario es parte del personal
    is_staff = models.BooleanField(default=False)
    # Corregir el paréntesis y usar default directamente
    is_superuser = models.BooleanField(default=False)
    # Indica si el usuario está activo
    is_active = models.BooleanField(default=True)

    # Asigna el gestor personalizado
    objects = UsuarioManager()

    # Define el campo utilizado para autenticación
    USERNAME_FIELD = 'usuario'
    # Campos adicionales requeridos para crear un usuario
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        """
        Representación en cadena del objeto Usuario.
        """
        return f'{self.nombre} ({self.usuario})'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def clean(self):
        super().clean()
        return self.usuario

    @property
    def username(self):
        return self.usuario


# Clase que define el modelo de Cliente
class Cliente(models.Model):
    """
    Modelo que define la información de un cliente.
    """
    # Clave primaria autoincremental para el cliente
    id_cliente = models.AutoField(primary_key=True)
    # Nombre completo del cliente
    nombre = models.CharField(max_length=30)
    # Correo electrónico del cliente
    correo = models.EmailField(max_length=150)
    # Dirección del cliente
    direccion = models.CharField(max_length=150)
    # Número de teléfono en formato internacional
    telefono = PhoneNumberField()

    def __str__(self):
        """
        Representación en cadena del objeto Cliente.
        """
        return self.nombre


# Clase que define el modelo de Categoría
class Categoria(models.Model):
    """
    Modelo que define las categorías de productos.
    """
    # Clave primaria autoincremental para la categoría
    id_categoria = models.AutoField(primary_key=True)
    # Nombre de la categoría de productos
    nombre = models.CharField(max_length=100)

    def __str__(self):
        """
        Representación en cadena del objeto Categoria.
        """
        return self.nombre


# Clase que define el modelo de Producto
class Producto(models.Model):
    """
    Modelo que define los productos disponibles en el inventario.
    """
    id_producto = models.AutoField(primary_key=True)
    # Nombre del producto
    nombre = models.CharField(max_length=30)
    # Precio del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Descripción del producto
    descripcion = models.TextField()
    # Cantidad en stock
    stock = models.IntegerField(default=0)
    # Imagen del producto
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    # Indica si el producto está disponible
    disponible = models.BooleanField(default=True)
    # Relación con la categoría del producto
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        """
        Representación en cadena del objeto Producto con su categoría.
        """
        return f"{self.nombre} - {self.categoria.nombre}"
    
    def save(self, *args, **kwargs):
        self.disponible = self.stock > 0
        super().save(*args, **kwargs)

    @property
    def esta_disponible(self):
        return self.stock > 0 and self.disponible

    def get_precio_formateado(self):
        return "{:.2f}".format(float(self.precio))
    
    def get_precio_input(self):
        """Formato específico para inputs type="number" """
        return f"{float(self.precio):.2f}"

    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre} (Stock: {self.stock})"


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    id_cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    id_producto = models.ManyToManyField('Producto')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta {self.id_venta} - {self.id_cliente.nombre}"
    
    def calcular_total(self):
        total = 0
        for producto in self.id_producto.all():
            total += producto.precio  # Asegúrate de que el modelo Producto tenga el campo `precio`
        self.total = total
        self.save()
