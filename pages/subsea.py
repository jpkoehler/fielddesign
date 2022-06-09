import base64

import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd
from persist import persist, load_widget_state

def app():
    st.title('Subsea - Layout Submarino')
    st.header('Mapeamento de poços:')

    st.write(
        f'<iframe src="https://spillmanager.riopetroleo.com/", width="800" height="800"></iframe>',
        unsafe_allow_html=True,
    )
















