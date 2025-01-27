from pymongo import MongoClient
import pandas as pd
import streamlit as st

# Conexión a la base de datos
def connect_to_mongo():
    # Cambia por tu URL y base de datos
    client = MongoClient("mongodb://137.184.143.185:27017?directConnection=true")
    db = client["Metadata"]  # Cambia por el nombre de tu base de datos
    collection = db["Metadata"]  # Cambia por el nombre de tu colección
    return collection

# Leer documentos de MongoDB y cargar en un DataFrame
def read_mongo_to_dataframe(filter={}):
    collection = connect_to_mongo()
    # Leer todos los documentos que coincidan con el filtro
    documents = collection.find(filter)
    
    # Convertir los documentos en un DataFrame
    df = pd.DataFrame(documents)
    
    # Eliminar el campo '_id' que MongoDB agrega por defecto, si no lo necesitas
    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)
    
    return df

df = read_mongo_to_dataframe()

# Configuración de Streamlit
st.title("Visualización de datos de MongoDB")
tabs = st.tabs(["Tabla", "Descripción", "Filtro"])

with tabs[0]:
    st.header("Tabla de datos")
    st.dataframe(df)

with tabs[1]:
    st.header("Descripción de datos")
    st.write(df.describe())

with tabs[2]:
    st.header("Filtrar datos")
    column = st.selectbox("Selecciona una columna", df.columns)
    value = st.text_input("Introduce un valor para filtrar")
    if value:
        filtered_df = df[df[column].astype(str).str.contains(value)]
        st.dataframe(filtered_df)
