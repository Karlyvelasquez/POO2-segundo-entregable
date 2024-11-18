$(document).ready(function () {
    const modal = $('#modal-form');
    const modalTitle = $('#modal-title');
    const productForm = $('#product-form');

    function openModal(title) {
        modalTitle.text(title);
        cargarCategorias(); 
        modal.show();
    }

    $('.close').on('click', function () {
        modal.hide();
    });

    $(window).on('click', function (event) {
        if ($(event.target).is(modal)) {
            modal.hide();
        }
    });

    function cargarCategorias() {
        $.get('/categorias', function (data) {
            const categoriaSelect = $('#categoria_id');
            categoriaSelect.empty(); 

            data.forEach(categoria => {
                categoriaSelect.append(new Option(categoria.nombre, categoria.id));
            });
        }).fail(function () {
            alert('Error al cargar las categorías.');
        });
    }

    $('#productos').on('click', function (e) {
        e.preventDefault();
        $('#main-content').html('<p>Cargando productos...</p>');

        $.get('/productos', function (data) {
            let content = `<button id="add-product">Agregar Producto</button>
                           <table>
                               <thead>
                                   <tr>
                                       <th>ID</th>
                                       <th>Nombre</th>
                                       <th>Descripción</th>
                                       <th>Precio</th>
                                       <th>Categoría</th>
                                       <th>Stock</th>
                                       <th>Acciones</th>
                                   </tr>
                               </thead>
                               <tbody>`;

            data.forEach(producto => {
                content += `<tr>
                                <td>${producto.id}</td>
                                <td>${producto.nombre}</td>
                                <td>${producto.descripcion}</td>
                                <td>${producto.precio}</td>
                                <td>${producto.categoria_nombre}</td> <!-- Nombre de la categoría -->
                                <td>${producto.stock}</td>
                                <td>
                                    <button class="editar-producto" data-id="${producto.id}">Editar</button>
                                    <button class="eliminar-producto" data-id="${producto.id}">Eliminar</button>
                                </td>
                            </tr>`;
            });

            content += `</tbody></table>`;
            $('#main-content').html(content);
        }).fail(function () {
            $('#main-content').html('<p>Error al cargar los productos.</p>');
        });
    });

    $('#main-content').on('click', '#add-product', function () {
        productForm[0].reset();
        $('#producto_id').val('');
        openModal('Agregar Producto');
    });

    $('#main-content').on('click', '.editar-producto', function () {
        const id = $(this).data('id');
        $.get(`/producto/${id}`, function (data) {
            if (data) {
                $('#producto_id').val(data.id);
                $('#nombre').val(data.nombre);
                $('#descripcion').val(data.descripcion);
                $('#precio').val(data.precio);
                $('#categoria_id').val(data.categoria_id);
                $('#stock').val(data.stock);
                openModal('Editar Producto');
            } else {
                alert('Producto no encontrado.');
            }
        }).fail(function () {
            alert('Error al cargar los datos del producto.');
        });
    });

    productForm.on('submit', function (e) {
        e.preventDefault();
        const payload = {
            nombre: $('#nombre').val(),
            descripcion: $('#descripcion').val(),
            precio: parseFloat($('#precio').val()),
            categoria_id: parseInt($('#categoria_id').val()),
            stock: parseInt($('#stock').val())
        };

        const id = $('#producto_id').val();

        if (id) {
            $.ajax({
                url: `/producto/${id}`,
                method: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(payload),
                success: function () {
                    modal.hide();
                    $('#productos').click();
                },
                error: function (xhr) {
                    alert('Error al editar el producto.');
                }
            });
        } else {
            $.ajax({
                url: '/producto',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(payload),
                success: function () {
                    modal.hide();
                    $('#productos').click();
                },
                error: function () {
                    alert('Error al agregar el producto.');
                }
            });
        }
    });
    
    $(document).ready(function () {
        $('#cerrar-sesion').on('click', function () {
            $.post('/logout', function () {
                window.location.href = '/index'; // Redirige al índice tras cerrar sesión
            }).fail(function () {
                alert('Error al cerrar sesión.');
            });
        });
    });

    $('#main-content').on('click', '.eliminar-producto', function () {
        const id = $(this).data('id');
        if (confirm('¿Estás seguro de eliminar este producto?')) {
            $.ajax({
                url: `/producto/${id}`,
                method: 'DELETE',
                success: function () {
                    $('#productos').click();
                },
                error: function () {
                    alert('Error al eliminar el producto.');
                }
            });
        }
    });
});
