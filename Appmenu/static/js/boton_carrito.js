// lourdessushi/Appmenu/static/js/boton_carrito.js

document.addEventListener("DOMContentLoaded", function() {
  const carritoSidebar = document.getElementById("sidebar-carrito"); // Obtener el sidebar del carrito
  const carritoBtn = document.getElementById("carritoBtn"); // Botón para abrir el carrito
  const cerrarBtn = document.querySelector(".cerrar-sidebar"); // Botón para cerrar el carrito

  // Abrir el sidebar cuando se hace clic en el botón del carrito
  carritoBtn.addEventListener("click", function() {
      console.log("Abriendo sidebar del carrito");
      carritoSidebar.classList.add("sidebar-abierto"); // Agregar clase para mostrar el sidebar
  });

  // Cerrar el sidebar cuando se hace clic en el botón de cerrar
  cerrarBtn.addEventListener("click", function() {
      console.log("Cerrando sidebar del carrito");
      carritoSidebar.classList.remove("sidebar-abierto"); // Quitar clase para ocultar el sidebar
  });

  // Cerrar el sidebar si el usuario hace clic fuera de él
  window.addEventListener("click", function(event) {
      if (event.target === carritoSidebar) {
          console.log("Cerrando sidebar al hacer clic fuera");
          carritoSidebar.classList.remove("sidebar-abierto"); // Quitar clase para ocultar el sidebar
      }
  });
});
