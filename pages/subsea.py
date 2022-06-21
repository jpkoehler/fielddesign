import base64

import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


def app():
    st.title('Subsea - Layout Submarino')
    st.header('Mapeamento de poços:')

    st.write(
        f'<iframe src="https://spillmanager.riopetroleo.com/mapaproto.html", width="800" height="800"></iframe>',
        unsafe_allow_html=True,
    )

    if st.button("Registrar Batimetria"):
        st.success("Batimetria registrada com sucesso!")
        st.write("Batimetria da Flowline 1:")
        bat1 = Image.open('Batimetria1.png')
        st.image(bat1)
        st.write("Batimetria da Flowline 2:")
        bat2 = Image.open('Batimetria2.png')
        st.image(bat2)
        st.write("Batimetria da Flowline 3:")
        bat3 = Image.open('Batimetria3.png')
        st.image(bat3)

















