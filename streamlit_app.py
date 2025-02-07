import streamlit as st
import pandas as pd
from pymongo import MongoClient

st.set_page_config(layout="wide")

# Conexión a MongoDB
client = MongoClient("mongodb://137.184.143.185:27017/?directConnection=true")
db = client["CRM"]

# Función para cargar datos con caché
@st.cache_data
def cargar_datos(coleccion_nombre, limit=0):
    coleccion = db[coleccion_nombre]
    datos = list(coleccion.find().limit(limit))
    return pd.DataFrame(datos)

# Título de la aplicación
st.title("Consulta de Colecciones CRM")

# Colecciones a mostrar
colecciones_a_mostrar = ["Actualizacion", "Demograficos"]

# Selector de colección
coleccion_seleccionada = st.selectbox("Seleccionar Colección", colecciones_a_mostrar)

# Obtener los datos únicos para los filtros
if coleccion_seleccionada == "Actualizacion":
    columna_filtro_1 = "Info_Carpeta_Archivo_x"
    columna_filtro_2 = "Numero Traslado"  # Nuevo filtro para "Actualizacion"
elif coleccion_seleccionada == "Demograficos":
    columna_filtro_1 = "Info_Carpeta_Archivo"
    columna_filtro_2 = "estado"  # Nuevo filtro para "Demograficos"

df_filtro = cargar_datos(coleccion_seleccionada)

print(df_filtro.columns)  # Imprime los nombres de las columnas para verificar
print(df_filtro.head())    # Imprime las primeras filas para inspeccionar los datos
print(df_filtro.info())    # Imprime información sobre el DataFrame

# Solución al KeyError: verifica si la columna existe antes de acceder a ella
valores_unicos_2 = df_filtro.get(columna_filtro_2).unique().tolist() if columna_filtro_2 in df_filtro.columns else []
valores_unicos_1 = df_filtro[columna_filtro_1].unique().tolist() if columna_filtro_1 in df_filtro.columns else []

# Filtros
filtro_seleccionado_1 = st.multiselect("Filtrar por " + columna_filtro_1, valores_unicos_1)
filtro_seleccionado_2 = st.multiselect("Filtrar por " + columna_filtro_2, valores_unicos_2)  # Nuevo filtro

# Botón de consulta
if st.button("Consultar"):
    try:
        # Aplicar los filtros
        if filtro_seleccionado_1 and filtro_seleccionado_2:
            df_filtrado = df_filtro[
                (df_filtro[columna_filtro_1].isin(filtro_seleccionado_1)) &
                (df_filtro[columna_filtro_2].isin(filtro_seleccionado_2))
            ]
        elif filtro_seleccionado_1:
            df_filtrado = df_filtro[df_filtro[columna_filtro_1].isin(filtro_seleccionado_1)]
        elif filtro_seleccionado_2:
            df_filtrado = df_filtro[df_filtro[columna_filtro_2].isin(filtro_seleccionado_2)]
        else:
            df_filtrado = df_filtro.copy()  # Mostrar todos los datos si no se selecciona filtro

        if not df_filtrado.empty:
            # Mostrar una muestra de los datos
            st.dataframe(df_filtrado.head(1000).style.set_properties(**{'width': '100%'}))  # Muestra las primeras 1000 filas

            # Botón de descarga con delimitador "|" (descarga los datos filtrados completos)
            st.download_button(
                label="Descargar datos filtrados como CSV",
                data=df_filtrado.to_csv(index=False, sep='|').encode('utf-8'),
                file_name=f'{coleccion_seleccionada}_filtrado.csv',
                mime='text/csv',
            )
        else:
            st.warning("No se encontraron datos con los filtros seleccionados.")
    except Exception as e:
        st.error(f"Error al consultar la colección: {e}")

# Cerrar la conexión
client.close()
