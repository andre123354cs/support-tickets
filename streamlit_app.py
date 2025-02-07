import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time
import logging

# Configuración de logging (se guarda en un archivo llamado 'app.log')
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


st.title("Descarga de Informe Novaventa")

import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Conexión a MongoDB (misma URI que antes)
client = MongoClient("mongodb://137.184.143.185/:27017/?directConnection=true")
db = client["CRM"]

def obtener_colecciones(db):
    return db.list_collection_names()

def cargar_datos(coleccion_nombre):
    coleccion = db[coleccion_nombre]
    datos = list(coleccion.find())
    return pd.DataFrame(datos)

# Título de la aplicación
st.title("Consulta de Colecciones CRM")

# Selector de colección
colecciones = obtener_colecciones(db)
coleccion_seleccionada = st.selectbox("Seleccionar Colección", colecciones)

# Botón de consulta
if st.button("Consultar"):
    try:
        df = cargar_datos(coleccion_seleccionada)
        if not df.empty:  # Verifica si el DataFrame no está vacío
            st.dataframe(df)  # Muestra la tabla
            # Botón de descarga (opcional)
            st.download_button(
                label="Descargar datos como CSV",
                data=df.to_csv(index=False).encode('utf-8'),  # index=False para no guardar el índice
                file_name=f'{coleccion_seleccionada}.csv',  # Nombre del archivo basado en la colección
                mime='text/csv',
            )
        else:
            st.warning("La colección seleccionada no tiene datos.")  # Mensaje si no hay datos
    except Exception as e:
        st.error(f"Error al consultar la colección: {e}")  # Muestra el error específico

# Cerrar la conexión a MongoDB al finalizar (buena práctica)
client.close()
