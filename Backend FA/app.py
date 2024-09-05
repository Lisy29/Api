from fastapi import FastAPI, Form
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import pandas as pd
import joblib

# Inicializar la aplicación FastAPI
app = FastAPI()

# Cargar el modelo entrenado
model = joblib.load('rf_model.pkl')
print("modelo cargado correctamente")


# Configurar SQLite y SQLAlchemy
DATABASE_URL = "sqlite:///satisfaction.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

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

# Crear la tabla si no existe
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

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
@app.post("/submit/")
async def submit_form(
    gender: str = Form(...),  # String para "Male" y "Female"
    customer_type: str = Form(...),  # String para "Loyal" y "Disloyal"
    age: int = Form(...),
    travel_type: str = Form(...),  # String para "Business" y "Personal"
    trip_class: str = Form(...),
    flight_distance: int = Form(...),
    inflight_wifi_service: int = Form(...),
    departure_arrival_time_convenient: int = Form(...),
    online_booking: int = Form(...),
    gate_location: int = Form(...),
    food_and_drink: int = Form(...),
    online_boarding: int = Form(...),
    seat_comfort: int = Form(...),
    inflight_entertainment: int = Form(...),
    onboard_service: int = Form(...),
    leg_room_service: int = Form(...),
    baggage_handling: int = Form(...),
    checkin_service: int = Form(...),
    inflight_service: int = Form(...),
    cleanliness: int = Form(...),
    departure_delay_in_minutes: int = Form(...),
    arrival_delay_in_minutes: int = Form(...),
    passenger_satisfaction: str = Form(...)
):
    # Crear un diccionario con los datos del formulario
    data = {
        "gender": gender,
        "customer_type": customer_type,
        "age": age,
        "travel_type": travel_type,
        "trip_class": trip_class,
        "flight_distance": flight_distance,
        "inflight_wifi_service": inflight_wifi_service,
        "departure_arrival_time_convenient": departure_arrival_time_convenient,
        "online_booking": online_booking,
        "gate_location": gate_location,
        "food_and_drink": food_and_drink,
        "online_boarding": online_boarding,
        "seat_comfort": seat_comfort,
        "inflight_entertainment": inflight_entertainment,
        "onboard_service": onboard_service,
        "leg_room_service": leg_room_service,
        "baggage_handling": baggage_handling,
        "checkin_service": checkin_service,
        "inflight_service": inflight_service,
        "cleanliness": cleanliness,
        "departure_delay_in_minutes": departure_delay_in_minutes,
        "arrival_delay_in_minutes": arrival_delay_in_minutes,
        "passenger_satisfaction": passenger_satisfaction
    }

    # Preprocesar los datos
    processed_data = preprocess_input(data)

    try:
        # Verificar si los datos ya existen
        exists = session.query(PassengerSatisfaction).filter_by(**processed_data).first()
        if exists:
            return {"message": "Los datos ya existen en la base de datos."}
        else:
            # Crear una nueva instancia de PassengerSatisfaction con los datos procesados
            new_entry = PassengerSatisfaction(**processed_data)
            session.add(new_entry)
            session.commit()
            return {"message": "Datos guardados correctamente en la base de datos"}
    except IntegrityError:
        session.rollback()
        return {"error": "Error de integridad en la base de datos."}
    except Exception as e:
        session.rollback()
        return {"error": f"Error al guardar los datos: {str(e)}"}

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "API de predicción de satisfacción de pasajeros de aerolíneas"}

# Ruta para predecir la satisfacción
@app.post("/predict/")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
