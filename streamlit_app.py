from pymongo import MongoClient
import pandas as pd
import streamlit as st

# Conexión a la base de datos
def connect_to_mongo():
    # Cambia por tu URL y base de datos
    client = MongoClient("mongodb://137.184.143.185:27017?directConnection=true")
    db = client["Metadata"]
    collection = db["Comfama"]
    return collection

# Leer documentos de MongoDB y cargar en un DataFrame
def read_mongo_to_dataframe(filter={}):
    collection = connect_to_mongo()
    documents = collection.find(filter)
    df = pd.DataFrame(documents)
    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)
    return df

df = read_mongo_to_dataframe()

# Ajustar DataFrame a Streamlit
st.title("Visualización de Datos de MongoDB en Streamlit")
st.dataframe(df)  # Eliminar los parámetros width y height para ajuste automático
