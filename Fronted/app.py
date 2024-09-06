import streamlit as st
import requests

# Diccionarios de mapeo para campos categóricos
gender_map = {'Female': 'female', 'Male': 'male'}
customer_type_map = {'Loyal': 'loyal', 'Disloyal': 'disloyal'}
travel_type_map = {'Personal Travel': 'personal travel', 'Business Travel': 'business travel'}
class_map = {'Eco': 'eco', 'Eco Plus': 'eco plus', 'Business': 'business'}

# Diccionario de satisfacción para los campos con valores 1 a 5
satisfaction_scale = {
    'Malo': 1,
    'Regular': 2,
    'Neutro': 3,
    'Bueno': 4,
    'Excelente': 5
}

# Crear la interfaz de Streamlit
st.title("Formulario de Satisfacción del Pasajero")

# Selección para el género
gender = st.selectbox("Seleccione Género:", ['Female', 'Male'], key="gender")
input_data = {'gender': gender_map[gender]}

# Selección para el tipo de cliente
customer_type = st.selectbox("Seleccione Tipo de Cliente:", ['Loyal', 'Disloyal'], key="customer_type")
input_data['customer_type'] = customer_type_map[customer_type]

# Entrada para la edad (0 a 100)
age = st.slider("Seleccione Edad:", 0, 100, 25, key="age")
input_data['age'] = age

# Selección para el tipo de viaje
travel_type = st.selectbox("Seleccione Tipo de Viaje:", ['Personal Travel', 'Business Travel'], key="travel_type")
input_data['travel_type'] = travel_type_map[travel_type]

# Selección para la clase
trip_class = st.selectbox("Seleccione Clase:", ['Eco', 'Eco Plus', 'Business'], key="trip_class")
input_data['trip_class'] = class_map[trip_class]

# Entrada para la distancia de vuelo (0 a 10000)
flight_distance = st.slider("Distancia de Vuelo (km):", 0, 10000, 500, key="flight_distance")
input_data['flight_distance'] = flight_distance

# Preguntas de satisfacción (escala de 1 a 5)
inflight_wifi = st.selectbox("Servicio de Wifi a Bordo:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="inflight_wifi")
input_data['inflight_wifi_service'] = satisfaction_scale[inflight_wifi]

departure_arrival_time_convenient = st.selectbox("Conveniencia del Tiempo de Salida/Llegada:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="departure_arrival_time_convenient")
input_data['departure_arrival_time_convenient'] = satisfaction_scale[departure_arrival_time_convenient]

online_booking = st.selectbox("Facilidad de Reserva Online:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="online_booking")
input_data['online_booking'] = satisfaction_scale[online_booking]

gate_location = st.selectbox("Ubicación de la Puerta:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="gate_location")
input_data['gate_location'] = satisfaction_scale[gate_location]

food_and_drink = st.selectbox("Comida y Bebida:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="food_and_drink")
input_data['food_and_drink'] = satisfaction_scale[food_and_drink]

online_boarding = st.selectbox("Embarque Online:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="online_boarding")
input_data['online_boarding'] = satisfaction_scale[online_boarding]

seat_comfort = st.selectbox("Comodidad del Asiento:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="seat_comfort")
input_data['seat_comfort'] = satisfaction_scale[seat_comfort]

inflight_entertainment = st.selectbox("Entretenimiento a Bordo:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="inflight_entertainment")
input_data['inflight_entertainment'] = satisfaction_scale[inflight_entertainment]

onboard_service = st.selectbox("Servicio a Bordo:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="onboard_service")
input_data['onboard_service'] = satisfaction_scale[onboard_service]

leg_room_service = st.selectbox("Espacio para las Piernas:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="leg_room_service")
input_data['leg_room_service'] = satisfaction_scale[leg_room_service]

baggage_handling = st.selectbox("Manejo del Equipaje:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="baggage_handling")
input_data['baggage_handling'] = satisfaction_scale[baggage_handling]

checkin_service = st.selectbox("Servicio de Check-in:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="checkin_service")
input_data['checkin_service'] = satisfaction_scale[checkin_service]

inflight_service = st.selectbox("Servicio en Vuelo:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="inflight_service")
input_data['inflight_service'] = satisfaction_scale[inflight_service]

cleanliness = st.selectbox("Limpieza:", ['Malo', 'Regular', 'Neutro', 'Bueno', 'Excelente'], key="cleanliness")
input_data['cleanliness'] = satisfaction_scale[cleanliness]

# Entrada para el retraso de salida (en minutos)
departure_delay = st.slider("Retraso en la Salida (en minutos):", 0, 1000, 0, key="departure_delay")
input_data['departure_delay_in_minutes'] = departure_delay

# Entrada para el retraso de llegada (en minutos)
arrival_delay = st.slider("Retraso en la Llegada (en minutos):", 0, 1000, 0, key="arrival_delay")
input_data['arrival_delay_in_minutes'] = arrival_delay

# Función para enviar datos a la API FastAPI
def send_data_to_api(data):
    try:
        response = requests.post("http://localhost:8000/submit/", json=data)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.RequestException as e:
        st.error(f"Error al conectar con la API: {str(e)}")
        return None

# Botón de guardar datos

if st.button("Guardar Datos"):
    print(input_data)
    result = send_data_to_api(input_data)
    if result:
        if 'error' in result:
            st.error(result['error'])
        else:
            st.success(result['message'])
