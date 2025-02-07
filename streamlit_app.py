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

from pymongo import MongoClient
import pandas as pd
import tkinter as tk
from tkinter import ttk

def obtener_colecciones(db):
    """Obtiene una lista de las colecciones en la base de datos."""
    return db.list_collection_names()

def consultar_coleccion():
    """Consulta la colección seleccionada y muestra los resultados en la tabla."""
    coleccion_nombre = combo_colecciones.get()
    if coleccion_nombre:
        coleccion = db[coleccion_nombre]
        datos = list(coleccion.find())  # Obtener todos los documentos
        df = pd.DataFrame(datos)

        # Limpiar la tabla anterior
        for row in tabla.get_children():
            tabla.delete(row)

        # Insertar nuevos datos en la tabla
        for _, row in df.iterrows():
            tabla.insert("", tk.END, values=list(row))

# Conexión a MongoDB
client = MongoClient("mongodb://137.184.143.185/:27017/?directConnection=true")
db = client["CRM"]  # Seleccionar la base de datos CRM

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Consulta de Colecciones CRM")

# Etiqueta y ComboBox para seleccionar colección
etiqueta_colecciones = ttk.Label(ventana, text="Seleccionar Colección:")
etiqueta_colecciones.pack(pady=5)

colecciones = obtener_colecciones(db)
combo_colecciones = ttk.Combobox(ventana, values=colecciones)
combo_colecciones.pack(pady=5)
combo_colecciones.current(0)  # Seleccionar la primera colección por defecto

# Botón de consulta
boton_consulta = ttk.Button(ventana, text="Consultar", command=consultar_coleccion)
boton_consulta.pack(pady=10)

# Tabla para mostrar los datos
tabla = ttk.Treeview(ventana, columns=[], show="headings")
tabla.pack()

# Ejecutar la aplicación
ventana.mainloop()
