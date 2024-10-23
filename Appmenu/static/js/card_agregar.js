// lourdessushi/Appmenu/static/js/card_agregar.js

const CREAR_CARRITO_URL = '/crear-carrito/';  // Cambia esta URL si es necesario
const AGREGAR_PRODUCTO_CARRITO_URL = '/agregar-producto-al-carrito/';  // Cambia esta URL si es necesario

// Escuchar el clic en los botones de agregar al carrito
document.addEventListener('click', function(event) {
    if (event.target.matches('[id^="boton-agregar-carrito-"]')) {
        event.preventDefault();  // Evita cualquier acción predeterminada del botón
        const boton = event.target.closest('button');  // Obtenemos el botón real en caso de que se haya hecho clic en el ícono
        const emprendimientoId = boton.dataset.emprendimientoId;  // Obtiene el ID del emprendimiento
        const productoId = boton.dataset.productoId;  // Obtiene el ID del producto
        const cantidad = 1;  // Fija la cantidad en 1

        crearCarritoYAgregarProducto(emprendimientoId, productoId, cantidad);  // Llama a la función para crear carrito y agregar producto
    }
});



// Función para verificar si el UUID es válido
function isValidUUID(uuid) {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    return uuidRegex.test(uuid);
}

// Definir el nombre de la cookie CSRF token
const CSRF_TOKEN_COOKIE_NAME = 'csrftoken';

// Función para obtener el valor de la cookie dado su nombre
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Función para crear carrito y agregar producto
// Función para crear carrito y agregar producto
function crearCarritoYAgregarProducto(emprendimientoId, productoId, cantidadProducto) {
    const csrftoken = getCookie(CSRF_TOKEN_COOKIE_NAME);
    console.log('CSRF Token:', csrftoken);
    console.log('ID del emprendimiento:', emprendimientoId);
    console.log('ID del producto:', productoId);

    if (emprendimientoId === undefined) {        
        console.error('El ID del emprendimiento no se ha proporcionado.');        
        return; 
    }
    // Validar si el productoId es un UUID válido
    if (!isValidUUID(productoId)) {
        console.error('El ID del producto no es un UUID válido:', productoId);
        return;
    }

    // Validar cantidad
    if (isNaN(cantidadProducto) || cantidadProducto <= 0) {
        console.error('La cantidad debe ser un número positivo.');
        return;
    }

    // Crear carrito
    fetch(`${CREAR_CARRITO_URL}${emprendimientoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Incluyendo el CSRF token
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        const carritoId = data.id;
        console.log('ID del carrito creado:', carritoId); // Añadido para depuración
        agregarProductoAlCarrito(carritoId, productoId, cantidadProducto);
    })
    .catch(error => console.error('Error al crear carrito:', error));
}

// Función para agregar un producto al carrito
function agregarProductoAlCarrito(carritoId, productoId, cantidadProducto) {
    const csrftoken = getCookie(CSRF_TOKEN_COOKIE_NAME);
    console.log('CSRF Token:', csrftoken);
    console.log('ID del carrito:', carritoId);
    console.log('ID del producto:', productoId);
    document.dispatchEvent(new CustomEvent('carritoActualizado'))
    fetch(`${AGREGAR_PRODUCTO_CARRITO_URL}${carritoId}/${productoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Incluyendo el CSRF token
        },
        body: JSON.stringify({
            cantidad: cantidadProducto,
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error('Respuesta de la solicitud:', text);
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Producto agregado:', data);

        // Actualiza el contador del carrito
        const contadorProductos = document.getElementById("contador-productos");
        let cantidadActual = parseInt(contadorProductos.textContent) || 0;
        contadorProductos.textContent = cantidadActual + 1;  // Incrementa la cantidad actual

        // Dispara evento personalizado
        document.dispatchEvent(new CustomEvent('carritoActualizado'));
    })
    .catch((error) => {
        console.error('Error al agregar producto:', error);
    });
}


