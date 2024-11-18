from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, session
from config import Config
import re
from flask_sqlalchemy import SQLAlchemy
from Models.ModelUsuarios import modeluser
from Models.entities.Usuarios import usuarios
from Models.ModelUsuarios import Usuario
from Models import ModelProductos
from Models import ModelEmpleado
from Models import ModelProveedor
from Models import ModelCliente
from Models import ModelVentas
from Models import ModelCategorias
import psycopg2
from sqlalchemy import create_engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/venta', methods=['POST'])
def crear_venta():
    try:
        data = request.get_json()

        # Log para verificar qué datos se están recibiendo
        print(f"Payload recibido: {data}")

        cliente_id = data.get('cliente_id')
        usuario_id = data.get('usuario_id')
        detalles = data.get('detalles')  # Lista de detalles de venta [{producto_id, cantidad, precio}, ...]

        # Validación de campos
        if not detalles or not cliente_id or not usuario_id:
            return jsonify({"error": "Datos incompletos"}), 400

        venta_id = ModelVentas.ModelVentas.crear_venta_con_detalles(cliente_id, usuario_id, detalles)
        return jsonify({"message": "Venta creada", "venta_id": venta_id}), 201
    except Exception as e:
        print(f"Error al crear venta: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500




@app.route('/productos', methods=['GET'])
def mostrar_productos():
    try:
        productos = ModelProductos.ModelProducto.obtener_productos()
        return jsonify(productos)
    except Exception as e:
        print(f"Error al obtener productos: {str(e)}")
        return jsonify({"error": "Error al obtener productos"}), 500


@app.route('/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = ModelProductos.ModelProducto.obtener_producto_por_id(id)
    if producto:
        return jsonify(producto)
    return jsonify({"message": "Producto no encontrado"}), 404

@app.route('/producto', methods=['POST'])
def crear_producto():
    try:
        data = request.json
        required_fields = ['nombre', 'descripcion', 'precio', 'categoria_id', 'stock']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        
        ModelProductos.ModelProducto.crear_producto(
            data['nombre'], data['descripcion'], data['precio'],
            data['categoria_id'], data['stock']
        )
        return jsonify({"message": "Producto creado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/producto/<int:id>', methods=['PUT'])
def editar_producto(id):
    try:
        data = request.json
        required_fields = ['nombre', 'descripcion', 'precio', 'categoria_id', 'stock']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        
        ModelProductos.ModelProducto.editar_producto(
            id, data['nombre'], data['descripcion'], data['precio'],
            data['categoria_id'], data['stock']
        )
        return jsonify({"message": "Producto actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/producto/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        ModelProductos.ModelProducto.eliminar_producto(id)
        return jsonify({"message": "Producto eliminado"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/categorias', methods=['GET'])
def obtener_categorias():
    try:
        categorias = ModelProductos.ModelProducto.obtener_categorias()
        return jsonify(categorias)
    except Exception as e:
        print(f"Error al obtener categorías: {str(e)}")
        return jsonify({"error": "No se pudieron obtener las categorías"}), 500

@app.route('/')
def index():
    return redirect(url_for('indexito'))

@app.route('/gerente_dashboard')
def gerente_dashboard():
    return render_template("gerente_dashboard.html")

@app.route('/empleado_dashboard')
def empleado_dashboard():
    return render_template("empleado_dashboard.html")
@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.route('/index')
def indexito():
    return render_template("Index.html")


@app.route('/Hogar')
def Hogar():
    producticos = ModelProductos.ModelProducto.obtener_productos()
    return render_template("herramientas_hogar.html", productos = producticos)

@app.route('/Herramientas')
def Herramientas():
    productos = ModelProductos.ModelProducto.obtener_productos()
    return render_template("herramientas.html",productos=productos)


@app.route('/Pinturas')
def Pinturas():
    productos = ModelProductos.ModelProducto.obtener_productos()
    return render_template("pinturas.html", productos = productos)

@app.route('/Iluminacion')
def Iluminacion():
    productos = ModelProductos.ModelProducto.obtener_productos()  
    return render_template('iluminacion.html', productos=productos)
    



from flask import session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        usuario_autenticado = Usuario.login(db, email, contraseña)
        
        if usuario_autenticado:
            session['usuario_id'] = usuario_autenticado.id
            session['usuario_nombre'] = usuario_autenticado.nombre  # Guarda el nombre
            session['rol_id'] = usuario_autenticado.rol_id
            
            if usuario_autenticado.rol_id == 1:
                return redirect(url_for('gerente_dashboard'))
            elif usuario_autenticado.rol_id == 2:
                return redirect(url_for('empleado_dashboard'))
            else:
                flash("Rol desconocido.", "danger")
        else:
            flash("Email o contraseña incorrectos.", "danger")
    
    return render_template("auth/login.html")


@app.route('/hogar')
def hogar():
    productos_hogar = ModelProductos.ModelProducto.obtener_productos_por_categoria('Hogar')
    return render_template('herramientas_hogar.html', productos=productos_hogar)


    


@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']

        # Verificar si la cédula ya existe en la base de datos
        usuario_existente = modeluser.buscar_usuario_por_cedula(db, cedula)
        
        if usuario_existente:
            # Si la cédula ya existe, mostrar un mensaje de error
            return render_template("Registro.html", error="La cédula ya está registrada.")

        # Si no existe, proceder a registrar el nuevo usuario
        nuevo_usuario = usuarios(cedula, nombre, email, contraseña)
        modeluser.registrar(db, nuevo_usuario)
        return redirect(url_for('login'))

    return render_template("Registro.html")

# empleado --------------------------
@app.route('/empleados', methods=['GET'])
def obtener_empleados():
    try:
        empleados = ModelEmpleado.ModelEmpleado.obtener_empleados()
        return jsonify(empleados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/empleado/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    try:
        if ModelEmpleado.ModelEmpleado.eliminar_empleado(id):
            return jsonify({"message": "Empleado eliminado correctamente."}), 200
        else:
            return jsonify({"error": "No se pudo eliminar el empleado."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    

@app.route('/empleado/<int:id>', methods=['GET'])
def obtener_empleado(id):
    try:
        empleado = ModelEmpleado.ModelEmpleado.obtener_empleado_por_id(id)
        return jsonify(empleado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/empleado/<int:id>', methods=['PUT'])
def editar_empleado(id):
    try:
        data = request.get_json()
        email = data.get('email')
        rol_id = data.get('rol_id')
        nueva_contrasena = data.get('nueva_contrasena')

        # Validación básica
        if not email or not rol_id or not nueva_contrasena:
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Llamada al modelo para actualizar empleado
        if ModelEmpleado.ModelEmpleado.editar_empleado(id, email, rol_id, nueva_contrasena):
            return jsonify({"message": "Empleado actualizado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar el empleado"}), 500
    except Exception as e:
        print(f"Error en editar_empleado: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/empleado', methods=['POST'])
def agregar_empleado():
    try:
        data = request.get_json()
        nombre = data['nombre']
        email = data['email']
        rol_id = data['rol_id']
        contrasena = data['nueva_contrasena']

        ModelEmpleado.ModelEmpleado.agregar_empleado(nombre, email, rol_id, contrasena)
        return jsonify({"message": "Empleado agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": f"No se pudo agregar el empleado: {str(e)}"}), 500


@app.route('/roles', methods=['GET'])
def obtener_roles():
    try:
        roles = ModelEmpleado.ModelEmpleado.obtener_roles()
        return jsonify(roles)
    except Exception as e:
        return jsonify({"error": str(e)})




# empleado --------------------------

# Proveedores ------------------------------

@app.route('/proveedor/<int:id>', methods=['GET'])
def obtener_proveedor(id):
    try:
        proveedor = ModelProveedor.ModelProveedor.obtener_proveedor_por_id(id)  # Llama al método del modelo
        if proveedor:
            return jsonify({
                'id': proveedor[0],
                'nombre': proveedor[1],
                'email': proveedor[2],
                'telefono': proveedor[3],
                'direccion': proveedor[4]
            })
        else:
            return jsonify({'error': 'Proveedor no encontrado'}), 404
    except Exception as e:
        print(f"Error en obtener_proveedor: {str(e)}")
        return jsonify({'error': 'Error al obtener el proveedor'}), 500
    
@app.route('/proveedores', methods=['GET'])
def obtener_proveedores():
    try:
        proveedores = ModelProveedor.ModelProveedor.obtener_proveedores()
        return jsonify([{
            "id": p[0],
            "nombre": p[1],
            "email": p[2],
            "telefono": p[3],
            "direccion": p[4]
        } for p in proveedores])
    except Exception as e:
        print(f"Error en obtener_proveedores: {str(e)}")
        return jsonify({"error": "Error al obtener proveedores"}), 500

@app.route('/proveedor', methods=['POST'])
def crear_proveedor():
    try:
        data = request.get_json()
        if ModelProveedor.ModelProveedor.crear_proveedor(data['nombre'], data['email'], data['telefono'], data['direccion']):
            return jsonify({"message": "Proveedor creado correctamente"}), 201
        else:
            return jsonify({"error": "No se pudo crear el proveedor"}), 500
    except Exception as e:
        print(f"Error en crear_proveedor: {str(e)}")
        return jsonify({"error": "Error en el servidor"}), 500

@app.route('/proveedor/<int:id>', methods=['PUT'])
def editar_proveedor(id):
    try:
        data = request.get_json()
        if ModelProveedor.ModelProveedor.editar_proveedor(id, data['nombre'], data['email'], data['telefono'], data['direccion']):
            return jsonify({"message": "Proveedor actualizado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar el proveedor"}), 500
    except Exception as e:
        print(f"Error en editar_proveedor: {str(e)}")
        return jsonify({"error": "Error en el servidor"}), 500

@app.route('/proveedor/<int:id>', methods=['DELETE'])
def eliminar_proveedor(id):
    try:
        if ModelProveedor.ModelProveedor.eliminar_proveedor(id):
            return jsonify({"message": "Proveedor eliminado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo eliminar el proveedor"}), 500
    except Exception as e:
        print(f"Error en eliminar_proveedor: {str(e)}")
        return jsonify({"error": "Error en el servidor"}), 500


# Proveedores -------------------------



# Clientes ---------------

@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    try:
        clientes = ModelCliente.ModelCliente.obtener_clientes()
        return jsonify([{
            'id': cliente[0],
            'nombre': cliente[1],
            'email': cliente[2],
            'telefono': cliente[3],
            'direccion': cliente[4]
        } for cliente in clientes])
    except Exception as e:
        # Imprimir el error en la consola para depurar
        print(f"Error en obtener_clientes: {str(e)}")
        return jsonify({'error': f'Error al obtener los clientes: {str(e)}'}), 500


@app.route('/cliente/<int:id>', methods=['GET'])
def obtener_cliente(id):
    try:
        cliente = ModelCliente.ModelCliente.obtener_cliente_por_id(id)
        if cliente:
            return jsonify({
                'id': cliente[0],
                'nombre': cliente[1],
                'email': cliente[2],
                'telefono': cliente[3],
                'direccion': cliente[4]
            })
        return jsonify({'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        print(f"Error en obtener_cliente: {str(e)}")
        return jsonify({'error': 'Error al obtener el cliente'}), 500


@app.route('/cliente', methods=['POST'])
def crear_cliente():
    try:
        data = request.json
        ModelCliente.ModelCliente.crear_cliente(
            data['nombre'], data['email'], data['telefono'], data['direccion']
        )
        return '', 201
    except Exception as e:
        return jsonify({'error': 'Error al crear cliente'}), 500

@app.route('/cliente/<int:id>', methods=['PUT'])
def editar_cliente(id):
    try:
        data = request.json
        ModelCliente.ModelCliente.editar_cliente(
            id, data['nombre'], data['email'], data['telefono'], data['direccion']
        )
        return jsonify({"message": "Cliente actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({'error': f"Error al editar cliente: {str(e)}"}), 500

@app.route('/cliente/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    try:
        ModelCliente.ModelCliente.eliminar_cliente(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': 'Error al eliminar cliente'}), 500


# Clientes --------------

# Ventas ------------

@app.route('/ventas', methods=['GET'])
def obtener_ventas():
    try:
        ventas = ModelVentas.ModelVentas.obtener_ventas()
        if not ventas:
            return jsonify({"error": "No se pudieron cargar las ventas."}), 500
        return jsonify(ventas), 200
    except Exception as e:
        print(f"Error en obtener_ventas: {str(e)}")
        return jsonify({"error": "Error al cargar las ventas."}), 500


@app.route('/venta/<int:venta_id>/detalles', methods=['GET'])
def obtener_detalles_venta(venta_id):
    try:
        detalles = ModelVentas.ModelVentas.obtener_detalles_venta(venta_id)
        return jsonify([
            {
                "id": d[0],
                "venta_id": d[1],
                "producto": d[2],
                "cantidad": d[3],
                "precio": d[4]
            } for d in detalles
        ])
    except Exception as e:
        print(f"Error en obtener_detalles_venta: {str(e)}")
        return jsonify({"error": "Error al cargar los detalles de la venta"}), 500


@app.route('/venta/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    try:
        if ModelVentas.ModelVentas.eliminar_venta(id):
            return jsonify({"message": "Venta eliminada correctamente"}), 200
        return jsonify({"error": "No se pudo eliminar la venta"}), 500
    except Exception as e:
        return jsonify({'error': 'Error al eliminar venta'}), 500

# Ventas ------------

# Categoerias -----------------------------

@app.route('/categoria/<int:id>', methods=['GET'])
def obtener_categoria(id):
    try:
        categoria = ModelCategorias.ModelCategorias.obtener_categoria_por_id(id)
        if categoria:
            return jsonify({
                'id': categoria[0],
                'nombre': categoria[1]
            })
        else:
            return jsonify({'error': 'Categoría no encontrada'}), 404
    except Exception as e:
        print(f"Error en obtener_categoria: {str(e)}")
        return jsonify({'error': 'Error al obtener la categoría'}), 500
    
@app.route('/categorias', methods=['GET'])
def obtener_categoriass():
    try:
        categorias = ModelCategorias.ModelCategorias.obtener_categorias()
        return jsonify(categorias), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener las categorías"}), 500

@app.route('/categoria', methods=['POST'])
def crear_categoria():
    try:
        data = request.json
        ModelCategorias.ModelCategorias.insertar_categoria(data['nombre'])
        return jsonify({"message": "Categoría creada"}), 201
    except Exception as e:
        return jsonify({"error": "Error al crear la categoría"}), 500

@app.route('/categoria/<int:id>', methods=['PUT'])
def actualizar_categoria(id):
    try:
        data = request.json
        ModelCategorias.ModelCategorias.actualizar_categoria(id, data['nombre'])
        return jsonify({"message": "Categoría actualizada"}), 200
    except Exception as e:
        return jsonify({"error": "Error al actualizar la categoría"}), 500

@app.route('/categoria/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    try:
        ModelCategorias.ModelCategorias.eliminar_categoria(id)
        return jsonify({"message": "Categoría eliminada"}), 200
    except Exception as e:
        return jsonify({"error": "Error al eliminar la categoría"}), 500



# Categorias ------------------------

@app.route('/cambiar_contraseña', methods=['POST'])
def cambiar_contraseña():
    email = request.form['email']
    nueva_contraseña = request.form['nueva_contraseña']
    
    try:
        # Llamamos al método para cambiar la contraseña
        Usuario.cambiar_contraseña(db, email, nueva_contraseña)
        flash("Contraseña cambiada exitosamente", "success")
        return redirect(url_for('login'))  # Redirigir al login

    except Exception as e:
        flash(f"Error al cambiar la contraseña: {str(e)}", "danger")
        return redirect(url_for('cambiar_contraseña'))  # Redirigir a la misma página de cambio


@app.route('/actualizarInfo', methods=['GET', 'POST'])
def actualizar_informacion():
    if request.method == 'POST':
        cedula = request.form['cedula']
        email = request.form['email']
        nueva_contraseña = request.form['nueva_contraseña']
        
        # Validar que la nueva contraseña cumple los requisitos
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', nueva_contraseña):
            flash("La contraseña debe tener al menos 8 caracteres y contener letras y números", "error")
            return redirect(url_for('actualizar_informacion'))

        # Buscar usuario por cédula
        usuario = modeluser.buscar_usuario_por_cedula(db, cedula)
        if usuario is None:
            flash("No se encontró un usuario con esa cédula.", "error")
            return redirect(url_for('actualizar_informacion'))

        # Actualizar el email y la contraseña del usuario
        usuario.email = email
        usuario.contraseña = nueva_contraseña
        
        try:
            # Guardar los cambios en la base de datos
            db.session.commit()
            flash("Cambio de email y contraseña exitoso, ingresa con tus datos", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Si hay un error, revertir cambios
            flash("Error al actualizar los datos: " + str(e), "error")
            return redirect(url_for('actualizar_informacion'))
    
    return render_template("actualizarInfo.html")

@app.route('/logout', methods=['POST'])
def logout():
    # Lógica para cerrar sesión (por ejemplo, limpiar cookies o sesiones)
    session.clear()  # Limpia la sesión actual
    return '', 200  # Respuesta exitosa



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)