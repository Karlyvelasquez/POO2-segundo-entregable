import os

class Config:
    SECRET_KEY = os.urandom(24)
    DEBUG = True  # Cambia a False en producción
    SQLALCHEMY_DATABASE_URI = 'postgresql://FerreteriaLa32_owner:LacOd5FW0Xzy@ep-odd-water-a56xxypi.us-east-2.aws.neon.tech/FerreteriaLa32?sslmode=require'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  
