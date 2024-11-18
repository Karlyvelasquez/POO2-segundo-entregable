from sqlalchemy import create_engine
from flask import Flask, json
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

class ModelVentas:



    @staticmethod
    def crear_venta_con_detalles(cliente_id, usuario_id, detalles):
        try:
            conn = engine.raw_connection()
            cur = conn.cursor()

        # Correcta llamada al procedimiento
            cur.execute("SELECT sp_insertar_venta_con_detalles(%s, %s, %s);", 
            (cliente_id, usuario_id, json.dumps(detalles)))
            venta_id = cur.fetchone()[0]  
            conn.commit()
        
            cur.close()
            conn.close()

            return venta_id
        except Exception as e:
            print(f"Error al crear venta con detalles: {e}")
            raise


    @staticmethod
    def guardar_venta(fecha, usuario_id, cliente_id, total, detalles):
        try:
            conn = engine.raw_connection()
            cur = conn.cursor()
            cur.execute("BEGIN;")
            cur.callproc('sp_insertar_venta', [fecha, usuario_id, cliente_id, total, json.dumps(detalles)])
            cur.execute("COMMIT;")
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error al guardar venta: {e}")
            raise



    @staticmethod
    def crear_venta(cliente_id, usuario_id, detalles):
        try:
            conn = engine.raw_connection()
            cur = conn.cursor()
            
            # Llamada correcta al procedimiento usando CALL
            cur.execute("SELECT sp_insertar_venta_con_detalles(%s, %s, %s);", 
            (cliente_id, usuario_id, json.dumps(detalles)))
            venta_id = cur.fetchone()[0]
            
            conn.commit()  # Asegúrate de hacer commit después de la ejecución
            cur.close()
            conn.close()
            
            print("Venta y detalles registrados correctamente.")
        except Exception as e:
            print(f"Error al crear venta con detalles: {e}")
            raise
    
    @staticmethod
    def obtener_ventas():
        try:
            conn = engine.raw_connection()
            cur = conn.cursor()
        
            cur.execute("CALL sp_obtener_ventas('ventas_cursor');")
            cur.execute("FETCH ALL IN ventas_cursor;")
            ventas = cur.fetchall()

            cur.close()
            conn.close()
        
            return [
            {
                "id": v[0],
                "fecha": v[1],
                "usuario": v[2],  
                "cliente": v[3],  
                "total": v[4]
            }
            for v in ventas
        ]
        except Exception as e:
            print(f"Error en obtener_ventas: {str(e)}")
            return []



    @staticmethod
    def obtener_detalles_venta(venta_id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
        
        # Inicia una transacción para manejar el cursor
            cursor.execute("BEGIN;")
        
        # Llama al procedimiento almacenado correctamente con CALL
            cursor.execute("CALL sp_obtener_detalles_venta('detalles_cursor', %s);", (venta_id,))
        
        # Recupera los datos del cursor abierto
            cursor.execute("FETCH ALL IN detalles_cursor;")
            detalles = cursor.fetchall()
        
        # Finaliza la transacción
            cursor.execute("COMMIT;")
            cursor.close()
            conn.close()
        
            return detalles
        except Exception as e:
            print(f"Error en obtener_detalles_venta: {str(e)}")
            raise







    @staticmethod
    def eliminar_venta(venta_id):
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute("CALL sp_eliminar_venta(%s);", [venta_id])
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error en eliminar_venta: {str(e)}")
            return False
