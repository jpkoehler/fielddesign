import base64

import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


def app():
    st.title('Subsea e Naval')
    st.header('Mapeamento de poços:')

    st.write(
        f'<iframe src="https://spillmanager.riopetroleo.com/mapaproto.html?a=0", width="800" height="800"></iframe>',
        unsafe_allow_html=True,
    )

    flowlineoptions = ["Flexível", "Rígida"]
    riseroptions = ["Flexível", "Rígida"]
    riserconfigs = ["Lazy Wave", "Catenária Livre"]

    flowlineselect = st.radio('Flowline:', flowlineoptions, key="flowline")
    riserselect = st.radio('Riser:', riseroptions, key="riser")
    riserconfigselect = st.radio('Configuração de Riser:', riserconfigs, key="riserconfig")

    if st.button("Gerar Arranjo Submarino"):
        st.success("Arranjo gerado com sucesso!")
        st.write("Layout Submarino:")
        bat1 = Image.open('subsealayout.jpeg')
        st.image(bat1)


















