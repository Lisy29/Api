from fastapi import FastAPI
from models import Base, engine
from routers import router  

# Inicializar la aplicación FastAPI
app = FastAPI()

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Incluir el router de predicciones y cualquier otro router
app.include_router(router)

# Ruta de prueba
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de predicción de satisfacción de pasajeros"}


