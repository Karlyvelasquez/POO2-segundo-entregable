from sqlalchemy import create_engine
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

class ModelCategorias:
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
            return [{"id": c[0], "nombre": c[1]} for c in categorias]
        except Exception as e:
            print(f"Error en obtener_categorias: {str(e)}")
            return []
        
    @staticmethod
    def obtener_categoria_por_id(id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("BEGIN;")
            cursor.execute("CALL sp_obtener_categoria('categoria_cursor', %s);", (id,))
            cursor.execute("FETCH ALL IN categoria_cursor;")
            categoria = cursor.fetchone()
            cursor.execute("COMMIT;")
            cursor.close()
            conn.close()
            return categoria
        except Exception as e:
            print(f"Error en obtener_categoria_por_id: {str(e)}")
            return None



    @staticmethod
    def insertar_categoria(nombre):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_insertar_categoria(%s);", (nombre,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error en insertar_categoria: {str(e)}")

    @staticmethod
    def actualizar_categoria(id_categoria, nuevo_nombre):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_actualizar_categoria(%s, %s);", (id_categoria, nuevo_nombre))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error en actualizar_categoria: {str(e)}")

    @staticmethod
    def eliminar_categoria(id_categoria):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_eliminar_categoria(%s);", (id_categoria,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error en eliminar_categoria: {str(e)}")
