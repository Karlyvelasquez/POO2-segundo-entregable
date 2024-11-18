from sqlalchemy import text
from Models.entities.Usuarios import usuarios
from werkzeug.security import check_password_hash


class modeluser:

    @classmethod
    def registrar(cls, db, usuario):
        try:
            consulta = text("SELECT registrar_usuario(:p_cedula, :p_nombre, :p_email, :p_contraseña)")
            db.session.execute(consulta, {
                "p_cedula": usuario.cedula,
                "p_nombre": usuario.nombre,
                "p_email": usuario.email,
                "p_contraseña": usuario.contraseña
            })
            db.session.commit()
            return True
        except Exception as ex:
            raise Exception(ex)


class Usuario:
    @classmethod
    def login(cls, db, email, contraseña):
        try:
            consulta = text("""
                CALL login_usuario(:p_email, :p_contraseña, 
                :p_id, :p_nombre, :p_email_ret, :p_rol_id)
            """)
            
            result = db.session.execute(consulta, {
                "p_email": email,
                "p_contraseña": contraseña,
                "p_id": None,  # Parámetro de salida
                "p_nombre": None,  # Parámetro de salida
                "p_email_ret": None,  # Parámetro de salida
                "p_rol_id": None  # Parámetro de salida
            }).fetchone()

            if result:
                # Crear el objeto usuario e ingresar los valores en los atributos
                usuario = cls()
                usuario.id = result[0]
                usuario.nombre = result[1]
                usuario.email = result[2]
                usuario.rol_id = result[3]
                
                return usuario
            
            return None
        except Exception as ex:
            raise Exception(f"Error al ejecutar el procedimiento: {str(ex)}")



    # Método para cambiar la contraseña
    @classmethod
    def cambiar_contraseña(cls, db, email, nueva_contraseña):
        try:
            # Actualizar la contraseña del usuario
            consulta = text("""
                CALL cambiar_contraseña(:email, :nueva_contraseña)
            """)
            db.session.execute(consulta, {"email": email, "nueva_contraseña": nueva_contraseña})
            db.session.commit()
        except Exception as ex:
            raise Exception(f"Error al cambiar la contraseña: {str(ex)}")



        
    @classmethod
    def actualizar(cls, db, usuario):
        try:
            consulta = text("CALL actualizar_usuario(:cedula, :nombre, :email)")
            db.session.execute(consulta, {
                "cedula": usuario.cedula,
                "nombre": usuario.nombre,
                "email": usuario.email
            })
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback() 
            raise Exception(ex)

        
    @staticmethod
    def buscar_usuario_por_cedula(db, cedula):
        usuario = db.session.query(usuarios).filter(usuarios.cedula == cedula).first()
        return usuario
