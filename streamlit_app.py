import streamlit as st
import pandas as pd
from pymongo import MongoClient

st.set_page_config(layout="wide")

# Conexión a MongoDB
client = MongoClient("mongodb://137.184.143.185:27017/?directConnection=true")
db = client["CRM"]

def cargar_datos(coleccion_nombre, limit=0):  # Limit 0 por defecto para traer todos los datos
    coleccion = db[coleccion_nombre]
    datos = list(coleccion.find().limit(limit))
    return pd.DataFrame(datos)

# Título de la aplicación
st.title("Consulta de Colecciones CRM")

# Colecciones a mostrar
colecciones_a_mostrar = ["Actualizacion", "Demograficos"]

# Selector de colección
coleccion_seleccionada = st.selectbox("Seleccionar Colección", colecciones_a_mostrar)

# Obtener los datos únicos para el filtro
if coleccion_seleccionada == "Actualizacion":
    columna_filtro = "Info_Carpeta_Archivo_x"
elif coleccion_seleccionada == "Demograficos":
    columna_filtro = "Info_Carpeta_Archivo"

df_filtro = cargar_datos(coleccion_seleccionada)
valores_unicos = df_filtro[columna_filtro].unique().tolist()

# Filtro
filtro_seleccionado = st.multiselect("Filtrar por " + columna_filtro, valores_unicos)

# Botón de consulta
if st.button("Consultar"):
    try:
        # Aplicar el filtro
        if filtro_seleccionado:
            df_mostrar = df_filtro[df_filtro[columna_filtro].isin(filtro_seleccionado)]
        else:
            df_mostrar = df_filtro.copy()  # Mostrar todos los datos si no se selecciona filtro

        if not df_mostrar.empty:
            st.dataframe(df_mostrar.style.set_properties(**{'width': '100%'}))

            # Botón de descarga con delimitador "|" (descarga los datos filtrados)
            st.download_button(
                label="Descargar datos filtrados como CSV",
                data=df_mostrar.to_csv(index=False, sep='|').encode('utf-8'),
                file_name=f'{coleccion_seleccionada}_filtrado.csv',
                mime='text/csv',
            )
        else:
            st.warning("No se encontraron datos con los filtros seleccionados.")
    except Exception as e:
        st.error(f"Error al consultar la colección: {e}")

# Cerrar la conexión
client.close()
