import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd
from persist import persist, load_widget_state

def app():
    st.title('Planta de Processo')
    st.header('Dado de Entrada')

    if 'oilprodp' in st.session_state:
        oilprodp = st.session_state['oilprodp']
    else:
        oilprodp = 15000

    qprodp = st.number_input('Capacidade da planta (STB/d):', 1, 1000000, oilprodp)
    st.session_state['oilprodp'] = qprodp

    Psep = st.number_input('Pressão do separador (bar):', 1, 100, 10)
    Pexp = st.number_input('Pressão de exportação (bar):', 1, 500, 300)
    MM = st.number_input('Massa Molar do Gás (kg/kmol):', 1, 500, 25)
    ROl = st.number_input('Massa específica do líquido (kg/m³):', 1, 2000, 800)
    Tc = st.number_input('Temperatura crítica (K):', 1, 2000, 252)
    Pc = st.number_input('Pressão crítica (bar):', 1, 2000, 47)

    button = st.button('Dimensionar planta')
    #dividir por 2 , como trem precisa ser feito


    if (button):

        if 'n' in st.session_state:
            n = st.session_state['n']
        else:
            n = 1

        if 'prodtotal' in st.session_state:
            prodtotal = st.session_state['prodtotal']
        else:
            prodtotal = 100000

        if 'RGO' in st.session_state:
            RGO = st.session_state['RGO']
        else:
            RGO = 46

        oilprod0 = prodtotal
        tf = 10950  # dias
        i = 0.09  # anual
        b = 0.2 / 365
        T = 0.35
        R = 0.10
        p = 50

        day = [*range(0, 10951, 1)]

        tp = (1 / b) * ((oilprod0 / oilprodp) - 1)
        oilprodplateau1 = []
        oilprod = []

        for y in day:
            bsw = 1 - numpy.exp((-0.2 * y) / 365)
            oilprod.append((oilprod0 * (1 - bsw)))
            if y >= tp:
                qcalc = oilprodp * numpy.exp(-b * (y - tp))
                oilprodplateau1.append(qcalc)
            else:
                oilprodplateau1.append(oilprodp)

        fig, ax = plt.subplots()
        ax.plot(day, oilprod, label="Original")
        ax.plot(day, oilprodplateau1, label="Patamar")
        ax.legend()

        st.pyplot(fig)

        vpn = oilprodp * 365 * (((1 - numpy.exp(-i * tp)) / i) + (
                ((numpy.exp(-i * tp)) - (numpy.exp((-(b + i) * tf) + b * tp))) / (b + i)))

        capexn = oilprodp * 1e4
        capexp = n * 300 * 1e6
        capexs = n * 150 * 1e6

        vpl = ((1 - R) * (1 - T) * (vpn * p)) - capexn - capexp - capexs
        st.session_state['vpl'] = vpl
        st.write(f'O VPN é {vpn}')
        st.write(f'O CAPEX para o navio é {capexn}')
        st.write(f'O CAPEX para os poços é de {capexp}')
        st.write(f'O CAPEX para arranjo subsea é {capexs}')
        st.write(f'O VPL é {vpl}')




        ql = qprodp * 0.0001104861  #m³/min
        trtrifasico = 10
        trbifasico = 5
        treletro = 25
        Vtrifasico = 2*ql*trtrifasico
        Vbifasico = 2*ql*trbifasico
        Veletro = 2*ql*treletro
        Dtrifasico = (Vtrifasico / 3.14159265359) ** (1 / 3)
        Dbifasico = (Vbifasico / 3.14159265359) ** (1 / 3)
        Deletro = (Veletro / 3.14159265359) ** (1 / 3)
        Ltrifasico = Dtrifasico * 5
        Lbifasico = Dbifasico * 4
        Leletro = Deletro * 4
        Hflotador = Dtrifasico * 5
        ciclonumber = (math.ceil((qprodp * 0.006629)/5))/2
        flux = Image.open('fluxograma.png')
        st.image(flux)
        st.write("O diâmetro do separador trifásico é " + str(Dtrifasico) + " m")
        st.write("O comprimento do separador trifásico é " + str(Ltrifasico) + " m")
        st.write("O diâmetro dos separadores bifásicos é " + str(Dbifasico) + " m")
        st.write("O comprimento dos separadores bifásicos é " + str(Lbifasico) + " m")
        st.write("O diâmetro do separador eletrostático é " + str(Deletro) + " m")
        st.write("O comprimento do separador eletrostático é " + str(Leletro) + " m")
        st.write("O número de hidrociclones do separador trifásico são " + str(ciclonumber))

        gasprod = prodtotal * RGO
        razcomp = (Pexp/Psep) ** (1/3)

        #Knockout1
        T1 = 313.15  # K
        P1 = Psep

        Kint = 0.080
        R = 0.082205  # L atm/K mol

        # Cálculo de Z
        Tr = (T1 / Tc)
        Pr = (P1 / Pc)
        B0 = 0.083 - (0.422 / (Tr ** 1.6))
        B1 = 0.139 - (0.172 / (Tr ** 4.2))
        w = -1 - math.log(Pr, 10)
        Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

        # Cálculo de vmax
        ROg = ((P1 / 1.013) * MM) / (Z * R * T1)
        vmax = Kint * math.sqrt((ROl - ROg) / ROg)

        # Cálculo de Área e Diâmetro
        qv = gasprod * 0.0000018414 #m³/s
        Aknock1 = qv / vmax
        Dknock1 = 1 * math.sqrt((4 * Aknock1) / math.pi)
        st.write("Área do knockout é " + str(Aknock1) + " m²")
        st.write("Diâmetro do Knockout é " + str(Dknock1) + " m")

        #Compressor1
        Pcomp1 = Psep * razcomp
        nisen = 0.7
        npoli = 0.75
        nmec = 0.8
        R = 8.314  # KJ/KmolK
        K = 1.72  # Cp/Cv
        M = 7562.99  # Kmol/h AJUSTAR DEPOIS

        # Cálculo de Td
        Td1 = T1 * ((Pcomp1 / Psep) ** (((K - 1) / K) * (1 / npoli)))

        # Cálculo de Z
        Tr = (((T1 + Td1) / 2) * (1 / Tc))
        Pr = (((Psep + Pcomp1) / 2) * (1 / Pc))
        B0 = 0.083 - (0.422 / (Tr ** 1.6))
        B1 = 0.139 - (0.172 / (Tr ** 4.2))
        w = -1 - math.log(Pr, 10)
        Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

        # Cálculo de Hisen e Pot
        Hisen = Z * R * (K / (K - 1)) * T1 * (((Pcomp1 / Psep) ** ((K - 1) / K)) - 1)
        Pot1 = (Hisen * M) / (nisen * nmec * 3600)

        st.write("T de descarga é " + str(Td1) + " K")
        st.write("Potência do compressor é " + str(Pot1) + " KW")

        #Resfriador1
        Tci = 293.15  # K
        Tco = 303.15  # K
        Thi = Td1  # K
        Tho = 313.15  # K
        mc = None  # Kg/s
        mh = qv * ROg   # Kg/s

        Cpc = 4200  # J/KgCº
        Cph = 2352.2  # J/KgCº
        ROc = 1000  # Kg/m³
        MIc = 0.001  # Pas
        Kc = 0.6  # W/mK

        K = 20  # W/mK
        Hext = 400  # W/m²K
        Rfin = 0.0001  # m²K/W
        Rfext = 0.0006  # m²K/W
        Dext = 0.75  # in
        Thk = 1.65  # mm
        Q = None

        # Cálculo do calor requerido e Tco/mc
        if Tco == None:
            Q = mh * Cph * (Thi - Tho)
            Tco = (Q / (mc * Cpc)) + Tci
        elif mc == None:
            Q = mh * Cph * (Thi - Tho)
            mc = (Q / (Cpc * (Tco - Tci)))

        # Cálculo DeltaTLM
        DT1 = Thi - Tco
        DT2 = Tho - Tci
        DTLM = ((DT1 - DT2) / (math.log(DT1 / DT2)))

        # Cálculo do coeficiente do Hin
        Dext = Dext * 0.0254
        Din = Dext - Thk * 0.001
        At = (math.pi * (Din ** 2) / 4)
        Vc = (mc / ROc) / At
        Rec = (Din * Vc * ROc) / MIc
        Prc = (Cpc * MIc) / Kc
        Nuc = 0.023 * (Rec ** 0.8) * (Prc ** 0.3)
        Hin = (Nuc * Kc) / Din

        # Cálculo do U
        U = 1 / ((Dext / (Hin * Din)) + ((Rfin * Dext) / Din) + ((Dext * math.log(Dext / Din)) / (2 * K)) + Rfext + (
                    1 / Hext))

        # Cálculo da área de Troca Térmica
        Atroc1 = (Q / (DTLM * U)) * 1.1

        st.write("Área de troca térmica é " + str(Atroc1) + " m²")
        st.write("A carga térmica do resfriador é " + str(Q) + " W")


















