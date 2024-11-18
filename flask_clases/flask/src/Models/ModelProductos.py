from Proyecto import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import Config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

class ModelProducto:


    @staticmethod
    def obtener_productos():
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.execute("CALL sp_obtener_productos('productos_cursor');")
            cursor.execute("FETCH ALL IN productos_cursor;")
            productos = cursor.fetchall()
            cursor.execute("COMMIT;")
            cursor.close()
            conn.close()

        # Construir la respuesta con el nombre de la categoría
            return [
                {
                'id': p[0],
                'nombre': p[1],
                'descripcion': p[2],
                'precio': p[3],
                'categoria_nombre': p[4],  # Aquí se asegura que el nombre de la categoría es correcto
                'stock': p[5]
                } 
                for p in productos
            ]
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []



    @staticmethod
    def obtener_producto_por_id(producto_id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.execute("CALL sp_obtener_producto_por_id('my_cursor', %s);", [producto_id])
            cursor.execute("FETCH ALL IN my_cursor;")
            producto = cursor.fetchone()  # Devuelve solo un producto
            cursor.execute("COMMIT;")
            cursor.close()
            conn.close()
        
            if producto:
                return {
                    "id": producto[0],
                    "nombre": producto[1],
                    "descripcion": producto[2],
                    "precio": producto[3],
                    "categoria_id": producto[4],
                    "stock": producto[5]
                }
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el producto por Id: {str(e)}")
            return None





    @staticmethod
    def crear_producto(nombre, descripcion, precio, categoria_id, stock):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
        # Se corrige para asegurar transacción
            cursor.execute("CALL sp_crear_producto(%s, %s, %s, %s, %s);", [nombre, descripcion, precio, categoria_id, stock])
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error al crear producto: {str(e)}")
            conn.rollback()  # Revertir cambios si hay error
        finally:
            conn.close()




    @staticmethod
    def editar_producto(producto_id, nombre, descripcion, precio, categoria_id, stock):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_editar_producto(%s, %s, %s, %s, %s, %s);", [producto_id, nombre, descripcion, precio, categoria_id, stock])
            conn.commit()  # Finaliza la transacción
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al editar producto: {str(e)}")

    @staticmethod
    def eliminar_producto(producto_id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_eliminar_producto(%s);", [producto_id])
            conn.commit()  # Finaliza la transacción
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al eliminar producto: {str(e)}")

    @staticmethod
    def obtener_categorias():
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.execute("CALL sp_obtener_categorias('categorias_cursor');")
            cursor.execute("FETCH ALL IN categorias_cursor;")
            categorias = cursor.fetchall()
            cursor.execute("COMMIT;")
            cursor.close()
            conn.close()

            # Convierte el resultado en una lista de diccionarios
            return [{"id": cat[0], "nombre": cat[1]} for cat in categorias]
        except Exception as e:
            print(f"Error al obtener categorías: {str(e)}")
            return []
        
    @staticmethod
    def obtener_productos_por_categoria(categoria):
        query = "SELECT p.id, p.nombre, p.descripcion, p.precio, p.imagen_url, c.nombre AS categoria FROM productos p JOIN categorias c ON p.categoria_id = c.id WHERE c.nombre = %s"
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute(query, (categoria,))
        return cursor.fetchall()


