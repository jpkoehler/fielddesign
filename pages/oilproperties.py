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
        api = 25

    api = st.number_input('Grau API do óleo:', 1, 1000000, api)
    st.session_state['api'] = api

    if st.button('Salvar'):
        st.success("Salvo com sucesso!")






















