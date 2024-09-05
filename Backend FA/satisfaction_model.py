import joblib
import pandas as pd

# Cargar el modelo entrenado desde un archivo .pkl
model = joblib.load('rf_model.plk')

def preprocess_input(data: dict) -> dict:
    """
    Preprocesa los datos de entrada para convertir valores no estandarizados en valores estandarizados.
    
    Args:
    data (dict): Un diccionario con los datos de entrada no estandarizados.

    Returns:
    dict: Un diccionario con los datos estandarizados.
    """
    # Mapeo de valores para estandarizar
    data['gender'] = 1 if data['gender'] == 'Male' else 0
    data['customer_type'] = 1 if data['customer_type'] == 'Loyal' else 0
    data['travel_type'] = 1 if data['travel_type'] == 'Business' else 0
    
    # Si 'trip_class' es "Eco", "Eco Plus" o "Business", transformamos a valores numéricos
    trip_class_map = {"Eco": 0, "Eco Plus": 1, "Business": 2}
    data['trip_class'] = trip_class_map.get(data['trip_class'], 0)
    
    return data

def predict_satisfaction(features: dict) -> int:
    """
    Realiza una predicción de satisfacción utilizando el modelo cargado.
    
    Args:
    features (dict): Un diccionario con las características requeridas para la predicción.

    Returns:
    int: La predicción de satisfacción.
    """
    # Preprocesar los datos de entrada
    standardized_data = preprocess_input(features)
    
    # Convertir las características estandarizadas en un DataFrame
    input_df = pd.DataFrame([standardized_data])
    
    # Realizar la predicción
    prediction = model.predict(input_df)
    
    # Retornar la predicción
    return int(prediction[0])