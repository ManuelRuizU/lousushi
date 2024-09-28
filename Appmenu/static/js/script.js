// script.js

// Selección de botones "Agregar al carrito"
const botonesAgregarCarrito = document.querySelectorAll('[id^="boton-agregar-carrito-"]');

// Agregar evento click a cada botón
botonesAgregarCarrito.forEach((boton) => {
    boton.addEventListener('click', () => {
        const productoId = boton.dataset.productoId;
        const productoNombre = boton.dataset.productoNombre;
        const productoPrecio = boton.dataset.productoPrecio;
        
        // Llamar a la función para agregar producto al carrito
        agregarProductoAlCarrito(productoId, productoNombre, productoPrecio);
    });
});