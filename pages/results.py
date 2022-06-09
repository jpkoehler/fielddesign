import base64

import streamlit as st
import math
from PIL import Image
import numpy
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


def app():
    st.title('Matriz de Resultados')
    st.header('Tabela de Casos:')

    data = pd.DataFrame(columns=["Caso","Número de Poços","Capacidade da planta","VPL"])

    # with every interaction, the script runs from top to bottom
    # resulting in the empty dataframe
    if 'data' in st.session_state:
        data = st.session_state['data']
        data.index.rename('foo', inplace=True)
    else:
        data = pd.DataFrame(columns=["Caso","Número de Poços","Capacidade da planta","VPL"])
        data.index.rename('foo', inplace=True)

    if 'n' in st.session_state:
        n = st.session_state['n']
    else:
        n = None

    if 'oilprodp' in st.session_state:
        oilprodp = st.session_state['oilprodp']
    else:
        oilprodp = None

    if 'vpl' in st.session_state:
        vpl = st.session_state['vpl']
    else:
        vpl = None

    if st.button("Registrar caso"):
        # update dataframe state
        row2 = [1,n,oilprodp,vpl]
        data2 = pd.DataFrame([[1,n,oilprodp,vpl]], columns=['Caso', 'Número de Poços', 'Capacidade da planta', 'VPL'])
        datafinal = pd.concat([data,data2],ignore_index=True)
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state['data'] = datafinal
        st.dataframe(datafinal)





















