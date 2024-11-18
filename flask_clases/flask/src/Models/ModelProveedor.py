from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import Config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)



class ModelProveedor:


    @staticmethod
    def obtener_proveedor_por_id(id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.execute("CALL sp_obtener_proveedor_por_id('my_cursor', %s);", [id])
            cursor.execute("FETCH ALL IN my_cursor;")
            proveedor = cursor.fetchone()
            cursor.execute("COMMIT;")
            cursor.close()
            conn.close()
            return proveedor
        except Exception as e:
            print(f"Error en obtener_proveedor_por_id: {str(e)}")
            return None
        
    @staticmethod
    def obtener_proveedores():
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.execute("CALL sp_obtener_proveedores('proveedores_cursor');")
            cursor.execute("FETCH ALL IN proveedores_cursor;")
            proveedores = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            return proveedores
        except Exception as e:
            print(f"Error en obtener_proveedores: {str(e)}")
            return []

    @staticmethod
    def crear_proveedor(nombre, email, telefono, direccion):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute(
                "CALL sp_crear_proveedor(%s, %s, %s, %s);",
                [nombre, email, telefono, direccion]
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error en crear_proveedor: {str(e)}")
            return False

    @staticmethod
    def editar_proveedor(proveedor_id, nombre, email, telefono, direccion):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute(
                "CALL sp_editar_proveedor(%s, %s, %s, %s, %s);",
                [proveedor_id, nombre, email, telefono, direccion]
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error en editar_proveedor: {str(e)}")
            return False

    @staticmethod
    def eliminar_proveedor(proveedor_id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_eliminar_proveedor(%s);", [proveedor_id])
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error en eliminar_proveedor: {str(e)}")
            return False
