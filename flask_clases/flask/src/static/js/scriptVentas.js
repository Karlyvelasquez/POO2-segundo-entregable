$(document).ready(function () {
    const mainContent = $('#main-content');

    // Función para cargar las ventas
    function cargarVentas() {
        mainContent.html('<p>Cargando ventas...</p>');

        $.get('/ventas', function (data) {
            if (data.error) {
                mainContent.html('<p>Error al cargar las ventas.</p>');
                console.error(data.error);
                return;
            }

            let content = `<table>
                               <thead>
                                   <tr>
                                       <th>ID</th>
                                       <th>Fecha</th>
                                       <th>Empleado</th>
                                       <th>Cliente</th>
                                       <th>Total</th>
                                       <th>Acciones</th>
                                   </tr>
                               </thead>
                               <tbody>`;

            if (data.length > 0) {
                data.forEach(venta => {
                    content += `<tr>
                                    <td>${venta.id}</td>
                                    <td>${venta.fecha}</td>
                                    <td>${venta.usuario}</td>
                                    <td>${venta.cliente}</td>
                                    <td>${venta.total}</td>
                                    <td>
                                        <button class="ver-detalles" data-id="${venta.id}">Ver Detalles</button>
                                        <button class="eliminar-venta" data-id="${venta.id}">Eliminar</button>
                                    </td>
                                </tr>`;
                });
            } else {
                content += `<tr><td colspan="6">No hay ventas registradas.</td></tr>`;
            }

            content += `</tbody></table>`;
            mainContent.html(content);

        }).fail(function () {
            mainContent.html('<p>Error al cargar las ventas.</p>');
            console.error('Error al cargar las ventas');
        });
    }

    // Evento para cargar ventas
    $('#ventas').on('click', function (e) {
        e.preventDefault();
        cargarVentas();
    });

    // Ver detalles de una venta
    mainContent.on('click', '.ver-detalles', function () {
        const ventaId = $(this).data('id');
        mainContent.html('<p>Cargando detalles de la venta...</p>');

        $.get(`/venta/${ventaId}/detalles`, function (data) {
            if (data.error) {
                mainContent.html('<p>Error al cargar los detalles de la venta.</p>');
                console.error(data.error);
                return;
            }

            let content = `<button id="volver-ventas">Volver a Ventas</button>
                           <table>
                               <thead>
                                   <tr>
                                       <th>ID</th>
                                       <th>Producto</th>
                                       <th>Cantidad</th>
                                       <th>Precio</th>
                                   </tr>
                               </thead>
                               <tbody>`;

            if (data.length > 0) {
                data.forEach(detalle => {
                    content += `<tr>
                                    <td>${detalle.id}</td>
                                    <td>${detalle.producto}</td>
                                    <td>${detalle.cantidad}</td>
                                    <td>${detalle.precio}</td>
                                </tr>`;
                });
            } else {
                content += `<tr><td colspan="4">No hay detalles para esta venta.</td></tr>`;
            }

            content += `</tbody></table>`;
            mainContent.html(content);
        }).fail(function () {
            mainContent.html('<p>Error al cargar los detalles de la venta.</p>');
            console.error('Error al cargar los detalles de la venta');
        });
    });

    // Volver a la tabla de ventas
    mainContent.on('click', '#volver-ventas', function () {
        cargarVentas();
    });

    // Eliminar una venta
    mainContent.on('click', '.eliminar-venta', function () {
        const ventaId = $(this).data('id');
        if (confirm('¿Estás seguro de eliminar esta venta?')) {
            $.ajax({
                url: `/venta/${ventaId}`,
                method: 'DELETE',
                success: function () {
                    alert('Venta eliminada correctamente.');
                    cargarVentas();
                },
                error: function (xhr) {
                    alert('Error al eliminar la venta.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    });
});
