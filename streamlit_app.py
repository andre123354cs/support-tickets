import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MetaData",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

gsheetid = '187dwusJTD2uEMOFNQb8735wvbj2cVSbaE_MytHQYdU0'
sheetod = '2086518071'
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetod}&format'
dfDatos = pd.read_csv(url)

tab1, tab2 = st.tabs(["Promedios", "Existencias"])

with tab1:
    st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>PROMEDIOS</h1></div>", unsafe_allow_html=True)
    st.dataframe(dfDatos)

    autonumerico_values = dfDatos['autonumerico'].unique()
    selected_value = st.selectbox('Selecciona un valor de autonumerico:', autonumerico_values)
    
    filtered_df = dfDatos[dfDatos['autonumerico'] == selected_value]
    st.dataframe(filtered_df)

with tab2:
    st.markdown("<div style='text-align: center;'><h1 style='color: #005780; font-size: 30px;'>EXISTENCIAS</h1></div>", unsafe_allow_html=True)
    st.write("Here you can add the logic for the 'Existencias' tab")



