from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProductoForm
from datetime import datetime  
from Inventario.models import (
    Usuario,
    Categoria,
    Producto,)
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import logging

logger = logging.getLogger(__name__)

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
                    return redirect('categorias')  # Redirige a la vista de categorías
                else:
                    messages.error(request, 'Datos incorrectos. Intenta nuevamente.')  # Error de contraseña
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')  # Error si el usuario no existe
        else:
            messages.error(request, 'Por favor, completa todos los campos.')  # Error si algún campo está vacío
    
    return render(request, 'login.html')  # Renderiza la plantilla de inicio de sesión

# Vista para registrar un nuevo usuario
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Autenticar y hacer login automáticamente después del registro
                login(request, user)
                messages.success(request, 'Cuenta creada exitosamente')
                return redirect('login')  
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

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
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.disponible = True if producto.stock > 0 else False
            producto.save()
            return redirect('categorias')  # Changed from 'menu'
        else:
            print(form.errors)  # Para debug
    else:
        form = ProductoForm()

    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'form': form, 'categorias': categorias})

# Vista para editar un producto
def editar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    categoria_original = producto.categoria

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            nuevo_producto = form.save(commit=False)
            nuevo_producto.categoria = categoria_original
            nuevo_producto.disponible = nuevo_producto.stock > 0
            nuevo_producto.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'producto': {
                        'nombre': nuevo_producto.nombre,
                        'precio': float(nuevo_producto.precio),
                        'stock': nuevo_producto.stock,
                        'disponible': nuevo_producto.disponible,
                        'descripcion': nuevo_producto.descripcion,
                        'id_producto': nuevo_producto.id_producto
                    },
                    'message': 'Producto actualizado correctamente'
                })
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Devolver errores más descriptivos
                errors = {field: str(error[0]) for field, error in form.errors.items()}
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error en el formulario',
                    'errors': errors
                }, status=400)

    # Para peticiones GET o formularios inválidos
    productos = categoria_original.productos.all()
    return render(request, 'productos.html', {
        'form': form,
        'producto': producto,
        'categoria': categoria_original,
        'productos': productos
    })


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
def agregar_al_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    carrito = request.session.get('carrito', [])

    # Convertir el precio a float
    precio = float(producto.precio)

    for item in carrito:
        if item['id'] == producto.id:
            item['cantidad'] += 1
            break
    else:
        carrito.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': precio,  # Asegurarse de que sea un número
            'cantidad': 1,
        })

    request.session['carrito'] = carrito
    return redirect('recibo_compra')

@ensure_csrf_cookie
def actualizar_carrito(request):
    logger.info("=== INICIANDO ACTUALIZAR_CARRITO ===")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            carrito = data.get('carrito', [])
            
            if not carrito:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Carrito vacío'
                })
            
            # Procesar el carrito
            for item in carrito:
                precio_str = str(item['precio']).strip().replace(',', '.')
                item['precio'] = round(float(precio_str), 2)
                item['cantidad'] = int(item['cantidad'])
                item['total'] = round(item['precio'] * item['cantidad'], 2)
            
            request.session['carrito'] = carrito
            request.session.modified = True
            
            return JsonResponse({
                'status': 'success',
                'message': 'Carrito actualizado correctamente'
            })
            
        except Exception as e:
            logger.error("Error en actualizar_carrito: %s", str(e))
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    })
'''
def recibo_compra(request):
    logger.info("=== Iniciando vista recibo_compra ===")
    carrito = request.session.get('carrito', [])
    cliente_data = request.session.get('cliente_data', {})
    
    if not carrito:
        messages.error(request, 'No hay productos en el carrito')
        return redirect('producto')  # Changed from 'menu'

    try:
        # Procesar carrito
        for item in carrito:
            precio = float(str(item['precio']).replace(',', '.'))
            cantidad = int(item['cantidad'])
            item['total'] = precio * cantidad
        
        subtotal = sum(item['total'] for item in carrito)
        total = subtotal

        context = {
            'carrito': carrito,
            'subtotal': round(subtotal, 2),
            'total': round(total, 2),
            'fecha_venta': datetime.now(),
            #'factura': { datetime.now().strftime('%Y%m%d%H%M%S')},
            'cliente': cliente_data  # Usar los datos del cliente
        }
        
        return render(request, 'recibo_compra.html', context)
    
    except Exception as e:
        logger.error("Error en recibo_compra: %s", str(e))
        messages.error(request, f'Error al generar el recibo: {str(e)}')
        return redirect('recibo_compra')  # Changed from 'menu'
'''
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
    

    
    
def recibo_compra(request):
    logger.info("=== Iniciando vista recibo_compra ===")
    
    carrito = request.session.get('carrito', [])
    metodo_pago = request.session.get('metodo_pago', 'No especificado')  # Recupera el método de pago
    nombre_cliente = request.session.get('nombre_cliente', 'Nombre no proporcionado')
    correo_cliente = request.session.get('correo_cliente', 'Correo no proporcionado')
    telefono_cliente = request.session.get('telefono_cliente', 'Teléfono no proporcionado')
    direccion_cliente = request.session.get('direccion_cliente', 'Dirección no proporcionada')

    # Recuperar el descuento desde la sesión o establecerlo a 0 si no está presente
    descuento = request.session.get('descuento', 0)
    
    logger.info("Carrito recuperado de sesión: %s", carrito)

    if not carrito:
        logger.warning("No hay productos en el carrito")
        messages.error(request, 'No hay productos en el carrito')
        return redirect('categorias')

    try:
        # Procesando los items del carrito
        for item in carrito:
            if 'total' not in item:
                precio = float(str(item['precio']).replace(',', '.'))
                cantidad = int(item['cantidad'])
                item['total'] = precio * cantidad
        
        subtotal = sum(item['total'] for item in carrito)
        
        # Aplicar el descuento al subtotal
        descuento_monto = subtotal * (descuento / 100)
        total = subtotal - descuento_monto

        # Contexto con los datos del cliente y el carrito
        context = {
            'carrito': carrito,
            'subtotal': round(subtotal, 2),
            'descuento': round(descuento_monto, 2),
            'total': round(total, 2),
            'fecha_venta': datetime.now(),
            'factura': datetime.now().strftime('%Y%m%d%H%M%S'),
            'direccion': 'Cra 4 #70-22 Conjunto Vaparaiso Local 44',
            'cliente': {
                'nombre': nombre_cliente,
                'correo': correo_cliente,
                'telefono': telefono_cliente,
                'direccion': direccion_cliente,
            },
            'metodo_pago': metodo_pago,  # Agregar el método de pago al contexto
        }

        logger.info("Context preparado exitosamente")
        return render(request, 'recibo_compra.html', context)
    
    except Exception as e:
        logger.error("Error en recibo_compra: %s", str(e), exc_info=True)
        messages.error(request, f'Error al generar el recibo: {str(e)}')
        return redirect('categorias')