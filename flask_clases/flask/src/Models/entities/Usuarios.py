from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)


    def __init__(self, nombre):
        self.nombre = nombre

class usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  # Relación con 'roles'

 
    rol = db.relationship('roles', backref='usuarios_rel') 

    def __init__(self, nombre, email, contraseña, rol_id):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.rol_id = rol_id

