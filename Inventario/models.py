# Importaciones necesarias de Django para definir modelos
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Clase que define un gestor de usuarios personalizado para manejar la creación de usuarios
class UsuarioManager(BaseUserManager):
    """
    Gestor de usuarios personalizado para crear usuarios y superusuarios.
    """

    def create_user(self, usuario, contrasena=None, **extra_fields):
        """
        Crea y guarda un usuario regular con nombre de usuario y contraseña.
        """
        # Verifica que se proporcione el nombre de usuario
        if not usuario:
            raise ValueError('El nombre de usuario debe ser proporcionado')
        
        # Crea el usuario con los datos proporcionados
        usuario = self.model(usuario=usuario, **extra_fields)
        # Encripta la contraseña y la asigna al usuario
        usuario.set_password(contrasena)
        # Guarda el usuario en la base de datos
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, usuario, contrasena=None, **extra_fields):
        """
        Crea y guarda un superusuario con nombre de usuario y contraseña.
        """
        # Define que este usuario es parte del personal y tiene permisos de superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Crea el superusuario con los datos proporcionados
        return self.create_user(usuario, contrasena, **extra_fields)


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
    # Indica si el usuario tiene permisos de superusuario
    is_superuser = models.BooleanField(default=False)

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


# Clase que define el modelo de Venta
class Venta(models.Model):
    """
    Modelo que define las ventas realizadas en el sistema.
    """
    # Clave primaria autoincremental para la venta
    id_venta = models.AutoField(primary_key=True)
    # Relación con el usuario que realizó la venta
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    # Relación con el cliente al que se realizó la venta
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # Relación muchos a muchos con los productos vendidos
    id_producto = models.ManyToManyField(Producto)
    # Fecha en que se realizó la venta
    fecha = models.DateField()
    # Total de la venta (opcional), calculado con el método `calcular_total`
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calcular_total(self):
        """
        Calcula el total de la venta sumando los precios de todos los productos en la venta.
        """
        # Calcula la suma de los precios de todos los productos en la venta
        total = sum(producto.precio for producto in self.id_producto.all())
        # Asigna el total calculado al campo 'total'
        self.total = total
        # Guarda los cambios en la base de datos
        self.save()
        return total

    def __str__(self):
        """
        Representación en cadena del objeto Venta con fecha y total.
        """
        return f"Fecha: {self.fecha}, Total: {self.total}"
