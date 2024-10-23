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
            window.addEventListener('click', function(event) {
                if (event.target === modal) {
                    modal.style.display = "none";
                }
            });
        }

        // Función para mostrar el modal con título y contenido específicos
        window.showModal = function(title, content) {
            var modalTitle = modal.querySelector("#modal-title");
            var modalContent = modal.querySelector("#modal-content");
        
            if (modalTitle && modalContent) {
                modalTitle.textContent = title || "Sin título";
                modalContent.textContent = content || "Sin contenido";
                modal.style.display = "block";
            } else {
                console.error("Elementos del modal no encontrados.");
            }
        };
        
    }
});

