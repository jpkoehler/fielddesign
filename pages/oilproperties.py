import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd

def app():
    st.title('Características do Projeto')
    st.header('Projeto:')

    projoptions = ["Greenfield", "Brownfield", "Tieback"]
    uepoptions = ["FPSO Spread Mooring", "FPSO Turret", "SPAR","SS","TLP"]
    contratoptions = ["Própria","Afretada"]

    projselect = st.radio('Projeto:', projoptions, key="proj")
    uepselect = st.radio('Modelo de UEP:', uepoptions, key="uep")
    contratoselect = st.radio('Modelo de Contrato:', contratoptions, key="contrato")

    st.header('Características do Petróleo:')

    if 'api' in st.session_state:
        api = st.session_state['api']
    else:
        api = 35

    if 'MM' in st.session_state:
        MM = st.session_state['MM']
    else:
        MM = 25

    if 'ROl' in st.session_state:
        ROl = st.session_state['ROl']
    else:
        ROl = 800

    if 'Tc' in st.session_state:
        Tc = st.session_state['Tc']
    else:
        Tc = 252

    if 'Pc' in st.session_state:
        Pc = st.session_state['Pc']
    else:
        Pc = 47

    col1, col2 = st.columns(2)

    with col1:

        api = st.number_input('Grau API do óleo:', 1, 1000000, api)
        st.session_state['api'] = api

        MM = st.number_input('Massa Molar do Gás (kg/kmol):', 1, 500, MM)
        ROl = st.number_input('Massa específica do líquido (kg/m³):', 1, 2000, ROl)
        Tc = st.number_input('Temperatura crítica (K):', 1, 2000, Tc)
        Pc = st.number_input('Pressão crítica (bar):', 1, 2000, Pc)

    if st.button('Salvar'):
        st.success("Salvo com sucesso!")
        Teletro = (0.0012 * (api) ** 3 ) - (0.024 * (api) ** 2) - (6.6052 * (api)) + 237.72
        if (Teletro < 60):
            Teletro = 60
        st.session_state['Teletro'] = Teletro
























