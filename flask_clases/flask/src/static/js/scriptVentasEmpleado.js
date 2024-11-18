$(document).ready(function () {
    const ventaModal = $('#modal-sale-form');
    const ventaForm = $('#sale-form');
    const modalTitle = $('#sale-modal-title');
    const productosContainer = $('#productos-container');
    const totalInput = $('#total');

    let productosData = [];

    // Función para abrir el modal
    function openVentaModal(title) {
        modalTitle.text(title);
        cargarClientes();
        cargarProductos();
        ventaModal.show();
        resetProductosContainer();
        agregarProductoRow(); // Añadir una fila de producto por defecto
    }

    // Cerrar el modal
    $(document).on('click', '.close', function () {
        ventaModal.hide();
    });

    $(window).on('click', function (event) {
        if ($(event.target).is(ventaModal)) {
            ventaModal.hide();
        }
    });

    // Cargar clientes dinámicamente
    function cargarClientes() {
        $.get('/clientes', function (data) {
            const clienteSelect = $('#cliente_id');
            clienteSelect.empty();
            clienteSelect.append(new Option('Seleccionar cliente', ''));
            data.forEach(cliente => {
                clienteSelect.append(new Option(cliente.nombre, cliente.id));
            });
        }).fail(function () {
            alert('Error al cargar clientes.');
        });
    }

    // Cargar productos dinámicamente
    function cargarProductos() {
        $.get('/productos', function (data) {
            productosData = data;
            $('.producto_id').each(function () {
                cargarOpcionesProductos($(this));
            });
        }).fail(function () {
            alert('Error al cargar productos.');
        });
    }

    function cargarOpcionesProductos(selectElement) {
        selectElement.empty();
        selectElement.append(new Option('Seleccionar producto', ''));
        productosData.forEach(producto => {
            selectElement.append(new Option(producto.nombre, producto.id)).data('precio', producto.precio);
        });
    }

    function resetProductosContainer() {
        productosContainer.empty();
    }

    function actualizarTotal() {
        let total = 0;
        $('.producto-item').each(function () {
            const cantidad = parseFloat($(this).find('.cantidad').val()) || 0;
            const productoId = $(this).find('.producto_id').val();
            const producto = productosData.find(p => p.id == productoId);
            if (producto) {
                total += cantidad * producto.precio;
            }
        });
        totalInput.val(total.toFixed(2));
    }

    // Agregar fila para nuevo producto
    function agregarProductoRow() {
        const nuevaFila = `
            <div class="producto-item">
                <label for="producto_id">Producto:</label>
                <select class="producto_id" required></select>
                <label for="cantidad">Cantidad:</label>
                <input type="number" class="cantidad" min="1" required>
                <button type="button" class="eliminar-producto">Eliminar</button>
            </div>`;
        productosContainer.append(nuevaFila);

        const nuevoSelect = productosContainer.find('.producto_id').last();
        cargarOpcionesProductos(nuevoSelect);

        nuevoSelect.on('change', actualizarTotal);
        productosContainer.find('.cantidad').last().on('input', actualizarTotal);
    }

    productosContainer.on('click', '.eliminar-producto', function () {
        $(this).closest('.producto-item').remove();
        actualizarTotal();
    });

    $('#add-product').on('click', function () {
        agregarProductoRow();
    });

    // Cargar ventas
    $('#ventas').on('click', function (e) {
        e.preventDefault();
        $('#main-content').html('<p>Cargando ventas...</p>');

        $.get('/ventas', function (data) {
            let content = `<button id="add-venta">Agregar Venta</button>
                           <table>
                               <thead>
                                   <tr>
                                       <th>ID</th>
                                       <th>Fecha</th>
                                       <th>Cliente</th>
                                       <th>Usuario</th>
                                       <th>Total</th>
                                       <th>Acciones</th>
                                   </tr>
                               </thead>
                               <tbody>`;

            data.forEach(venta => {
                content += `<tr>
                                <td>${venta.id}</td>
                                <td>${venta.fecha}</td>
                                <td>${venta.cliente}</td>
                                <td>${venta.usuario}</td>
                                <td>${venta.total}</td>
                                <td>
                                    <button class="ver-detalles-venta" data-id="${venta.id}">Ver Detalles</button>
                                </td>
                            </tr>`;
            });

            content += `</tbody></table>`;
            $('#main-content').html(content);

            $('#add-venta').on('click', function () {
                ventaForm[0].reset();
                openVentaModal('Nueva Venta');
            });
        }).fail(function () {
            $('#main-content').html('<p>Error al cargar las ventas.</p>');
        });
    });

    // Guardar venta
    ventaForm.on('submit', function (e) {
        e.preventDefault();
    
        const detalles = [];
        $('.producto-item').each(function () {
            const productoId = $(this).find('.producto_id').val();
            const cantidad = $(this).find('.cantidad').val();
            const producto = productosData.find(p => p.id == productoId);
    
            if (producto) {
                detalles.push({ producto_id: productoId, cantidad: cantidad, precio: producto.precio });
            }
        });
    
        const payload = {
            cliente_id: $('#cliente_id').val(),
            usuario_id: $('#usuario_id').val(),
            detalles: detalles
        };
    
        console.log('Payload:', payload); // Verifica los datos enviados.
    
        $.ajax({
            url: '/venta',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function () {
                ventaModal.hide();
                alert('Venta registrada correctamente.');
                $('#ventas').click();
            },
            error: function (xhr) {
                alert(`Error al registrar la venta: ${xhr.responseText}`);
                console.error('Detalles del error:', xhr.responseText);
            }
        });
    });
    
    

    // Cargar detalles de venta
    $(document).on('click', '.ver-detalles-venta', function () {
        const ventaId = $(this).data('id');
        $.get(`/venta/${ventaId}/detalles`, function (data) {
            let content = '<h3>Detalles de Venta</h3><table>';
            data.forEach(detalle => {
                content += `<tr>
                                <td>${detalle.producto}</td>
                                <td>${detalle.cantidad}</td>
                                <td>${detalle.precio}</td>
                            </tr>`;
            });
            content += '</table>';
            $('#main-content').html(content);
        }).fail(function () {
            alert('Error al cargar los detalles de la venta.');
        });
    });
});



