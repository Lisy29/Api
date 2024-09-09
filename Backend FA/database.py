from typing import Generator  # Importamos Generator para definir el tipo de retorno
from fastapi import Depends
from sqlalchemy.orm import Session
from models import SessionLocal

# Usamos Generator para anotar correctamente el tipo de retorno de la función
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # Crear una nueva sesión de base de datos
    try:
        yield db  # Pasar la sesión a la ruta que la necesita
    finally:
        db.close()  # Cerrar la sesión cuando ya no se necesite

