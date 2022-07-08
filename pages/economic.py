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
    st.title('Análise Econômica')
    st.header('Dados de entrada:')

    if 'n' in st.session_state:
        n = st.session_state['n']
    else:
        n = 1

    if 'oilprodp' in st.session_state:
        oilprodp = st.session_state['oilprodp']
    else:
        oilprodp = 15000

    if 'tp' in st.session_state:
        tp = st.session_state['tp']
    else:
        tp = 8000

    econpd = pd.DataFrame(columns=["VPN (Barris)","Capex do Navio","Capex dos Poços", "Capex do Subsea","VPL"])

    # with every interaction, the script runs from top to bottom
    # resulting in the empty dataframe
    if 'econpd' in st.session_state:
        econpd = st.session_state['econpd']
    else:
        econpd = pd.DataFrame(columns=["VPN (Barris)","Capex do Navio","Capex dos Poços", "Capex do Subsea","VPL"])


    i = st.number_input('Taxa Mínima de Atratividade (%)',0.0,1.0,0.09,0.01)
    T = st.number_input('CSLL e IRPJ (%)', 0.0, 1.0, 0.35,0.01)
    R = st.number_input('Royalties (%)', 0.0, 1.0, 0.10,0.01)
    p = st.number_input('Preço do Barril de Óleo (US$)', 0.0, 5000.0, 50.0,1.0)
    tf = 10950  # dias
    b = 0.2 / 365


    if st.button("Confirmar"):
        # update dataframe state

        vpn = oilprodp * 365 * (((1 - numpy.exp(-i * tp)) / i) + (
                ((numpy.exp(-i * tp)) - (numpy.exp((-(b + i) * tf) + b * tp))) / (b + i)))

        capexn = oilprodp * 1e4
        capexp = n * 300 * 1e6
        capexs = n * 150 * 1e6

        vpl = ((1 - R) * (1 - T) * (vpn * p)) - capexn - capexp - capexs

        econpd = pd.DataFrame([[f'{str("{:.0f}".format(vpn/1e6))} milhões', f'US${str("{:.0f}".format(capexn/1e6))} milhões',f'US${str("{:.0f}".format(capexp/1e6))} milhões',f'US${str("{:.0f}".format(capexs/1e6))} milhões',f'US${str("{:.0f}".format(vpl/1e6))} milhões']], columns=["VPN (Barris)","Capex do Navio","Capex dos Poços", "Capex do Subsea","VPL"])
        st.dataframe(econpd)
        st.session_state['vpl'] = vpl






















