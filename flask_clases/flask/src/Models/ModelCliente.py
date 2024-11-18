from sqlalchemy import create_engine
from config import Config
from flask import jsonify

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

class ModelCliente:

    @staticmethod
    def obtener_clientes():
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN;")  # Inicia la transacción
            cursor.execute("CALL sp_obtener_clientes('clientes_cursor');")  # Llama al procedimiento
            cursor.execute("FETCH ALL IN clientes_cursor;")  # Recupera los datos del cursor
            clientes = cursor.fetchall()
            cursor.execute("COMMIT;")  # Finaliza la transacción
            cursor.close()
            conn.close()
            return clientes
        except Exception as e:
            print(f"Error en obtener_clientes: {str(e)}")
            conn.rollback()  # Asegúrate de hacer rollback si algo falla
            raise



    @staticmethod
    def obtener_cliente_por_id(cliente_id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.execute("CALL sp_obtener_cliente_por_id('cliente_cursor', %s);", [cliente_id])
            cursor.execute("FETCH ALL IN cliente_cursor;")
            cliente = cursor.fetchone()
            cursor.execute("COMMIT;")
            cursor.close()
            conn.close()
            return cliente
        except Exception as e:
            print(f"Error en obtener_cliente_por_id: {str(e)}")
            return None

    @staticmethod
    def crear_cliente(nombre, email, telefono, direccion):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_crear_cliente(%s, %s, %s, %s);", [nombre, email, telefono, direccion])
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error en crear_cliente: {str(e)}")

    @staticmethod
    def editar_cliente(id, nombre, email, telefono, direccion):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_editar_cliente(%s, %s, %s, %s, %s);", 
                           (id, nombre, email, telefono, direccion))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error en editar_cliente: {str(e)}")
            raise


    @staticmethod
    def eliminar_cliente(cliente_id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_eliminar_cliente(%s);", [cliente_id])
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error en eliminar_cliente: {str(e)}")
