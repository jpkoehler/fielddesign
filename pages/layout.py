import base64
import time

import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


def app():
    st.title('Planta de Processo - Arranjo')
    fpso = Image.open('FPSO.png')
    st.image(fpso)

    def show_pdf(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    button1 = st.button('Gerar diagramas')
    if st.session_state.get('button') != True:
        st.session_state['button'] = button1

    if button1:
        with st.spinner('Processando...'):
            time.sleep(1)
        st.success('Sucesso!')

    if st.session_state['button'] == True:

        st.header('Diagramas gerados:')

        if st.button('Abrir Arranjo Geral'):
            show_pdf('I-DE-3010.90-1200-942-PPC-001_G - Arranjo Geral.pdf')
        if st.button('Abrir Laboratório 1'):
            show_pdf('I-DE-3010.90-1350-190-PPC-001_A_P001 - Laboratório.pdf')
        if st.button('Abrir Laboratório 2'):
            show_pdf('I-DE-3010.90-1350-190-PPC-001_A_P002 - Laboratório.pdf')
        if st.button('Riser Balcony'):
            show_pdf('I-DE-3010.90-1350-942-PPC-001_B - Riser Balcony.pdf')
        if st.button('Abrir Compressão de CO2 1'):
            show_pdf('I-DE-3010.90-1411-942-PPC-002_D - Compressão de CO2.pdf')
        if st.button('Abrir Compressão de CO2 2'):
            show_pdf('I-DE-3010.90-1411-942-PPC-102_A - Compressão de CO2.pdf')
        if st.button('Abrir Sistema de Flare'):
            show_pdf('I-DE-3010.90-1412-942-PPC-001_B - Sistema de Flare.pdf')
        if st.button('Abrir Remoção de CO2'):
            show_pdf('I-DE-3010.90-1413-942-PPC-002_B - Remoção de CO2.pdf')
        if st.button('Abrir Compressão de Gás de Exportação 1'):
            show_pdf('I-DE-3010.90-1414-942-PPC-002_C - Compressão de Gás de Exportação.pdf')
        if st.button('Abrir Compressão de Gás de Exportação 2'):
            show_pdf('I-DE-3010.90-1414-942-PPC-102_A - Compressão de Gás de Exportação.pdf')
        if st.button('Abrir Desidratação de Gás e Gás Combustível'):
            show_pdf('I-DE-3010.90-1415-942-PPC-001_C - Desidratação de Gás e Gás Combustível.pdf')
        if st.button('Abrir Compressão Principal'):
            show_pdf('arranjocompleto.pdf')
        if st.button('Abrir Injeção de Gás'):
            show_pdf('I-DE-3010.90-1417-942-PPC-001_B - Injeção de Gás.pdf')
        if st.button('Abrir Tratamento de Óleo'):
            show_pdf('I-DE-3010.90-1418-942-PPC-001_B - Tratamento de Óleo.pdf')
        if st.button('Abrir Lançadores e Recebedores de PIG'):
            show_pdf('I-DE-3010.90-1419-942-PPC-001_B - Lançadores e Recebedores de PIG.pdf')
        if st.button('Abrir Processamento de Óleo e Tratamento de Água Produzida'):
            show_pdf('I-DE-3010.90-1421-942-PPC-001_C - Processamento de Óleo e Tratamento de Água Produzida.pdf')
        if st.button('Abrir Injeção de Água e Remoção de Sulfato'):
            show_pdf('I-DE-3010.90-1422-942-PPC-001_B - Injeção de Água e Remoção de Sulfato.pdf')
        if st.button('Abrir Utilidades'):
            show_pdf('I-DE-3010.90-1423-942-PPC-001_B - Utilidades.pdf')
        if st.button('Abrir Automação e Elétrica'):
            show_pdf('I-DE-3010.90-1424-942-PPC-001_B - Automação e Elétrica.pdf')
        if st.button('Abrir Armazenamento de Químicos e Laydown'):
            show_pdf('I-DE-3010.90-1425-942-PPC-001_B - Armazenamento de Químicos e Laydown.pdf')
        if st.button('Abrir Geração de Energia 1'):
            show_pdf('I-DE-3010.90-1426-942-PPC-001_B - Geração de Energia.pdf')
        if st.button('Abrir Geração de Energia 2'):
            show_pdf('I-DE-3010.90-1427-942-PPC-001_B - Geração de Energia.pdf')




























