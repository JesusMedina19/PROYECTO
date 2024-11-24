from django.http import HttpResponse,JsonResponse
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProductoForm
from Inventario.models import Usuario, Categoria, Producto,Cliente
from datetime import datetime  


# Vista para ingresar a la aplicación (inicio de sesión)
def login_view(request):
    """
    Vista que maneja el inicio de sesión del usuario. Recibe los datos de usuario y contraseña
    y verifica si el usuario existe y la contraseña es correcta. Si los datos son correctos,
    se redirige a la vista de categorías. En caso contrario, se muestra un mensaje de error.
    """
    if request.method == 'POST':
        username = request.POST.get('username')  # Obtiene el nombre de usuario
        password = request.POST.get('password')  # Obtiene la contraseña

        if username and password:  # Verifica que ambos campos sean no vacíos
            try:
                user = Usuario.objects.get(usuario=username)  # Busca el usuario en la base de datos
                if user.check_password(password):  # Verifica si la contraseña es correcta
                    login(request, user)  # Inicia sesión al usuario
                    return redirect('menu')  # Redirige a la vista de categorías
                else:
                    messages.error(request, 'Datos incorrectos. Intenta nuevamente.')  # Error de contraseña
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')  # Error si el usuario no existe
        else:
            messages.error(request, 'Por favor, completa todos los campos.')  # Error si algún campo está vacío
    
    return render(request, 'login.html')  # Renderiza la plantilla de inicio de sesión


# Vista para registrar un nuevo usuario
def register_view(request):
    """
    Vista para registrar un nuevo usuario. Si se envían datos válidos, se guarda el nuevo usuario
    y se redirige al inicio de sesión. Si hay errores en el formulario, se muestran mensajes de error.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Obtiene los datos del formulario
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda el nuevo usuario
            messages.success(request, 'Cuenta creada con éxito')  # Mensaje de éxito
            return redirect('login')  # Redirige a la página de inicio de sesión
        else:
            messages.error(request, 'Error al crear la cuenta. Por favor, verifica los errores.')  # Error de validación
    else:
        form = CustomUserCreationForm()  # Si no es POST, crea un formulario vacío

    return render(request, 'register.html', {'form': form})  # Renderiza la plantilla de registro


# Vista para mostrar categorías
def categorias_view(request):
    """
    Vista que muestra todas las categorías en el inventario. Se obtienen todos los objetos de tipo
    Categoria y se pasan a la plantilla para su visualización.
    """
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    return render(request, 'categorias.html', {'categorias': categorias})  # Renderiza la plantilla con las categorías


# Vista para crear una nueva categoría
def crear_categoria(request):
    """
    Vista que permite crear una nueva categoría. Si se envía el nombre de la categoría,
    se crea y redirige a la vista de categorías.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')  # Obtiene el nombre de la nueva categoría
        if nombre:
            Categoria.objects.create(nombre=nombre)  # Crea la nueva categoría
            return redirect('categorias')  # Redirige a la lista de categorías
        else:
            return HttpResponse("Error: No se recibió el nombre de la categoría.")  # Si no se recibe el nombre
    return HttpResponse("Error: No se permite acceso directo.")  # Si no es un POST


# Vista para modificar una categoría existente
def modificar_categoria(request, id_categoria):
    """
    Vista que permite modificar una categoría existente. Se obtiene la categoría mediante su ID
    y se actualiza su nombre. Luego, se redirige a la lista de categorías.
    """
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)  # Obtiene la categoría por ID
    if request.method == 'POST':
        categoria.nombre = request.POST['nombre']  # Modifica el nombre de la categoría
        categoria.save()  # Guarda los cambios
        return redirect('categorias')  # Redirige a la lista de categorías
    return render(request, 'categorias.html', {'categoria': categoria})  # Renderiza la vista con los datos de la categoría


# Vista para eliminar una categoría
def eliminar_categoria(request, id_categoria):
    """
    Vista que permite eliminar una categoría. Se obtiene la categoría por su ID y, si es un POST,
    se elimina y redirige a la lista de categorías.
    """
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)  # Obtiene la categoría por ID
    if request.method == 'POST':
        categoria.delete()  # Elimina la categoría
        return redirect('categorias')  # Redirige a la lista de categorías
    return HttpResponse("Error: No se permite acceso directo.")  # Si no es un POST


# Vista para agregar un nuevo producto
def agregar_producto(request):
    """
    Vista para agregar un nuevo producto. Si se recibe un formulario válido, se guarda el producto
    y se redirige al menú. Si el formulario no es válido, se muestran los errores.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # Obtiene los datos del formulario y archivos
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda el nuevo producto
            return redirect('menu')  # Redirige al menú
    else:
        form = ProductoForm()  # Si no es un POST, crea un formulario vacío

    categorias = Categoria.objects.all()  # Obtiene todas las categorías de la base de datos
    return render(request, 'menu.html', {'form': form, 'categorias': categorias})
# Vista para editar un producto
def editar_producto(request, id_producto):
    """
    Vista para editar un producto existente. Se obtiene el producto por su ID y, si se envían datos
    válidos, se guardan los cambios. Luego, se redirige a la lista de productos de la categoría correspondiente.
    """
    producto = get_object_or_404(Producto, id_producto=id_producto)  # Obtiene el producto por ID

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)  # Prellena el formulario con los datos del producto
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda los cambios
            return redirect('productos', id_categoria=producto.categoria.id_categoria)  # Redirige a los productos de la categoría
    else:
        form = ProductoForm(instance=producto)  # Si no es POST, crea un formulario con los datos del producto

    return render(request, 'productos.html', {'form': form, 'producto': producto})  # Renderiza la plantilla con el formulario y el producto


# Vista para eliminar un producto
def eliminar_producto(request, id_producto):
    """
    Vista para eliminar un producto. Se obtiene el producto por su ID, se elimina y se redirige a la lista
    de productos de la categoría correspondiente.
    """
    producto = get_object_or_404(Producto, id_producto=id_producto)  # Obtiene el producto por ID
    id_categoria = producto.categoria.id_categoria  # Obtiene el ID de la categoría del producto
    producto.delete()  # Elimina el producto
    return redirect('productos', id_categoria=id_categoria)  # Redirige a los productos de la categoría correspondiente


# Vista para ver los productos de una categoría
def ver_productos(request, id_categoria):
    """
    Vista para ver los productos de una categoría específica. Se obtienen todos los productos de la categoría
    y se pasan a la plantilla para su visualización.
    """
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)  # Obtiene la categoría por ID
    productos = categoria.productos.all()  # Obtiene todos los productos de esa categoría
    return render(request, 'productos.html', {'categoria': categoria, 'productos': productos})  # Renderiza la plantilla con los productos

#Vista agregar al carrito
def agregar_al_carrito(request, nombre, precio):
    # Verificar si existe la clave 'carrito' en la sesión
    if 'carrito' not in request.session:
        request.session['carrito'] = []  # Crear carrito si no existe

    # Trabajar con el carrito de la sesión directamente
    carrito = request.session['carrito']

    # Convertir el precio a float y manejar errores
    try:
        precio = float(precio)
    except ValueError:
        return JsonResponse({"success": False, "message": "Precio inválido"})

    # Buscar el producto en el carrito por su nombre y precio
    producto_existente = None
    for producto in carrito:
        if producto['nombre'] == nombre and producto['precio'] == precio:
            producto_existente = producto
            break  # Romper el bucle una vez que encontramos el producto

    if producto_existente:
        # Si el producto ya existe, incrementar la cantidad y actualizar el subtotal
        producto_existente['cantidad'] += 1
        producto_existente['subtotal'] = producto_existente['cantidad'] * producto_existente['precio']
    else:
        # Si no existe, agregarlo como un nuevo producto con cantidad 1
        producto_id = str(uuid4())  # Generar un ID único
        nuevo_producto = {
            'id': producto_id,
            'nombre': nombre,
            'precio': precio,
            'cantidad': 1,
            'subtotal': precio
        }
        carrito.append(nuevo_producto)

    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito
    request.session.modified = True  # Marcar la sesión como modificada

    return JsonResponse({
        "success": True,
        "message": "Producto agregado al carrito",
        "carrito": carrito
    })

#Mostrar carrito
def mostrar_carrito(request):
    # Obtiene el carrito de la sesión
    carrito = request.session.get('carrito', [])
    
    # Calcula el total sumando el precio de todos los productos en el carrito
    total = sum(item['precio'] for item in carrito)

    # Devuelve el carrito y el total en formato JSON
    return JsonResponse({
        'carrito': carrito,
        'total': total
    })
    
    
def menu_view(request):
    return render(request, "menu.html")

def recibo_compra(request):
    # Obtener el carrito desde la sesión
    carrito = request.session.get('carrito', [])

    # Validar que el carrito no esté vacío
    if not carrito:
        carrito = []

    # Procesar el formulario de cliente
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')  # Capturar la dirección

        # Guardar la información del cliente en la base de datos
        cliente = Cliente.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion
        )

        # Renderizar el recibo con los datos del cliente
        subtotal = sum(item['precio'] * item['cantidad'] for item in carrito)
        return render(request, 'recibo_compra.html', {
            'carrito': carrito,
            'subtotal': subtotal,
            'total': subtotal,
            'fecha_venta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cliente': cliente,  # Pasar el cliente a la plantilla
        })

    # Renderizar la página sin procesar el formulario
    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito)
    return render(request, 'recibo_compra.html', {
        'carrito': carrito,
        'subtotal': subtotal,
        'total': subtotal,
        'fecha_venta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })