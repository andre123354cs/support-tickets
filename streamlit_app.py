import streamlit as st
import pandas as pd
import requests

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

tab1, tab2 = st.tabs(["Promedios", "Existencias"])

with tab1:
    st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>PROMEDIOS</h1></div>", unsafe_allow_html=True)
    
    gsheetid = '187dwusJTD2uEMOFNQb8735wvbj2cVSbaE_MytHQYdU0'
    sheetod = '2086518071'
    url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetod}&format'
    dfDatos = pd.read_csv(url)

    st.dataframe(dfDatos)

    search_value = st.text_input("Buscar en autonumerico:")
    if search_value:
        filtered_df = dfDatos[dfDatos['autonumerico'].astype(str).str.contains(search_value, case=False, na=False)]
        st.dataframe(filtered_df)

with tab2:
    st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>EXISTENCIAS</h1></div>", unsafe_allow_html=True)
    st.write("Aquí puedes agregar la lógica para la pestaña 'Existencias'")
