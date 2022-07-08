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
    st.title('Análise de Risco')
    st.header('Inserção de pontos de atenção:')

    riskpd = pd.DataFrame(columns=["Risco","Comentário"])

    # with every interaction, the script runs from top to bottom
    # resulting in the empty dataframe
    if 'riskpd' in st.session_state:
        riskpd = st.session_state['riskpd']
    else:
        riskpd = pd.DataFrame(columns=["Risco","Comentário"])

    if 'riskvar' in st.session_state:
        riskvar = st.session_state['riskvar']
    else:
        riskvar = 0

    if 'risktext' in st.session_state:
        risktext = st.session_state['risktext']
    else:
        risktext = ""

    riskno = st.number_input('Nível de Risco',1,10,1)
    risktext = st.text_input('Comentário',risktext)


    if st.button("Registrar"):
        # update dataframe state
        riskpd2 = pd.DataFrame([[riskno,risktext]], columns=['Risco', 'Comentário'])
        datafinal = pd.concat([riskpd,riskpd2],ignore_index=True)
        riskvar = riskvar + riskno
        st.session_state['riskpd'] = datafinal
        st.session_state['riskvar'] = riskvar
        st.dataframe(datafinal)





















