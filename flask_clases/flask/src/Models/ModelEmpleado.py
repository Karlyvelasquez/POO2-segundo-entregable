from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import Config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)


class ModelEmpleado:

    @staticmethod
    def obtener_empleados():
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_obtener_empleados('empleados_cursor');")
            cursor.execute("FETCH ALL IN empleados_cursor;")
            empleados = cursor.fetchall()
            cursor.close()
            conn.close()

            return [
                {
                    "id": emp[0],
                    "nombre": emp[1],
                    "email": emp[2],
                    "rol_nombre": emp[3],
                    "contrasena": emp[4]  
                } for emp in empleados
            ]
        except Exception as e:
            print(f"Error en obtener_empleados: {str(e)}")
            return []

    @staticmethod
    def obtener_empleado_por_id(id):
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute("CALL sp_obtener_empleado_por_id(%s, 'my_cursor');", [id])
        cursor.execute("FETCH ALL IN my_cursor;")
        empleado = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"id": empleado[0], "nombre": empleado[1], "email": empleado[2], "rol_id": empleado[3]}


    @staticmethod
    def agregar_empleado(nombre, email, rol_id, contrasena):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_agregar_empleado(%s, %s, %s, %s);", [nombre, email, rol_id, contrasena])
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            raise Exception(f"Error en agregar_empleado: {str(e)}")
        
    @staticmethod
    def obtener_roles():
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute("CALL sp_obtener_roles('roles_cursor');")  # Asume un cursor nombrado
        cursor.execute("FETCH ALL IN roles_cursor;")
        roles = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [{"id": rol[0], "nombre": rol[1]} for rol in roles]
    
    @staticmethod
    def eliminar_empleado(empleado_id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_eliminar_empleado(%s);", [empleado_id])
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar empleado: {str(e)}")
            return False
        
    
    @staticmethod
    def editar_empleado(empleado_id, email, rol_id, nueva_contrasena):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute(
                "CALL sp_editar_empleado(%s, %s, %s, %s);",
                [empleado_id, email, rol_id, nueva_contrasena]
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error en editar_empleado: {str(e)}")
            return False
