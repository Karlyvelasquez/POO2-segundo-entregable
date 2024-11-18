$(document).ready(function () {
    const categoryModal = $('#modal-category-form');
    const categoryForm = $('#category-form');
    const modalTitle = $('#category-modal-title');

    // Abre el modal para agregar o editar categorías
    function openCategoryModal(title) {
        modalTitle.text(title);
        categoryModal.show();
    }

    // Cerrar modal al hacer clic en la X
    $(document).on('click', '.close', function () {
        categoryModal.hide();
    });

    // Cerrar modal si se hace clic fuera del contenido
    $(window).on('click', function (event) {
        if ($(event.target).is(categoryModal)) {
            categoryModal.hide();
        }
    });

    // Cargar categorías al hacer clic en el menú
    $('#categorias').on('click', function (e) {
        e.preventDefault();
        $('#main-content').html('<p>Cargando categorías...</p>');

        $.get('/categorias', function (data) {
            if (data.error) {
                $('#main-content').html('<p>Error al cargar las categorías.</p>');
                console.error(data.error);
                return;
            }

            let content = `<button id="add-category">Agregar Categoría</button>
                           <table>
                               <thead>
                                   <tr>
                                       <th>ID</th>
                                       <th>Nombre</th>
                                       <th>Acciones</th>
                                   </tr>
                               </thead>
                               <tbody>`;

            data.forEach(categoria => {
                content += `<tr>
                                <td>${categoria.id}</td>
                                <td>${categoria.nombre}</td>
                                <td>
                                    <button class="editar-categoria" data-id="${categoria.id}">Editar</button>
                                    <button class="eliminar-categoria" data-id="${categoria.id}">Eliminar</button>
                                </td>
                            </tr>`;
            });

            content += `</tbody></table>`;
            $('#main-content').html(content);

            // Evento para agregar nueva categoría
            $('#add-category').on('click', function () {
                categoryForm[0].reset();
                $('#category_id').val('');
                openCategoryModal('Agregar Categoría');
            });
        }).fail(function () {
            $('#main-content').html('<p>Error al cargar las categorías.</p>');
            console.error('Error al cargar categorías');
        });
    });

    // Editar categoría
    $('#main-content').on('click', '.editar-categoria', function () {
        const id = $(this).data('id');
        $.get(`/categoria/${id}`, function (data) {
            if (data && !data.error) {
                $('#category_id').val(data.id);
                $('#nombre_categoria').val(data.nombre);
                openCategoryModal('Editar Categoría');
            } else {
                alert('Categoría no encontrada.');
            }
        }).fail(function () {
            alert('Error al cargar los datos de la categoría.');
        });
    });

    // Guardar categoría
    categoryForm.on('submit', function (e) {
        e.preventDefault();

        const payload = {
            nombre: $('#nombre_categoria').val()
        };

        const id = $('#category_id').val();
        const method = id ? 'PUT' : 'POST';

        $.ajax({
            url: id ? `/categoria/${id}` : '/categoria',
            method: method,
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function () {
                categoryModal.hide();
                alert('Categoría actualizada o agregada correctamente.');
                $('#categorias').click();
            },
            error: function (xhr) {
                alert('Error al actualizar o agregar categoría.');
                console.error('Error:', xhr.responseText);
            }
        });
    });

    // Eliminar categoría
    $('#main-content').on('click', '.eliminar-categoria', function () {
        const id = $(this).data('id');
        if (confirm('¿Estás seguro de eliminar esta categoría?')) {
            $.ajax({
                url: `/categoria/${id}`,
                method: 'DELETE',
                success: function () {
                    alert('Categoría eliminada correctamente.');
                    $('#categorias').click();
                },
                error: function (xhr) {
                    alert('Error al eliminar categoría.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    });
});
