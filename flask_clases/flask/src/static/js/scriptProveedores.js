$(document).ready(function () {
    const providerModal = $('#modal-provider-form');
    const providerForm = $('#provider-form');
    const modalTitle = $('#provider-modal-title');

    function openProviderModal(title, isEdit = false) {
        modalTitle.text(title);
        if (isEdit) {
            $('#nombre_proveedor').prop('disabled', true);
        } else {
            $('#nombre_proveedor').prop('disabled', false);
        }
        providerModal.show();
    }

    $('#proveedores').on('click', function (e) {
        e.preventDefault();
        $('#main-content').html('<p>Cargando proveedores...</p>');

        $.get('/proveedores', function (data) {
            let content = `<button id="add-provider">Agregar Proveedor</button>
                           <table>
                               <thead>
                                   <tr>
                                       <th>ID</th>
                                       <th>Nombre</th>
                                       <th>Email</th>
                                       <th>Teléfono</th>
                                       <th>Dirección</th>
                                       <th>Acciones</th>
                                   </tr>
                               </thead>
                               <tbody>`;

            data.forEach(proveedor => {
                content += `<tr>
                                <td>${proveedor.id}</td>
                                <td>${proveedor.nombre}</td>
                                <td>${proveedor.email}</td>
                                <td>${proveedor.telefono}</td>
                                <td>${proveedor.direccion}</td>
                                <td>
                                    <button class="editar-proveedor" data-id="${proveedor.id}">Editar</button>
                                    <button class="eliminar-proveedor" data-id="${proveedor.id}">Eliminar</button>
                                </td>
                            </tr>`;
            });

            content += `</tbody></table>`;
            $('#main-content').html(content);

            $('#add-provider').on('click', function () {
                providerForm[0].reset();
                $('#provider_id').val('');
                openProviderModal('Agregar Proveedor', false);
            });
        }).fail(function () {
            $('#main-content').html('<p>Error al cargar los proveedores.</p>');
        });
    });

    $('#main-content').on('click', '.editar-proveedor', function () {
        const id = $(this).data('id');
        $.get(`/proveedor/${id}`, function (data) {
            if (data) {
                $('#provider_id').val(data.id);
                $('#nombre_proveedor').val(data.nombre);
                $('#email_proveedor').val(data.email);
                $('#telefono_proveedor').val(data.telefono);
                $('#direccion_proveedor').val(data.direccion);
                openProviderModal('Editar Proveedor', true);
            } else {
                alert('Proveedor no encontrado.');
            }
        }).fail(function () {
            alert('Error al cargar los datos del proveedor.');
        });
    });

    providerForm.on('submit', function (e) {
        e.preventDefault();
        const payload = {
            nombre: $('#nombre_proveedor').val(),
            email: $('#email_proveedor').val(),
            telefono: $('#telefono_proveedor').val(),
            direccion: $('#direccion_proveedor').val()
        };
        const id = $('#provider_id').val();
        const method = id ? 'PUT' : 'POST';

        $.ajax({
            url: id ? `/proveedor/${id}` : '/proveedor',
            method: method,
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function () {
                providerModal.hide();
                alert('Proveedor actualizado o agregado correctamente.');
                $('#proveedores').click();
            },
            error: function (xhr) {
                alert('Error al actualizar o agregar proveedor.');
                console.error('Error:', xhr.responseText);
            }
        });
    });

    $('#main-content').on('click', '.eliminar-proveedor', function () {
        const id = $(this).data('id');
        if (confirm('¿Estás seguro de eliminar este proveedor?')) {
            $.ajax({
                url: `/proveedor/${id}`,
                method: 'DELETE',
                success: function () {
                    alert('Proveedor eliminado correctamente.');
                    $('#proveedores').click();
                },
                error: function (xhr) {
                    alert('Error al eliminar proveedor.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    });

    $(document).on('click', '.close', function () {
        providerModal.hide();
    });

    $(window).on('click', function (event) {
        if ($(event.target).is(providerModal)) {
            providerModal.hide();
        }
    });
});
