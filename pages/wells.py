import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


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
    Liftoptions = ["Nenhum", "Gaslift", "BCS"]

    for i, x in enumerate(cols):
        depth.append(st.number_input(f'Profundidade da cabeça do Poço {i+1}:', 0, 20000, 300))
        completion.append(st.number_input(f'Profundidado do canhoneado do Poço {i+1}:', 0, 50000, 2000))
        optselect = st.radio(f'Configuração do Poço {i + 1}:', Woptions)
        config.append(optselect)
        if (optselect == "Direcional"):
            horizont.append(st.number_input(f'Deslocamento horizontal do Poço {i + 1}:', 0, 50000, 600))
        with st.expander("Inserir detalhes"):
            st.write("Casing:")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.number_input(f"Profundidade Final {1+i}(m):", float(0), float(50000), float(2000),float(1.0))

            with col2:
                st.number_input(f"Diâmetro interno {1+i}(in):", float(0),float(50000), float(9.66),float(1.0))

            with col3:
                st.number_input(f"Diâmetro externo {1+i} (in):", float(0), float(50000), float(10.375),float(1.0))

            with col4:
                st.number_input(f"Rugosidade {1+i}(in):", float(0), float(50000), float(0.01),float(1.0))

            st.write("Tubing:")
            colt1, colt2, colt3, colt4 = st.columns(4)

            with colt1:
                st.number_input(f"Profundidade Final {1 + i}(m): ", float(0), float(50000), float(1980), float(1.0))

            with colt2:
                st.number_input(f"Diâmetro interno {1 + i}(in): ", float(0), float(50000), float(5.921), float(1.0))

            with colt3:
                st.number_input(f"Diâmetro externo {1 + i} (in): ", float(0), float(50000), float(6.625), float(1.0))

            with colt4:
                st.number_input(f"Rugosidade {1 + i}(in): ", float(0), float(50000), float(0.01), float(1.0))

            st.write("Packers:")
            coltt1, coltt2, coltt3 = st.columns(3)

            with coltt1:
                st.write("Packer 1")
                st.write("Packer 2")

            with coltt2:
                st.checkbox("Ativo",True,"keycheck1"+str(i))
                st.checkbox("Ativo",True,"keycheck2"+str(i))

            with coltt3:
                st.number_input(f"Profundidade {1 + i} (in): ", float(0), float(50000), float(1920), float(1.0))
                st.number_input(f"Profundidade {1 + i} (in):  ", float(0), float(50000), float(1920), float(1.0))

            liftselect = st.radio(f'Artificial Lift {i + 1}:', Liftoptions)

            if (liftselect == "Gaslift"):
                colttt1, colttt2, colttt3 = st.columns(3)

                with colttt1:
                    st.number_input(f"Profundidade {1 + i} (m): ", float(0), float(50000), float(620), float(1.0))

                with colttt2:
                    st.number_input(f"Quantidade de Injeção {1 + i} (SM³/d): ", float(0), float(50000), float(2000), float(1.0))

                with colttt3:
                    st.number_input(f"Diâmetro do Mandril {1 + i} (in): ", float(0), float(50000), float(2), float(1.0))

            if (liftselect == "BCS"):
                coltttt1, coltttt2, coltttt3 = st.columns(3)

                with coltttt1:
                    st.number_input(f"Profundidade {1 + i} (m): ", float(0), float(50000), float(620), float(1.0))

                with coltttt2:
                    st.number_input(f"Diâmetro {1 + i} (in): ", float(0), float(50000), float(5.5), float(1.0))

                with coltttt3:
                    st.number_input(f"Delta P {1 + i} (bar): ", float(0), float(50000), float(20), float(1.0))








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















