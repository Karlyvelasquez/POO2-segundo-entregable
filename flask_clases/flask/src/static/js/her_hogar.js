document.addEventListener('DOMContentLoaded', function () {
    const mostrador = document.getElementById("mostrador");
    const seleccion = document.getElementById("seleccion");
    const imgSeleccionada = document.getElementById("img");
    const modeloSeleccionado = document.getElementById("modelo");
    const descripSeleccionada = document.getElementById("descripcion");
    const precioSeleccionado = document.getElementById("precio");

    function cargar(item) {
        quitarBordes();
        mostrador.style.width = "80%";
        seleccion.style.display = "flex"; 
        seleccion.style.width = "70%";
        seleccion.style.opacity = "1";

        const idProducto = item.getAttribute("data-id");

        fetch(`/producto/${idProducto}`)
            .then(response => response.json())
            .then(data => {
                imgSeleccionada.src = data.imagen_url || '/static/images/default.png';
                modeloSeleccionado.textContent = data.nombre || 'Sin nombre';
                descripSeleccionada.textContent = data.descripcion || 'Sin descripción';
                precioSeleccionado.textContent = `$ ${data.precio || 0}`;
            })
            .catch(error => {
                console.error('Error al cargar los datos del producto:', error);
            });
    }

    function quitarBordes() {
        document.querySelectorAll(".item").forEach(item => {
            item.style.border = "none";
        });
    }

    function cerrar() {
        mostrador.style.width = "100%";
        seleccion.style.width = "0";
        seleccion.style.opacity = "0";
        seleccion.style.display = "none"; 
        quitarBordes();
    }

    document.querySelectorAll('.item').forEach(item => {
        item.addEventListener('click', function () {
            cargar(this);
        });
    });

    document.querySelector('.cerrar').addEventListener('click', cerrar);
});
