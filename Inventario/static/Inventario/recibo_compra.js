// Manejar el formulario de cliente
document.getElementById("cliente-form").addEventListener("submit", function (e) {
    e.preventDefault();

    // Obtener valores del formulario
    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const telefono = document.getElementById("telefono").value;

    // Mostrar la información del cliente
    document.getElementById("cliente-nombre").textContent = nombre;
    document.getElementById("cliente-correo").textContent = correo;
    document.getElementById("cliente-telefono").textContent = telefono;

    // Cambiar de vista: formulario -> cliente guardado
    document.getElementById("formulario-cliente").style.display = "none";
    document.getElementById("info-cliente").style.display = "block";
});

// Botón para imprimir la factura
document.querySelector(".btn-imprimir").addEventListener("click", function () {
    window.print();
});

// Mostrar el detalle del pago
function mostrarDetallePago(metodo) {
    const detallePago = document.getElementById("detalle-pago");
    const metodoPagoTexto = document.getElementById("metodo-pago");

    // Actualizar el texto del método de pago
    metodoPagoTexto.textContent = `Método de Pago: ${metodo}`;
    detallePago.style.display = "block"; // Mostrar el detalle del pago
}

    // Obtener los datos de la factura
    const clienteNombre = document.getElementById("cliente-nombre").textContent;
    const clienteCorreo = document.getElementById("cliente-correo").textContent;
    const clienteTelefono = document.getElementById("cliente-telefono").textContent;

    // Obtener la tabla de servicios (factura)
    const tablaFactura = document.querySelector(".tabla");

    // Crear el contenido en PDF
    doc.text("Factura", 20, 20);
    doc.text(`Cliente: ${clienteNombre}`, 20, 30);
    doc.text(`Correo: ${clienteCorreo}`, 20, 40);
    doc.text(`Teléfono: ${clienteTelefono}`, 20, 50);

    // Añadir la tabla de servicios al PDF
    doc.autoTable({ 
        html: tablaFactura, 
        startY: 60,
        theme: 'grid',
    });

    // Añadir totales al PDF
    const totales = document.querySelector(".totales").textContent;
    doc.text(totales, 20, doc.autoTableEndPosY() + 10);

    // Guardar el archivo PDF con un nombre único
    const fecha = new Date().toISOString().slice(0, 10); // Obtener la fecha actual en formato yyyy-mm-dd
    const nombreArchivo = `Factura_${fecha}_01234.pdf`; // Nombre del archivo con fecha y número de factura
    doc.save(nombreArchivo); // Guardar el archivo PDF

    // Esto abrirá la ventana para descargar el PDF

