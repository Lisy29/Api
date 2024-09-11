Predicción de Satisfacción - Machine Learning

Este proyecto implementa un sistema de predicción de satisfacción de clientes usando Machine Learning. La aplicación tiene dos componentes principales:

API construida con FastAPI para procesar y predecir los datos.

Interfaz de usuario desarrollada con Streamlit para recolectar datos del usuario y mostrar predicciones en tiempo real.
Estructura del Proyecto

.
├── app
│   ├── main.py          # API en FastAPI
│   └── models.py        # Modelos de predicción (Machine Learning)
├── streamlit_app
│   └── app.py           # Interfaz de usuario en Streamlit
├── models
│   └── model.pkl        # Modelo entrenado en formato pickle
├── README.md            # Este archivo
├── requirements.txt     # Dependencias del proyecto
└── notebooks
    └── EDA.ipynb        # Análisis exploratorio de datos


Te recomendamos crear y activar un entorno virtual, puedes ejecutar el siguiente comando:
Python -m ven env #crea el entorno con nombre env
./env/Scripts/Activate  #activa el entorno

No olvides desactivarlo si dejas de usarlo, usa el siguiente comando:

deactivate
    
Características del Proyecto

API en FastAPI: Se encarga de recibir solicitudes con datos del usuario y devolver predicciones de satisfacción.
Interfaz en Streamlit: Permite a los usuarios ingresar datos y recibir una predicción de forma visual y amigable.
Modelo de Machine Learning: El modelo predice la satisfacción del cliente en función de varias características recolectadas.
Requisitos
Para ejecutar este proyecto, necesitas instalar las siguientes dependencias:
Puedes instalarlas todas ejecutando:

pip install -r requirements.txt


Cómo Ejecutar el Proyecto

1. API en FastAPI
Para ejecutar la API, navega al directorio donde se encuentra main.py y ejecuta el siguiente comando:


uvicorn app.main:app --reload

Esto iniciará un servidor en http://localhost:8000 donde puedes realizar solicitudes POST para obtener predicciones.


2. Interfaz de Usuario en Streamlit
Para lanzar la aplicación de Streamlit, navega al directorio donde se encuentra app.py y ejecuta:


streamlit run streamlit_app2.py

Esto abrirá la aplicación en tu navegador, generalmente en http://localhost:8501, donde los usuarios pueden interactuar con la interfaz.

Cómo Funciona
Entrenamiento del Modelo: El modelo de predicción fue entrenado usando un conjunto de datos con características relevantes para predecir la satisfacción. Esto incluye variables como edad, ingresos, género, entre otros.

Predicción: El modelo toma como entrada los datos ingresados a través de Streamlit o enviados vía API, y devuelve una predicción de la satisfacción.

Interfaz: El usuario puede interactuar con la aplicación de Streamlit, ingresar los datos y ver los resultados de predicción.

Próximos Pasos

Mejorar la precisión del modelo.
Añadir autenticación a la API para mayor seguridad.
Implementar validación de datos más robusta en FastAPI.
Mejorar la interfaz de Streamlit con gráficos y análisis adicionales.

Contribuciones

Las contribuciones son bienvenidas. Por favor, siéntete libre de abrir un issue o un pull request si deseas colaborar.
