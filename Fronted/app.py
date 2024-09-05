import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Configurar SQLite y crear la base de datos si no existe
DATABASE_URL = "sqlite:///satisfaction.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

# Definir el modelo de la base de datos usando SQLAlchemy
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

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Cargar los datos del CSV (esto es solo para obtener las columnas y valores únicos)
file_path = 'data/airline_clean.csv'  # Ruta del archivo CSV
df = pd.read_csv(file_path)

# Eliminar columnas no deseadas como 'Unnamed' y 'id'
#df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
#if 'id' in df.columns:
    #df = df.drop(columns=['id'])

# Convertir los valores únicos de cada columna a minúsculas
unique_values_dict = {column: [str(val).lower() for val in df[column].unique().tolist()] for column in df.columns}

# Crear la interfaz de Streamlit
st.title("Formulario de Satisfacción del Pasajero")

# Crear un desplegable para cada característica
input_data = {}
for column, unique_values in unique_values_dict.items():
    if df[column].dtype == 'object':  # Solo desplegables para columnas de tipo objeto
        selected_value = st.selectbox(f"Seleccione {column}:", unique_values)
        input_data[column] = selected_value.lower()  # Convertir a minúsculas
    else:  # Para columnas numéricas
        input_data[column] = st.number_input(f"Introduzca {column}:", min_value=0, step=1)

# Botón de guardar datos
if st.button("Guardar Datos"):
    try:
        # Verificar si los datos ya existen en la base de datos
        exists = session.query(PassengerSatisfaction).filter_by(**input_data).first()
        if exists:
            st.warning("Los datos ya existen en la base de datos.")
        else:
            # Crear una nueva instancia de PassengerSatisfaction con los datos ingresados
            new_entry = PassengerSatisfaction(**input_data)
            
            # Agregar la nueva entrada a la sesión
            session.add(new_entry)
            
            # Confirmar la transacción
            session.commit()
            
            st.success("Datos guardados correctamente en la base de datos")
    
    except IntegrityError as e:
        session.rollback()
        st.error(f"Error de integridad de la base de datos: {str(e)}")
    except Exception as e:
        session.rollback()
        st.error(f"Error al guardar los datos: {str(e)}")

# Cerrar la sesión al final
session.close()
