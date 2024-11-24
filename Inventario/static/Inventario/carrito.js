document.addEventListener("DOMContentLoaded", function () {
    const productoImgs = document.querySelectorAll(".producto-img");
    const carritoCantidad = document.getElementById("cantidadCarrito");
    const listaCarrito = document.querySelector("#listaCarrito tbody");
    const carritoVacio = document.getElementById("carritoVacio");

    // Array para almacenar los productos en el carrito
    const carrito = [];

    // Función para agregar producto al carrito
    function agregarAlCarrito(productId, productoCard) {
        // Extraer los datos del producto desde la tarjeta asociada
        const nombre = productoCard.querySelector(".card-title").textContent.trim();
        const precio = parseFloat(
            productoCard.querySelector(".card-text strong").nextSibling.textContent.trim().slice(1)
        );

        console.log(`Agregando producto: ${nombre}, Precio: ${precio}, ID: ${productId}`);

        // Verificar si el producto ya existe en el carrito
        const productoExistente = carrito.find(producto => producto.nombre === nombre && producto.precio === precio);

        if (productoExistente) {
            // Si el producto ya existe, incrementar la cantidad
            productoExistente.cantidad += 1;
        } else {
            // Crear una entrada única para este producto si no existe en el carrito
            const productoUnico = {
                id: `${productId}-${Date.now()}`, // ID único generado dinámicamente
                nombre: nombre,
                precio: precio,
                cantidad: 1,
            };
            carrito.push(productoUnico);
        }

        // Actualizar el contador y la vista del carrito
        actualizarCarritoCantidad();
        renderizarCarrito();
    }

    // Actualiza el número total de productos en el carrito
    function actualizarCarritoCantidad() {
        const totalCantidad = carrito.reduce((total, producto) => total + producto.cantidad, 0);
        carritoCantidad.textContent = totalCantidad;
    }

    // Renderiza el contenido del carrito en el modal
    function renderizarCarrito() {
        listaCarrito.innerHTML = ""; // Limpiar contenido previo

        // Si el carrito está vacío, mostrar mensaje "carrito vacío"
        if (carrito.length === 0) {
            carritoVacio.classList.remove("d-none");
            return;
        }

        carritoVacio.classList.add("d-none"); // Ocultar mensaje "carrito vacío"

        // Crear una fila por cada producto en el carrito
        carrito.forEach((producto, index) => {
            const subtotal = producto.precio * producto.cantidad; // Calcular subtotal
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${producto.nombre}</td>
                <td>${producto.precio.toFixed(2)} $</td>
                <td>
                    <button class="btn btn-sm btn-secondary" onclick="actualizarCantidad(${index}, -1)">-</button>
                    ${producto.cantidad}
                    <button class="btn btn-sm btn-secondary" onclick="actualizarCantidad(${index}, 1)">+</button>
                </td>
                <td>${subtotal.toFixed(2)} €</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="eliminarProducto(${index})">Eliminar</button>
                </td>
            `;
            listaCarrito.appendChild(row);
        });
    }

    // Actualiza la cantidad de un producto
    window.actualizarCantidad = function (index, delta) {
        if (carrito[index]) {
            carrito[index].cantidad += delta;
            if (carrito[index].cantidad <= 0) {
                carrito.splice(index, 1); // Eliminar el producto si la cantidad es 0
            }
            actualizarCarritoCantidad();
            renderizarCarrito();
        }
    };

    // Elimina un producto del carrito
    window.eliminarProducto = function (index) {
        if (carrito[index]) {
            carrito.splice(index, 1); // Eliminar el producto del carrito
            actualizarCarritoCantidad();
            renderizarCarrito();
        }
    };

    // Vaciar el carrito
    document.getElementById("vaciarCarrito").addEventListener("click", function () {
        carrito.length = 0; // Vaciar el array del carrito
        actualizarCarritoCantidad();
        renderizarCarrito();
    });

    // Evento para agregar productos al carrito
    productoImgs.forEach((img) => {
        img.addEventListener("click", function () {
            const productId = img.getAttribute("data-id"); // Obtener ID único del producto
            const productoCard = img.closest(".card"); // Obtener tarjeta asociada a la imagen
            agregarAlCarrito(productId, productoCard);
        });
    });

    // Proceder a la compra
    document.getElementById("procederCompra").addEventListener("click", function () {
        if (carrito.length === 0) {
            alert("El carrito está vacío. Por favor, agrega productos antes de proceder.");
            return;
        }
        alert("Gracias por tu compra. Este es solo un ejemplo, aquí puedes redirigir al sistema de pago.");
        carrito.length = 0; // Vaciar carrito después de la compra
        actualizarCarritoCantidad();
        renderizarCarrito();
    });
});
