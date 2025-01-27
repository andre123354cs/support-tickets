from pymongo import MongoClient
import pandas as pd
import streamlit as st

# Conexión a la base de datos
def connect_to_mongo():
    # Cambia por tu URL y base de datos
    client = MongoClient("mongodb://137.184.143.185:27017?directConnection=true")
    db = client["Metadata"]
    return db

# Leer documentos de MongoDB y cargar en un DataFrame
def read_mongo_to_dataframe(collection_name, filter={}):
    db = connect_to_mongo()
    collection = db[collection_name]
    documents = collection.find(filter)
    df = pd.DataFrame(documents)
    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)
    return df

# DataFrames para las dos colecciones
df_comfama = read_mongo_to_dataframe('Comfama')
df_cueros = read_mongo_to_dataframe('Cueros')

# Configurar la página de Streamlit
st.set_page_config(
    page_title="MetaData",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<div style='text-align: center; display: flex; align-items: center; justify-content: center;'>
    <h1 style='color: #005780; font-size: 40px;'>INVERSIONES JAY MORRIS SAS</h1>
    <img src='https://i0.wp.com/ijmsas.com/wp-content/uploads/2021/09/logo-ijm.png?resize=2048%2C2024&ssl=1' style='margin-left: 20px;' width='128' height='128'>
</div>
""", unsafe_allow_html=True)

# Crear pestañas
tab1, tab2 = st.tabs(["Comfama", "Cueros"])

with tab1:
    st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>COMFAMA</h1></div>", unsafe_allow_html=True)
    st.dataframe(df_comfama, use_container_width=True)

with tab2:
    st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>CUEROS</h1></div>", unsafe_allow_html=True)
    st.dataframe(df_cueros, use_container_width=True)

