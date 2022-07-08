import base64

import streamlit as st
import math
from fpdf import FPDF
from PIL import Image
import numpy
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('logo_branco.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(80, 10, 'Relatório de Resultados', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')





def app():
    st.title('Matriz de Resultados')
    st.header('Tabela de Casos:')

    data = pd.DataFrame(columns=["Número de Poços","Capacidade da planta","VPL", "Risco"])

    def show_pdf(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # with every interaction, the script runs from top to bottom
    # resulting in the empty dataframe
    if 'data' in st.session_state:
        data = st.session_state['data']
        data.index.rename('foo', inplace=True)
    else:
        data = pd.DataFrame(columns=["Número de Poços","Capacidade da planta","VPL","Risco"])
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

    if 'riskvar' in st.session_state:
        riskvar = st.session_state['riskvar']
    else:
        riskvar = None

    if 'wells' in st.session_state:
        wells = st.session_state['wells']
    else:
        wells = []

    if 'dfreservoir' in st.session_state:
        dfreservoir = st.session_state['dfreservoir']
    else:
        dfreservoir = pd.DataFrame(columns=wells, index=["IP", "Oil Production (bpd)","Psep (bar)","Pe (bar)","RGO (sm³/sm³)"])

    if st.button("Registrar caso"):
        # update dataframe state
        data2 = pd.DataFrame([[n,f'{str("{:.0f}".format(oilprodp))} STB/d',f'US${str("{:.0f}".format(vpl/1e6))} milhões',riskvar]], columns=['Número de Poços', 'Capacidade da planta', 'VPL','Risco'])
        datafinal = pd.concat([data,data2],ignore_index=True)

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis('tight')
        ax.axis('off')
        the_table = ax.table(cellText=dfreservoir.values, colLabels=dfreservoir.columns, loc='center')
        plt.savefig('table.png', dpi=200, bbox_inches='tight')

        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)

        pdf.cell(0, 10, 'Resultados de Reservatório e Escoamento:', 0, 1)
        pdf.image('table.png', x=None, y=None, w=200, h=100, type='', link='')
        pdf.output('Relatório - Caso X.pdf', 'F')
        #show_pdf('Relatório - Caso X.pdf')

        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state['data'] = datafinal
        st.dataframe(datafinal)





















