from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from pydantic import BaseModel
import joblib
from schema import PassengerFormData

# Cargar el modelo entrenado
model = joblib.load('rf_model.pkl')
print("Modelo cargado correctamente")

# Configurar la base de datos
DATABASE_URL = "sqlite:///satisfaction.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir el modelo de la base de datos
class PassengerSatisfaction(Base):
    __tablename__ = 'passenger_satisfaction'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(String)
    customer_type = Column(String)
    age = Column(Integer)
    travel_type = Column(String)
    trip_class = Column(String)
    flight_distance = Column(Integer)
    inflight_wifi_service = Column(Integer)
    departure_arrival_time_convenient = Column(Integer)
    online_booking = Column(Integer)
    gate_location = Column(Integer)
    food_and_drink = Column(Integer)
    online_boarding = Column(Integer)
    seat_comfort = Column(Integer)
    inflight_entertainment = Column(Integer)
    onboard_service = Column(Integer)
    leg_room_service = Column(Integer)
    baggage_handling = Column(Integer)
    checkin_service = Column(Integer)
    inflight_service = Column(Integer)
    cleanliness = Column(Integer)
    departure_delay_in_minutes = Column(Integer)
    arrival_delay_in_minutes = Column(Integer)
    passenger_satisfaction = Column(String)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Definir el esquema de los datos de entrada
class SatisfactionInput(BaseModel):
    gender: str
    customer_type: str
    age: int
    travel_type: str
    trip_class: str
    flight_distance: int
    inflight_wifi_service: int
    departure_arrival_time_convenient: int
    online_booking: int
    gate_location: int
    food_and_drink: int
    online_boarding: int
    seat_comfort: int
    inflight_entertainment: int
    onboard_service: int
    leg_room_service: int
    baggage_handling: int
    checkin_service: int
    inflight_service: int
    cleanliness: int
    departure_delay_in_minutes: int
    arrival_delay_in_minutes: int


# Inicializar la aplicación FastAPI
app = FastAPI()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para estandarizar y preprocesar los datos
def preprocess_input(data):
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.lower()
    return data

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "API de predicción de satisfacción de pasajeros de aerolíneas"}

# Ruta para predecir la satisfacción
@app.post("/predict/")
def predict_satisfaction(input_data: SatisfactionInput):
    data = input_data.dict()
    df = pd.DataFrame([list(data.values())], columns=['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class',
       'Flight Distance', 'Inflight wifi service',
       'Departure/Arrival time convenient', 'Ease of Online booking',
       'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
       'Inflight entertainment', 'On-board service', 'Leg room service',
       'Baggage handling', 'Checkin service', 'Inflight service',
       'Cleanliness', 'Departure Delay in Minutes', 'Arrival Delay in Minutes'])
    if not df.empty:
        prediction = model.predict(df)
        return {"predicted_satisfaction": int(prediction[0])}

# Ruta para recibir los datos y guardarlos en la base de datos
@app.post("/submit/")
async def submit_form(
    data: SatisfactionInput,  # Cambiar a SatisfactionInput aquí
    db: Session = Depends(get_db)  # Obtener sesión de base de datos
):
    data_dict = data.dict()
    processed_data = preprocess_input(data_dict)

    try:
        exists = db.query(PassengerSatisfaction).filter_by(**processed_data).first()
        if exists:
            return {"message": "Los datos ya existen en la base de datos."}
        else:
            new_entry = PassengerSatisfaction(**processed_data)
            db.add(new_entry)
            db.commit()
            return {"message": "Datos guardados correctamente en la base de datos"}
    except IntegrityError:
        db.rollback()
        return {"error": "Error de integridad en la base de datos."}
    except Exception as e:
        db.rollback()
        return {"error": f"Error al guardar los datos: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

