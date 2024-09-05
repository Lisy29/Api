from fastapi import Depends
from sqlalchemy.orm import Session
from models import SessionLocal

def get_db() -> Session:
    db = SessionLocal()  # Crear una nueva sesión de base de datos
    try:
        yield db  # Pasar la sesión a la ruta que la necesita
    finally:
        db.close()  # Cerrar la sesión cuando ya no se necesite
