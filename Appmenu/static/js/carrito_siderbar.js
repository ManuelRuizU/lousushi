// lourdessushi/Appmenu/static/js/carrito_siderbar.js

class Carrito {
    constructor() {
        this.id = ""; // UUID
        this.emprendimientoId = ""; // ID del emprendimiento asociado
        this.productos = []; // Arreglo de productos
        this.nombreComprador = "";
        this.apellidoComprador = "";
        this.direccionDespacho = ""; // ID de la dirección de despacho
        this.telefonoContacto = "";
        this.nota = "";
        this.fechaCreacion = ""; // Fecha de creación
        this.descuento = 0;
        this.valorEnvio = 0;
        this.total = 0;
        this.completo = false;
        this.cupon = ""; // ID del cupon de descuento
        this.metodoPago = "";
    }
}

document.addEventListener('carritoActualizado', function() {
    mostrarCarrito();
});

// Obtener el ID del emprendimiento
function obtenerEmprendimientoId() {
    return fetch('/api/emprendimiento/obtener-id')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al obtener ID del emprendimiento: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => data.emprendimiento_id)
        .catch(error => {
            console.error('Error al obtener ID del emprendimiento:', error);
            return null;
        });
}

// Obtener el carrito del LocalStorage
function obtenerCarritoLocalStorage(emprendimientoId) {
    const carritoLocalStorage = localStorage.getItem(`carrito-${emprendimientoId}`);
    return carritoLocalStorage ? JSON.parse(carritoLocalStorage) : new Carrito();
}

// Guardar el carrito en el LocalStorage
function guardarCarritoLocalStorage(emprendimientoId, carrito) {
    localStorage.setItem(`carrito-${emprendimientoId}`, JSON.stringify(carrito));
}

// Buscar producto dinámicamente
let productos = [];
fetch('/api/obtener-productos/')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Productos obtenidos:", data);
        productos = data;
    })
    .catch(error => console.error('Error al obtener productos:', error));



function buscarcarrito(carritoId) {
    console.log("Buscando carrito con ID:", carritoId);
    const carrito = carrito.find(carrito => carrito.id === carritoId);
    console.log("Producto encontrado:", carrito);
    return carrito;
}

function buscarProducto(productoId) {
    console.log("Buscando producto con ID:", productoId);
    const producto = productos.find(producto => producto.id === productoId);
    console.log("Producto encontrado:", producto);
    return producto;
}

// Agregar producto al carrito
function agregarProductoAlCarrito(productoId, cantidad) {
    obtenerEmprendimientoId()
        .then(emprendimientoId => {
            const carrito = obtenerCarritoLocalStorage(emprendimientoId);
            const producto = buscarProducto(productoId);
            if (!producto) {
                console.error("Producto no encontrado");
                return;
            }
            const productoEnCarrito = carrito.productos.find((p) => p.id === productoId);
            if (productoEnCarrito) {
                productoEnCarrito.cantidad += cantidad;
            } else {
                carrito.productos.push({ ...producto, cantidad });
            }
            carrito.total = carrito.productos.reduce((total, producto) => total + producto.cantidad * producto.precio, 0);
            guardarCarritoLocalStorage(emprendimientoId, carrito);
            console.log("Carrito después de agregar producto:", carrito);
            document.dispatchEvent(new CustomEvent('carritoActualizado'));
        })
        .catch(error => {
            console.error('Error al agregar producto al carrito:', error);
        });
}


// Mostrar carrito
function mostrarCarrito() {
    obtenerEmprendimientoId()
        .then(emprendimientoId => {
            const carrito = obtenerCarritoLocalStorage(emprendimientoId);
            const contenidoSidebar = document.getElementById("carrito-sidebar");
            contenidoSidebar.innerHTML = carritoInnerHtml(carrito);
        })
        .catch(error => {
            console.error('Error al mostrar carrito:', error);
        });
}

function carritoInnerHtml(carrito) {
    let innerHtml = "";
    innerHtml += `
        <div>
            <h4>Información del carrito</h4>
            <p>Nombre del comprador: ${carrito.nombreComprador}</p>
            <p>Apellido del comprador: ${carrito.apellidoComprador}</p>
            <p>Teléfono de contacto: ${carrito.telefonoContacto}</p>
            <p>Dirección de despacho: ${carrito.direccionDespacho}</p>
            <p>Descuento: ${carrito.descuento}</p>
            <p>Valor de envío: ${carrito.valorEnvio}</p>
        </div>
    `;
    carrito.productos.forEach((producto) => {
        innerHtml += `
            <div>
                <h4>${producto.nombre}</h4>
                <p>Cantidad: ${producto.cantidad}</p>
                <p>Precio: ${producto.precio}</p>
            </div>
        `;
    });
    innerHtml += `
        <div>
            <h4>Total: ${carrito.total}</h4>
        </div>
    `;
    return innerHtml;
}

// Helper para obtener el token CSRF si está habilitado
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




