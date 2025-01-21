import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import locale
import pyarrow.parquet as pq
import numpy as np

st.set_page_config(
    page_title="MetaData",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed"
    )


url_carteras = {
        "Comfama": r"https://drive.usercontent.google.com/u/0/uc?id=187dwusJTD2uEMOFNQb8735wvbj2cVSbaE_MytHQYdU0&export=download",
        "Azzorti": r"https://drive.usercontent.google.com/u/0/uc?id=1kxVQ7PvD9ueO8qqZdk9aZotYGVjiRq0Y&export=download",
        "Cueros": r"https://drive.usercontent.google.com/u/0/uc?id=1ffZu1qoNK5iBo7lSo8WbS1bKZRYaIbMK&export=download",
        "Keypagos" : r"https://drive.usercontent.google.com/u/0/uc?id=1zYX2uONwvxBolHPEl4pm3qVjFeTRXCrQ&export=download",
        "Linea Directa": r"https://drive.usercontent.google.com/u/0/uc?id=1ceYiVkmia5GvS1m0TYuv9tdQ00UjhP1A&export=download",
        "Nova Mexico": r"https://drive.usercontent.google.com/u/0/uc?id=1Z8UOXpetXRvDPala0rSzPlQh8tSwbvIA&export=download",
        "Nova_Colombia": r"https://drive.usercontent.google.com/u/0/uc?id=1EkGd1UbyuVpCK2yqDjrxzV1i6SLNi607&export=download",
        #"Dolce": r"https://drive.usercontent.google.com/u/0/uc?id=1Ew7xK8rjDGDA4jjkhQ_XGRfDuFzIG5e8&export=download",
    }


st.markdown(""" <div style='text-align: center; display: flex; align-items: center; justify-content: center;'> <h1 style='color: #005780; font-size: 40px;'>INVERSIONES JAY MORRIS SAS </h1> <img src='https://i0.wp.com/ijmsas.com/wp-content/uploads/2021/09/logo-ijm.png?resize=2048%2C2024&ssl=1' style='margin-left: 20px;' width='128' height='128'> </div> """, unsafe_allow_html=True)

st.markdown(""" <div style='text-align: center;'> <h1 style='color: #005780; font-size: 30px;'>INVENTARIOS</h1> </div> """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Promedios", "Existencias"]) # Contenido para la pestaña "Promedios" 

with tab1: 
    
        st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>PROMEDIOS</h1></div>", unsafe_allow_html=True) 
       
        cartera = st.selectbox('Selecciona una cartera:',list(url_carteras.keys()))

with tab2: 
        st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>EXISTENCIAS</h1></div>", unsafe_allow_html=True)
        
