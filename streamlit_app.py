import streamlit as st
import pandas as pd
from pymongo import MongoClient

st.set_page_config(layout="wide")

# Conexión a MongoDB
client = MongoClient("mongodb://137.184.143.185:27017/?directConnection=true")
db = client["CRM"]

def cargar_datos(coleccion_nombre, limit=100):  # Nuevo parámetro 'limit'
    coleccion = db[coleccion_nombre]
    datos = list(coleccion.find().limit(limit))  # Limitar registros
    return pd.DataFrame(datos)

# Título de la aplicación
st.title("Consulta de Colecciones CRM")

# Colecciones a mostrar
colecciones_a_mostrar = ["Actualizacion", "Demograficos"]

# Selector de colección
coleccion_seleccionada = st.selectbox("Seleccionar Colección", colecciones_a_mostrar)

# Botón de consulta
if st.button("Consultar"):
    try:
        # Mostrar tabla con límite de 100 registros
        df_mostrar = cargar_datos(coleccion_seleccionada)
        if not df_mostrar.empty:
            st.dataframe(df_mostrar.style.set_properties(**{'width': '100%'}))

            # Obtener todos los datos para la descarga
            df_descargar = cargar_datos(coleccion_seleccionada, limit=0)  # limit=0 para traer todos los registros

            # Botón de descarga con delimitador "|"
            st.download_button(
                label="Descargar todos los datos como CSV",
                data=df_descargar.to_csv(index=False, sep='|').encode('utf-8'),
                file_name=f'{coleccion_seleccionada}.csv',
                mime='text/csv',
            )
        else:
            st.warning("La colección seleccionada no tiene datos.")
    except Exception as e:
        st.error(f"Error al consultar la colección: {e}")

# Cerrar la conexión
client.close()
