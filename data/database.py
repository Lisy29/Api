from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import joblib

DATABASE_URL = "sqlite:///satisfaction.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)()

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

# Cargar el modelo entrenado
model = joblib.load('satisfaction_rf_model.pkl')

# Función para estandarizar y preprocesar los datos
def preprocess_input(data):
    # Convertir todos los valores string a minúsculas
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.lower()
    return data
