document.addEventListener('DOMContentLoaded', function() {
    const productImages = document.querySelectorAll('.product-image'); // Selector de las imágenes de los productos
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    productImages.forEach(image => {
        image.addEventListener('click', function() {
            const productId = this.dataset.id; // Suponiendo que tienes un atributo data-id en la imagen
            
            fetch('/agregar_al_carrito/', { // Asegúrate de usar la URL correcta de tu vista Django
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ id: productId }),
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al agregar el producto al carrito');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    alert('Producto agregado al carrito');
                    // Aquí puedes actualizar el carrito visualmente, si es necesario
                } else {
                    alert(data.message || 'No se pudo agregar el producto al carrito');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al agregar el producto al carrito:\n' + error.message);
            });
        });
    });
});
