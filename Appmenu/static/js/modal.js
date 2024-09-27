//Appmenu/static/js/modal.js
document.addEventListener("DOMContentLoaded", function() {
    // Obtener el modal y el botón de cerrar
    var modal = document.getElementById("myModal");

    if (modal) {
        var closeButton = modal.querySelector(".close");

        if (closeButton) {
            // Cuando el usuario hace clic en el botón de cerrar, ocultar el modal
            closeButton.onclick = function() {
                modal.style.display = "none";
            };

            // Cuando el usuario hace clic en cualquier parte fuera del modal, ocultar el modal
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            };
        }

        // Función para mostrar el modal con título, contenido y precio específicos
        window.showModal = function(title, content, publicPrice) {
            var modalTitle = modal.querySelector("#modal-title");
            var modalContent = modal.querySelector("#modal-content");
            var modalPublicPrice = modal.querySelector("#modal-precio"); // Corregido aquí

            if (modalTitle && modalContent && modalPublicPrice) {
                modalTitle.textContent = title;
                modalContent.textContent = content;
                modalPublicPrice.textContent = "Precio público: $" + publicPrice;
            }

            modal.style.display = "block";
        };
    }
});

