$(document).ready(function () {
    const clientModal = $('#modal-client-form');
    const clientForm = $('#client-form');
    const modalTitle = $('#client-modal-title');

    function openClientModal(title, isEdit = false) {
        modalTitle.text(title);
        clientModal.show();
    }

    // Cerrar modal al hacer clic en la X
    $(document).on('click', '.close', function () {
        clientModal.hide();
    });

    // Cerrar modal si se hace clic fuera del contenido
    $(window).on('click', function (event) {
        if ($(event.target).is(clientModal)) {
            clientModal.hide();
        }
    });

    // Cargar clientes
    $('#clientes').on('click', function (e) {
        e.preventDefault();
        $('#main-content').html('<p>Cargando clientes...</p>');

        $.get('/clientes', function (data) {
            if (data.error) {
                $('#main-content').html('<p>Error al cargar los clientes.</p>');
                console.error(data.error);
                return;
            }

            let content = `<button id="add-client">Agregar Cliente</button>
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

            data.forEach(cliente => {
                content += `<tr>
                                <td>${cliente.id}</td>
                                <td>${cliente.nombre}</td>
                                <td>${cliente.email}</td>
                                <td>${cliente.telefono}</td>
                                <td>${cliente.direccion}</td>
                                <td>
                                    <button class="editar-cliente" data-id="${cliente.id}">Editar</button>
                                    <button class="eliminar-cliente" data-id="${cliente.id}">Eliminar</button>
                                </td>
                            </tr>`;
            });

            content += `</tbody></table>`;
            $('#main-content').html(content);

            // Evento para agregar un nuevo cliente
            $('#add-client').on('click', function () {
                clientForm[0].reset();
                $('#client_id').val('');
                openClientModal('Agregar Cliente', false);
            });
        }).fail(function () {
            $('#main-content').html('<p>Error al cargar los clientes.</p>');
            console.error('Error al cargar clientes');
        });
    });

    // Editar cliente
    $('#main-content').on('click', '.editar-cliente', function () {
        const id = $(this).data('id');
        $.get(`/cliente/${id}`, function (data) {
            if (data) {
                $('#client_id').val(data.id);
                $('#nombre_cliente').val(data.nombre);
                $('#email_cliente').val(data.email);
                $('#telefono_cliente').val(data.telefono);
                $('#direccion_cliente').val(data.direccion);
                openClientModal('Editar Cliente', true);
            } else {
                alert('Cliente no encontrado.');
            }
        }).fail(function () {
            alert('Error al cargar los datos del cliente.');
        });
    });

    // Guardar cliente (Agregar o Editar)
    clientForm.on('submit', function (e) {
        e.preventDefault();

        const payload = {
            nombre: $('#nombre_cliente').val(),
            email: $('#email_cliente').val(),
            telefono: $('#telefono_cliente').val(),
            direccion: $('#direccion_cliente').val()
        };

        const id = $('#client_id').val();
        const method = id ? 'PUT' : 'POST';

        $.ajax({
            url: id ? `/cliente/${id}` : '/cliente',
            method: method,
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function () {
                clientModal.hide();
                alert('Cliente actualizado o agregado correctamente.');
                $('#clientes').click();
            },
            error: function (xhr) {
                alert('Error al actualizar o agregar cliente.');
                console.error('Error:', xhr.responseText);
            }
        });
    });

    // Eliminar cliente
    $('#main-content').on('click', '.eliminar-cliente', function () {
        const id = $(this).data('id');
        if (confirm('¿Estás seguro de eliminar este cliente?')) {
            $.ajax({
                url: `/cliente/${id}`,
                method: 'DELETE',
                success: function () {
                    alert('Cliente eliminado correctamente.');
                    $('#clientes').click(); // Recargar lista de clientes
                },
                error: function (xhr) {
                    alert('Error al eliminar cliente.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    });
});
