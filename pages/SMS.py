import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


def app():
    st.title('SMS - Saúde, Meio Ambiente e Segurança')
    st.header('Relatório de simulação de vazamento de Óleo:')

    st.text_area('Descrição:')

    st.write(
        f'<iframe src="https://spillmanager.riopetroleo.com/", width="800" height="800"></iframe>',
        unsafe_allow_html=True,
    )

















