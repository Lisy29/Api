from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pandas as pd
import joblib
from database import get_db  
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

    # Mapear los valores categóricos a los valores esperados por la base de datos
    column_mapping = {
        'gender': {'male': 'Male', 'female': 'Female'},
        'customer_type': {'loyal': 'Loyal', 'disloyal': 'Disloyal'},
        'travel_type': {'personal travel': 'Personal Travel', 'business travel': 'Business Travel'},
        'trip_class': {'eco': 'Eco', 'eco plus': 'Eco Plus', 'business': 'Business'},
        # Mapea otros campos si es necesario
    }

    for key, mapping in column_mapping.items():
        if processed_data[key] in mapping:
            processed_data[key] = mapping[processed_data[key]]

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
    try:
        # Convertir los datos de entrada en un diccionario y preprocesar
        input_dict = input_data.dict()
        standardized_data = preprocess_input(input_dict)
        
        # Crear el DataFrame con los nombres exactos de columnas que el modelo espera
        input_df = pd.DataFrame([{
            'Gender': standardized_data['gender'],
            'Customer Type': standardized_data['customer_type'],
            'Age': standardized_data['age'],
            'Type of Travel': standardized_data['travel_type'],
            'Class': standardized_data['trip_class'],
            'Flight Distance': standardized_data['flight_distance'],
            'Inflight wifi service': standardized_data['inflight_wifi_service'],
            'Departure/Arrival time convenient': standardized_data['departure_arrival_time_convenient'],
            'Ease of Online booking': standardized_data['online_booking'],
            'Gate location': standardized_data['gate_location'],
            'Food and drink': standardized_data['food_and_drink'],
            'Online boarding': standardized_data['online_boarding'],
            'Seat comfort': standardized_data['seat_comfort'],
            'Inflight entertainment': standardized_data['inflight_entertainment'],
            'On-board service': standardized_data['onboard_service'],
            'Leg room service': standardized_data['leg_room_service'],
            'Baggage handling': standardized_data['baggage_handling'],
            'Checkin service': standardized_data['checkin_service'],
            'Inflight service': standardized_data['inflight_service'],
            'Cleanliness': standardized_data['cleanliness'],
            'Departure Delay in Minutes': standardized_data['departure_delay_in_minutes'],
            'Arrival Delay in Minutes': standardized_data['arrival_delay_in_minutes']
        }])
        
        # Mostrar cómo luce el DataFrame
        print(f"DataFrame enviado al modelo:\n{input_df}")

        # Realizar la predicción
        prediction = model.predict(input_df)
        
        return {"predicted_satisfaction": int(prediction[0])}
    except ValueError as e:
        # Manejar errores relacionados con la predicción
        print(f"Error de Valor: {e}")
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
