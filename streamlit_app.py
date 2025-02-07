import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient("mongodb://137.184.143.185:27017/?directConnection=true")
db = client["CRM"]

def cargar_datos(coleccion_nombre):
    coleccion = db[coleccion_nombre]
    datos = list(coleccion.find())
    return pd.DataFrame(datos)

# Título de la aplicación
st.title("Consulta de Colecciones CRM")

# Colecciones específicas que quieres mostrar
colecciones_a_mostrar = ["Actualizacion", "Demograficos"]

# Selector de colección (con las colecciones filtradas)
coleccion_seleccionada = st.selectbox("Seleccionar Colección", colecciones_a_mostrar)

# Botón de consulta
if st.button("Consultar"):
    try:
        df = cargar_datos(coleccion_seleccionada)
        if not df.empty:
            st.dataframe(df)
            st.download_button(
                label="Descargar datos como CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f'{coleccion_seleccionada}.csv',
                mime='text/csv',
            )
        else:
            st.warning("La colección seleccionada no tiene datos.")
    except Exception as e:
        st.error(f"Error al consultar la colección: {e}")

# Cerrar la conexión
client.close()
