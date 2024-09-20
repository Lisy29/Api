import streamlit as st
import requests
from enum import Enum

API_URL = "http://localhost:8000"

class CustomerType(str, Enum):
    LOYAL = "Loyal Customer"
    DISLOYAL = "Disloyal Customer"

class TravelType(str, Enum):
    PERSONAL = "Personal Travel"
    BUSINESS = "Business Travel"

class TripClass(str, Enum):
    ECO = "Eco"
    ECO_PLUS = "Eco Plus"
    BUSINESS = "Business"

class Satisfaction(str, Enum):
    NEUTRAL = "Neutral or Dissatisfied"
    SATISFIED = "Satisfied"

st.set_page_config(page_title="Satisfacción del Pasajero", page_icon="✈️")


st.title("📋 Formulario de Satisfacción del Pasajero 🛫😊")

st.write("¡Por favor, llena los siguientes campos para ayudarnos a mejorar! 🙏")

gender = st.selectbox("Seleccione Género:", ['Female', 'Male'])
input_data = {'gender': 0 if gender == 'Female' else 1}

customer_type = st.selectbox("Seleccione Tipo de Cliente:", [CustomerType.LOYAL.value, CustomerType.DISLOYAL.value])
input_data['customer_type'] = customer_type

age = st.slider("Seleccione Edad:", 0, 120, 25)
input_data['age'] = age

travel_type = st.selectbox("Seleccione Tipo de Viaje:", [TravelType.PERSONAL.value, TravelType.BUSINESS.value])
input_data['travel_type'] = travel_type

trip_class = st.selectbox("Seleccione Clase:", [TripClass.ECO.value, TripClass.ECO_PLUS.value, TripClass.BUSINESS.value])
input_data['trip_class'] = trip_class

flight_distance = st.slider("Distancia de Vuelo (km):", 0, 10000, 500)
input_data['flight_distance'] = flight_distance

def get_satisfaction(label: str):
    return st.slider(label, 0, 5, 3)

input_data['inflight_wifi_service'] = get_satisfaction("Servicio de Wifi a Bordo")
input_data['departure_arrival_time_convenient'] = get_satisfaction("Conveniencia del Tiempo de Salida/Llegada")
input_data['online_booking'] = get_satisfaction("Facilidad de Reserva Online")
input_data['gate_location'] = get_satisfaction("Ubicación de la Puerta")
input_data['food_and_drink'] = get_satisfaction("Comida y Bebida")
input_data['online_boarding'] = get_satisfaction("Embarque Online")
input_data['seat_comfort'] = get_satisfaction("Comodidad del Asiento")
input_data['inflight_entertainment'] = get_satisfaction("Entretenimiento a Bordo")
input_data['onboard_service'] = get_satisfaction("Servicio a Bordo")
input_data['leg_room_service'] = get_satisfaction("Espacio para las Piernas")
input_data['baggage_handling'] = get_satisfaction("Manejo del Equipaje")
input_data['checkin_service'] = get_satisfaction("Servicio de Check-in")
input_data['inflight_service'] = get_satisfaction("Servicio en Vuelo")
input_data['cleanliness'] = get_satisfaction("Limpieza")

departure_delay = st.slider("Retraso en la Salida (en minutos):", 0, 1000, 0)
input_data['departure_delay_in_minutes'] = departure_delay

# arrival_delay = st.slider("Retraso en la Llegada (en minutos):", 0, 1000, 0)
# input_data['arrival_delay_in_minutes'] = arrival_delay

satisfaction_client = st.selectbox("¿Está satisfecho con el servicio?", [Satisfaction.NEUTRAL.value, Satisfaction.SATISFIED.value])
input_data['satisfaction'] = satisfaction_client

def send_data_to_api(data):
    try:
        response = requests.post(f"{API_URL}/submit_and_predict/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error al conectar con la API: {str(e)}")
        if e.response is not None:
            st.error(e.response.text)
        return None

if st.button("Guardar Datos y Predecir"):
    result = send_data_to_api(input_data)
    if result:
        st.success("Datos Guardados Exitosamente")
        st.success(f"La predicción de satisfacción del cliente es: {result['predicted_satisfaction']}")
        st.info(f"La satisfacción real del cliente es: {result['satisfaction']}")
        
        if result['predicted_satisfaction'] == result['satisfaction']:
            st.success("¡La predicción coincide con la satisfacción real del cliente!")
        else:
            st.warning("La predicción no coincide con la satisfacción real del cliente.")