import streamlit as st
import pandas as pd
import pyarrow.parquet as pq
import requests

st.set_page_config(
    page_title="MetaData",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

url_carteras = {
    "INVENTARIO": "https://docs.google.com/spreadsheets/d/187dwusJTD2uEMOFNQb8735wvbj2cVSbaE_MytHQYdU0/edit?gid=2086518071#gid=2086518071"
}

st.markdown("""
<div style='text-align: center; display: flex; align-items: center; justify-content: center;'>
    <h1 style='color: #005780; font-size: 40px;'>INVERSIONES JAY MORRIS SAS</h1>
    <img src='https://i0.wp.com/ijmsas.com/wp-content/uploads/2021/09/logo-ijm.png?resize=2048%2C2024&ssl=1' style='margin-left: 20px;' width='128' height='128'>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: #005780; font-size: 30px;'>INVENTARIOS</h1>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Promedios", "Existencias"])

def load_parquet(url):
    response = requests.get(url)
    with open('temp.parquet', 'wb') as f:
        f.write(response.content)
    df = pd.read_parquet('temp.parquet')
    return df

with tab1:
    st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>PROMEDIOS</h1></div>", unsafe_allow_html=True)
    cartera = st.selectbox('Selecciona una cartera:', list(url_carteras.keys()))
    if cartera:
        st.write(f"Tabla para {cartera}")
        df = load_parquet(url_carteras[cartera])
        st.dataframe(df)

with tab2:
    st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>EXISTENCIAS</h1></div>", unsafe_allow_html=True)
    st.write("Here you can add the logic for the 'Existencias' tab")
