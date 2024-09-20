from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
# load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = ("sqlite:///./satisfaction.db")

# Si DATABASE_URL no está definido, usar un valor por defecto


# Asegurarse de que DATABASE_URL sea una cadena de texto


# Crear el motor de la base de datos
# Nota: `check_same_thread` es específico de SQLite y se debe usar solo si es necesario
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

# Configurar el SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base para los modelos
Base = sqlalchemy.orm.declarative_base()

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()