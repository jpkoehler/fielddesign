import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd

def app():
    st.title('Propriedades do Óleo')
    st.header('Dados de Entrada:')

    if 'api' in st.session_state:
        api = st.session_state['api']
    else:
        api = 35

    api = st.number_input('Grau API do óleo:', 1, 1000000, api)
    st.session_state['api'] = api

    if st.button('Salvar'):
        st.success("Salvo com sucesso!")
        Telectro = (0.0012 * (api) ** 3 ) - (0.024 * (api) ** 2) - (6.6052 * (api)) + 237.72
        if (Telectro < 60):
            Telectro = 60
        st.session_state['Telectro'] = Telectro
        st.write('Temperatura do Separador Eletrostático'+Telectro)























