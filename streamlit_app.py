import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time
import logging

# Configuración de logging (se guarda en un archivo llamado 'app.log')
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

TIMEOUT = 10
MAX_REINTENTOS = 3

def esperar_elemento_clickeable(by, locator):
    return WebDriverWait(browser, TIMEOUT).until(EC.element_to_be_clickable((by, locator)))

def esperar_elemento_presente(by, locator):
    return WebDriverWait(browser, TIMEOUT).until(EC.presence_of_element_located((by, locator)))

def esperar_elemento_visible(by, locator):
    return WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((by, locator)))

def ejecutar_paso(descripcion, funcion, *args, **kwargs):
    for intento in range(MAX_REINTENTOS):
        try:
            logging.info(f"Intentando: {descripcion} (Intento {intento+1}/{MAX_REINTENTOS})")
            resultado = funcion(*args, **kwargs)
            logging.info(f"Paso completado: {descripcion}")
            return resultado
        except Exception as e:
            logging.error(f"Error en el paso: {descripcion} - {e}")
            if intento < MAX_REINTENTOS - 1:
                time.sleep(5)
            else:
                raise

def descargar_informe(usuario, clave):
    """Función principal que contiene la lógica de Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1200")

    global browser  # Declarar browser como variable global
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        ejecutar_paso("Abrir navegador", browser.get, 
                      'https://novaventa.adminfo.net/smartplus/index.php?rtr=mantenimiento&ctr=autenticacion&acc=')

        ejecutar_paso("Ingresar usuario", esperar_elemento_presente, By.NAME, "usuario").send_keys(usuario)
        ejecutar_paso("Ingresar clave", esperar_elemento_presente, By.NAME, "clave").send_keys(clave)
        ejecutar_paso("Hacer clic en Login", esperar_elemento_clickeable, By.CLASS_NAME, "botonLogin").click()

        # ... (resto de los pasos de Selenium, usando ejecutar_paso como en el ejemplo anterior)

        st.success("Informe descargado exitosamente.")
        logging.info("Informe descargado exitosamente.")

    except Exception as e:
        st.error(f"Error al descargar el informe: {e}")
        logging.exception("Error al descargar el informe:")
    finally:
        browser.quit()

# Interfaz de Streamlit
st.title("Descarga de Informe Novaventa")

usuario = st.text_input("Usuario")
clave = st.text_input("Clave", type="password")

if st.button("Descargar Informe"):
    if usuario and clave:
        descargar_informe(usuario, clave)
    else:
        st.warning("Por favor, ingresa usuario y clave.")
