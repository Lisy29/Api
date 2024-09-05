from fastapi import APIRouter, Depends, Form
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pandas as pd
import joblib
from database import get_db  # Asegúrate de que esta importación es correcta

from models import PassengerSatisfaction

router = APIRouter()

# Cargar el modelo entrenado
model = joblib.load('rf_model_v1.pkl')

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
    passenger_satisfaction: str

# Función para estandarizar y preprocesar los datos
def preprocess_input(data):
    # Convertir todos los valores string a minúsculas
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.lower()
    return data

# Ruta para recibir los datos
@router.post("/submit/")
async def submit_form(
    input_data: SatisfactionInput,  # Usa el modelo Pydantic en lugar de Form(...)
    db: Session = Depends(get_db)  # Inyectar la sesión de base de datos
):
    # Convertir los datos de entrada en un diccionario
    data = input_data.dict()

    # Preprocesar los datos
    processed_data = preprocess_input(data)

    try:
        # Verificar si los datos ya existen
        exists = db.query(PassengerSatisfaction).filter_by(**processed_data).first()
        if exists:
            return {"message": "Los datos ya existen en la base de datos."}
        else:
            # Crear una nueva instancia de PassengerSatisfaction con los datos procesados
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

# Ruta de prueba
@router.get("/")
def read_root():
    return {"message": "API de predicción de satisfacción de pasajeros de aerolíneas"}

# Ruta para predecir la satisfacción
@router.post("/predict/")
def predict_satisfaction(input_data: SatisfactionInput):
    # Convertir los datos de entrada en un diccionario y preprocesar
    input_dict = input_data.dict()
    standardized_data = preprocess_input(input_dict)
    
    # Convertir los datos estandarizados en un DataFrame de pandas
    input_df = pd.DataFrame([standardized_data])
    
    # Realizar la predicción
    prediction = model.predict(input_df)
    
    # Retornar la predicción como una respuesta JSON
    return {"predicted_satisfaction": int(prediction[0])}
