import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd
from persist import persist, load_widget_state

def app():
    st.title('Poços')
    st.header('Dados de Entrada:')

    if 'n' in st.session_state:
        n = st.session_state['n']
    else:
        n = 1

    cols = st.columns(n)
    depth = []
    completion = []
    config = []
    horizont = []
    Woptions = ["Vertical", "Direcional"]

    for i, x in enumerate(cols):
        depth.append(st.number_input(f'Profundidade da cabeça do Poço {i+1}:', 0, 20000, 300))
        completion.append(st.number_input(f'Profundidado do canhoneado do Poço {i+1}:', 0, 50000, 2000))
        optselect = st.radio(f'Configuração do Poço {i + 1}:', Woptions)
        config.append(optselect)
        if (optselect == "Direcional"):
            horizont.append(st.number_input(f'Deslocamento horizontal do Poço {i + 1}:', 0, 50000, 600))

    button = st.button('Dimensionar Poços')

    if (button):

        for i in range(0,n,1):
            st.markdown(f"Diagrama do Poço {i+1}:")
            if (config[i] == "Vertical"):
                image = Image.open('Vertical.png')
                st.image(image)
            else:
                image = Image.open('Direcional.png')
                st.image(image)

        capexp = n * 300 * 1e6
        st.write(f'O CAPEX Total para os poços é de {(capexp/1e6)} milhões de dólares.')















