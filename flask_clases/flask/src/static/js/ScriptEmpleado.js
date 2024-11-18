$(document).ready(function () {
    const employeeModal = $('#modal-employee-form');
    const employeeForm = $('#employee-form');
    const modalTitle = $('#employee-modal-title');

    function openEmployeeModal(title, isEdit = false) {
        modalTitle.text(title);

        if (isEdit) {
            $('#nombre_empleado').prop('disabled', true); // Deshabilitar nombre al editar
            $('#email_empleado').prop('disabled', false); // Habilitar email al editar
        } else {
            $('#nombre_empleado').prop('disabled', false); // Habilitar nombre al agregar
            $('#email_empleado').prop('disabled', false); // Habilitar email al agregar
        }

        cargarRoles();
        employeeModal.show();
    }

    // Cargar roles para el select
    function cargarRoles() {
        $.get('/roles', function (data) {
            const roleSelect = $('#rol_id');
            roleSelect.empty(); // Limpiar opciones previas

            data.forEach(rol => {
                roleSelect.append(new Option(rol.nombre, rol.id));
            });
        }).fail(function () {
            alert('Error al cargar los roles.');
        });
    }

    // Cargar empleados
    $('#empleados').on('click', function (e) {
        e.preventDefault();
        $('#main-content').html('<p>Cargando empleados...</p>');

        $.get('/empleados', function (data) {
            if (data.error) {
                $('#main-content').html('<p>Error al cargar los empleados.</p>');
                console.error(data.error);
                return;
            }

            let content = `<button id="add-employee">Agregar Empleado</button>
                           <table>
                               <thead>
                                   <tr>
                                       <th>ID</th>
                                       <th>Nombre</th>
                                       <th>Email</th>
                                       <th>Rol</th>
                                       <th>Contraseña</th>
                                       <th>Acciones</th>
                                   </tr>
                               </thead>
                               <tbody>`;

            data.forEach(usuario => {
                content += `<tr>
                                <td>${usuario.id}</td>
                                <td>${usuario.nombre}</td>
                                <td>${usuario.email}</td>
                                <td>${usuario.rol_nombre}</td>
                                <td>${usuario.contrasena || '********'}</td> <!-- Ocultar contraseña real -->
                                <td>
                                    <button class="editar-empleado" data-id="${usuario.id}">Editar</button>
                                    <button class="eliminar-empleado" data-id="${usuario.id}">Eliminar</button>
                                </td>
                            </tr>`;
            });

            content += `</tbody></table>`;
            $('#main-content').html(content);

            // Evento para agregar un nuevo empleado
            $('#add-employee').on('click', function () {
                employeeForm[0].reset();
                $('#employee_id').val('');
                openEmployeeModal('Agregar Empleado', false);
            });
        }).fail(function () {
            $('#main-content').html('<p>Error al cargar los empleados.</p>');
            console.error('Error al cargar empleados');
        });
    });

    // Editar empleado
    $('#main-content').on('click', '.editar-empleado', function () {
        const id = $(this).data('id');
        $.get(`/empleado/${id}`, function (data) {
            if (data) {
                $('#employee_id').val(data.id);
                $('#nombre_empleado').val(data.nombre);
                $('#email_empleado').val(data.email);
                $('#rol_id').val(data.rol_id);
                openEmployeeModal('Editar Empleado', true);
            } else {
                alert('Empleado no encontrado.');
            }
        }).fail(function () {
            alert('Error al cargar los datos del empleado.');
        });
    });

    // Guardar empleado (Agregar o Editar)
    employeeForm.on('submit', function (e) {
        e.preventDefault();

        const payload = {
            rol_id: $('#rol_id').val(),
            nueva_contrasena: $('#nueva_contrasena').val(),
            email: $('#email_empleado').val(),
            nombre: $('#nombre_empleado').val()
        };

        const id = $('#employee_id').val();
        const method = id ? 'PUT' : 'POST';

        $.ajax({
            url: id ? `/empleado/${id}` : '/empleado',
            method: method,
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function () {
                employeeModal.hide();
                alert('Empleado actualizado o agregado correctamente.');
                $('#empleados').click();
            },
            error: function (xhr) {
                alert('Error al actualizar o agregar empleado.');
                console.error('Error:', xhr.responseText);
            }
        });
    });

    // Eliminar empleado
    $('#main-content').on('click', '.eliminar-empleado', function () {
        const id = $(this).data('id');
        if (confirm('¿Estás seguro de eliminar este empleado?')) {
            $.ajax({
                url: `/empleado/${id}`,
                method: 'DELETE',
                success: function () {
                    alert('Empleado eliminado correctamente.');
                    $('#empleados').click(); // Recarga la lista de empleados
                },
                error: function (xhr) {
                    alert('Error al eliminar empleado.');
                    console.error('Error:', xhr.responseText);
                }
            });
        }
    });

    // Cerrar modal al hacer clic en la X
    $(document).on('click', '.close', function () {
        employeeModal.hide();
    });

    // Cerrar modal si se hace clic fuera del contenido
    $(window).on('click', function (event) {
        if ($(event.target).is(employeeModal)) {
            employeeModal.hide();
        }
    });
});
