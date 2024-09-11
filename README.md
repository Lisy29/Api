## 📁 **Estructura del Proyecto**

```bash
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



⚙️ Predicción de Satisfacción - Machine Learning

Este proyecto implementa un sistema de predicción de satisfacción de clientes usando Machine Learning. La aplicación tiene dos componentes principales:

- 🖥️ **API construida con FastAPI** para procesar y predecir los datos.
- 🌐 **Interfaz de usuario desarrollada con Streamlit** para recolectar datos del usuario y mostrar predicciones en tiempo real.

🚀 Requisitos

Te recomendamos crear y activar un entorno virtual para gestionar las dependencias. Puedes hacerlo con los siguientes comandos:


python -m venv env  # Crea el entorno virtual con nombre 'env'
source env/bin/activate  # Activa el entorno en Unix/Mac
.\env\Scripts\Activate  # Activa el entorno en Windows

Para desactivar el entorno:
deactivate

Instala las dependencias ejecutando:
pip install -r requirements.txt

🛠️ Características del Proyecto

API en FastAPI: Recibe solicitudes con datos del usuario y devuelve predicciones de satisfacción.
Interfaz en Streamlit: Permite a los usuarios ingresar datos y recibir una predicción de forma visual e interactiva.
Modelo de Machine Learning: Predice la satisfacción del cliente basado en varias características recolectadas.

▶️ Cómo Ejecutar el Proyecto

1. API en FastAPI
Para ejecutar la API, navega al directorio donde se encuentra main.py y ejecuta el siguiente comando:
uvicorn app.main:app --reload

Esto iniciará un servidor en http://localhost:8000 donde puedes realizar solicitudes POST para obtener predicciones.

2. Interfaz de Usuario en Streamlit
Para lanzar la aplicación de Streamlit, navega al directorio donde se encuentra app.py y ejecuta:
streamlit run streamlit_app/app.py

Esto abrirá la aplicación en tu navegador, generalmente en http://localhost:8501.

🔍 Cómo Funciona

Entrenamiento del Modelo: El modelo fue entrenado con un conjunto de datos que incluye variables como edad, ingresos, género, etc., para predecir la satisfacción del cliente.
Predicción: El modelo toma como entrada los datos proporcionados y devuelve una predicción de la satisfacción.
Interfaz de Streamlit: El usuario ingresa datos en la interfaz y ve los resultados de predicción.
🔧 Próximos Pasos

Mejorar la precisión del modelo.
Añadir autenticación a la API para mayor seguridad.
Implementar validación de datos más robusta en FastAPI.
Mejorar la interfaz de Streamlit con gráficos adicionales y análisis visual.

🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar, por favor abre un issue o un pull request.

