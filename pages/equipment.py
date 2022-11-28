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
    st.title('Planta de Processo')
    st.header('Dado de Entrada')

    def show_pdf(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    if 'oilprodp' in st.session_state:
        oilprodp = st.session_state['oilprodp']
    else:
        oilprodp = 90000

    #if 'MM' in st.session_state:
    #    MM = st.session_state['MM']
    #else:
    #    MM = 25

    #if 'ROl' in st.session_state:
    #    ROl = st.session_state['ROl']
    #else:
    #    ROl = 800

    #if 'Tc' in st.session_state:
    #    Tc = st.session_state['Tc']
    #else:
    #    Tc = 252

    #if 'Pc' in st.session_state:
    #    Pc = st.session_state['Pc']
    #else:
    #    Pc = 47

    qprodp = st.number_input('Capacidade da planta (STB/d):', 1, 1000000, oilprodp)
    st.session_state['oilprodp'] = qprodp

    Psep = st.number_input('Pressão do separador (bar):', 1, 100, 10)
    Pexp = st.number_input('Pressão de exportação (bar):', 1, 1000, 300)
    C1 = st.number_input('Fração molar de C1:', 0, 1, 0.1)
    C2 = st.number_input('Fração molar de C2:', 0, 1, 0)
    C3 = st.number_input('Fração molar de C3:', 0, 1, 0)
    iC4 = st.number_input('Fração molar de i-C4:', 0, 1, 0)
    nC4 = st.number_input('Fração molar de n-C4:', 0, 1, 0)
    iC5 = st.number_input('Fração molar de i-C5:', 0, 1, 0)
    nC5 = st.number_input('Fração molar de n-C5:', 0, 1, 0)
    nC6 = st.number_input('Fração molar de n-C6:', 0, 1, 0)
    nC7 = st.number_input('Fração molar de n-C7:', 0, 1, 0)
    nC8 = st.number_input('Fração molar de n-C8:', 0, 1, 0)
    n2 = st.number_input('Fração molar de n2:', 0, 1, 0)
    co2 = st.number_input('Fração molar de CO2:', 0, 1, 0)
    h2s = st.number_input('Fração molar de H2S:', 0, 1, 0)
    h2o = st.number_input('Fração molar de H2O:', 0, 1, 0)
    #st.write("Processos adicionais:")
    #CO2 = st.checkbox("CO2")
    #H2S = st.checkbox("H2S")
    #lavagem = st.checkbox("Lavagem de óleo")

    button1 = st.button('Dimensionar planta')
    #dividir por 2 , como trem precisa ser feito
    if st.session_state.get('button1') != True:
        st.session_state['button1'] = button1

    if (button1):
        with st.spinner('Processando...'):
            time.sleep(2)
        st.success('Sucesso!')


    if st.session_state['button1'] == True:

        if 'n' in st.session_state:
            n = st.session_state['n']
        else:
            n = 1

        if 'prodtotal' in st.session_state:
            prodtotal = st.session_state['prodtotal']
        else:
            prodtotal = 130000

        if 'rgofinal' in st.session_state:
            RGO = st.session_state['rgofinal']
        else:
            RGO = 46

        if 'Teletro' in st.session_state:
            Teletro = st.session_state['Teletro']
        else:
            Teletro = 60

        oilprod0 = prodtotal
        MM = C1*16.04 + C2*30.07 + C3*44.1 + iC4*58.12 + nC4*58.12 + iC5*72.15 + nC5*72.15 + nC6*86.18 + nC7*100.21 + nC8*114.23 + n2*28.014 + co2*44.01 + h2s*34.1 + h2o*18.01
        Tc = C1*190.58 + C2*305.42 + C3*369.82 + iC4*408.14 + nC4*425.18 + iC5*692 + nC5*469.65 + nC6*507.43 + nC7*540.26 + nC8*568.83 + n2*126.10 + co2*304.19 + h2s*373.55 + h2o*647.13
        Pc = C1*46.04 + C2*48.80 + C3*42.49 + iC4*36.48 + nC4*37.97 + iC5*35.60 + nC5*33.69 + nC6*30.12 + nC7*27.36 + nC8*24.86 + n2*33.94 + co2*73.82 + h2s*90.08 + h2o*220.55
        ROl = 800
        tf = 10950  # dias
        i = 0.09  # anual
        b = 0.2 / 365
        T = 0.35
        R = 0.10
        p = 50

        day = [*range(0, 10951, 1)]

        tp = (1 / b) * ((oilprod0 / oilprodp) - 1)
        st.session_state['tp'] = tp
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

        #fig, ax = plt.subplots()
        #ax.plot(day, oilprod, label="Original")
        #ax.plot(day, oilprodplateau1, label="Patamar")
        #ax.legend()

        #st.pyplot(fig)

        vpn = oilprodp * 365 * (((1 - numpy.exp(-i * tp)) / i) + (
                ((numpy.exp(-i * tp)) - (numpy.exp((-(b + i) * tf) + b * tp))) / (b + i)))

        capexn = oilprodp * 1e4
        capexp = n * 300 * 1e6
        capexs = n * 150 * 1e6

        vpl = ((1 - R) * (1 - T) * (vpn * p)) - capexn - capexp - capexs
        st.session_state['vpl'] = vpl

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

        gasprod = oilprodp * RGO
        nestag = math.ceil(math.log(Pexp/Psep)/math.log(4))
        razcomp = (Pexp / Psep) ** (1 / nestag)

        if (nestag == 3):

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



            # Knockout2
            T2 = 313.15  # K
            P2 = Pcomp1

            Kint = 0.080
            R = 0.082205  # L atm/K mol

            # Cálculo de Z
            Tr = (T2 / Tc)
            Pr = (P2 / Pc)
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de vmax
            ROg = ((P2 / 1.013) * MM) / (Z * R * T2)
            vmax = Kint * math.sqrt((ROl - ROg) / ROg)

            # Cálculo de Área e Diâmetro
            qv = gasprod * 0.0000018414  # m³/s
            Aknock2 = qv / vmax
            Dknock2 = 1 * math.sqrt((4 * Aknock2) / math.pi)


            # Compressor2
            Pcomp2 = P2 * razcomp
            nisen = 0.7
            npoli = 0.75
            nmec = 0.8
            R = 8.314  # KJ/KmolK
            K = 1.72  # Cp/Cv
            M = 7562.99  # Kmol/h AJUSTAR DEPOIS

            # Cálculo de Td
            Td2 = T2 * ((Pcomp2 / Pcomp1) ** (((K - 1) / K) * (1 / npoli)))

            # Cálculo de Z
            Tr = (((T2 + Td2) / 2) * (1 / Tc))
            Pr = (((Pcomp1 + Pcomp2) / 2) * (1 / Pc))
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de Hisen e Pot
            Hisen = Z * R * (K / (K - 1)) * T2 * (((Pcomp2 / Pcomp1) ** ((K - 1) / K)) - 1)
            Pot2 = (Hisen * M) / (nisen * nmec * 3600)



            # Resfriador2
            Tci = 293.15  # K
            Tco = 303.15  # K
            Thi = Td2  # K
            Tho = 313.15  # K
            mc = None  # Kg/s
            mh = qv * ROg  # Kg/s

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
            Q2 = None

            # Cálculo do calor requerido e Tco/mc
            if Tco == None:
                Q2 = mh * Cph * (Thi - Tho)
                Tco = (Q2 / (mc * Cpc)) + Tci
            elif mc == None:
                Q2 = mh * Cph * (Thi - Tho)
                mc = (Q2 / (Cpc * (Tco - Tci)))

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
            U = 1 / ((Dext / (Hin * Din)) + ((Rfin * Dext) / Din) + (
                        (Dext * math.log(Dext / Din)) / (2 * K)) + Rfext + (
                             1 / Hext))

            # Cálculo da área de Troca Térmica
            Atroc2 = (Q2 / (DTLM * U)) * 1.1



            # Knockout3
            T3 = 313.15  # K
            P3 = Pcomp2

            Kint = 0.080
            R = 0.082205  # L atm/K mol

            # Cálculo de Z
            Tr = (T3 / Tc)
            Pr = (P3 / Pc)
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de vmax
            ROg = ((P3 / 1.013) * MM) / (Z * R * T3)
            vmax = Kint * math.sqrt((ROl - ROg) / ROg)

            # Cálculo de Área e Diâmetro
            qv = gasprod * 0.0000018414  # m³/s
            Aknock3 = qv / vmax
            Dknock3 = 1 * math.sqrt((4 * Aknock3) / math.pi)


            # Compressor3
            Pcomp3 = P3 * razcomp
            nisen = 0.7
            npoli = 0.75
            nmec = 0.8
            R = 8.314  # KJ/KmolK
            K = 1.72  # Cp/Cv
            M = 7562.99  # Kmol/h AJUSTAR DEPOIS

            # Cálculo de Td
            Td3 = T3 * ((Pcomp3 / Pcomp2) ** (((K - 1) / K) * (1 / npoli)))

            # Cálculo de Z
            Tr = (((T3 + Td3) / 2) * (1 / Tc))
            Pr = (((Pcomp3 + Pcomp2) / 2) * (1 / Pc))
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de Hisen e Pot
            Hisen = Z * R * (K / (K - 1)) * T3 * (((Pcomp3 / Pcomp2) ** ((K - 1) / K)) - 1)
            Pot3 = (Hisen * M) / (nisen * nmec * 3600)



            # Resfriador3
            Tci = 293.15  # K
            Tco = 303.15  # K
            Thi = Td3  # K
            Tho = 313.15  # K
            mc = None  # Kg/s
            mh = qv * ROg  # Kg/s

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
            Q3 = None

            # Cálculo do calor requerido e Tco/mc
            if Tco == None:
                Q3 = mh * Cph * (Thi - Tho)
                Tco = (Q3 / (mc * Cpc)) + Tci
            elif mc == None:
                Q3 = mh * Cph * (Thi - Tho)
                mc = (Q3 / (Cpc * (Tco - Tci)))

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
            U = 1 / ((Dext / (Hin * Din)) + ((Rfin * Dext) / Din) + (
                    (Dext * math.log(Dext / Din)) / (2 * K)) + Rfext + (
                             1 / Hext))

            # Cálculo da área de Troca Térmica
            Atroc3 = (Q3 / (DTLM * U)) * 1.1



        elif (nestag == 4):

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


            # Knockout2
            T2 = 313.15  # K
            P2 = Pcomp1

            Kint = 0.080
            R = 0.082205  # L atm/K mol

            # Cálculo de Z
            Tr = (T2 / Tc)
            Pr = (P2 / Pc)
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de vmax
            ROg = ((P2 / 1.013) * MM) / (Z * R * T2)
            vmax = Kint * math.sqrt((ROl - ROg) / ROg)

            # Cálculo de Área e Diâmetro
            qv = gasprod * 0.0000018414  # m³/s
            Aknock2 = qv / vmax
            Dknock2 = 1 * math.sqrt((4 * Aknock2) / math.pi)


            # Compressor2
            Pcomp2 = P2 * razcomp
            nisen = 0.7
            npoli = 0.75
            nmec = 0.8
            R = 8.314  # KJ/KmolK
            K = 1.72  # Cp/Cv
            M = 7562.99  # Kmol/h AJUSTAR DEPOIS

            # Cálculo de Td
            Td2 = T2 * ((Pcomp2 / Pcomp1) ** (((K - 1) / K) * (1 / npoli)))

            # Cálculo de Z
            Tr = (((T2 + Td2) / 2) * (1 / Tc))
            Pr = (((Pcomp1 + Pcomp2) / 2) * (1 / Pc))
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de Hisen e Pot
            Hisen = Z * R * (K / (K - 1)) * T2 * (((Pcomp2 / Pcomp1) ** ((K - 1) / K)) - 1)
            Pot2 = (Hisen * M) / (nisen * nmec * 3600)



            # Resfriador2
            Tci = 293.15  # K
            Tco = 303.15  # K
            Thi = Td2  # K
            Tho = 313.15  # K
            mc = None  # Kg/s
            mh = qv * ROg  # Kg/s

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
            Q2 = None

            # Cálculo do calor requerido e Tco/mc
            if Tco == None:
                Q2 = mh * Cph * (Thi - Tho)
                Tco = (Q2 / (mc * Cpc)) + Tci
            elif mc == None:
                Q2 = mh * Cph * (Thi - Tho)
                mc = (Q2 / (Cpc * (Tco - Tci)))

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
            U = 1 / ((Dext / (Hin * Din)) + ((Rfin * Dext) / Din) + (
                        (Dext * math.log(Dext / Din)) / (2 * K)) + Rfext + (
                             1 / Hext))

            # Cálculo da área de Troca Térmica
            Atroc2 = (Q2 / (DTLM * U)) * 1.1

            #st.write("Área de troca térmica do resfriador 2 é " + str("{:.0f}".format(Atroc2)) + " m².")
            #st.write("A carga térmica do resfriador 2 é " + str("{:.0f}".format(Q2)) + " W.")

            # Knockout3
            T3 = 313.15  # K
            P3 = Pcomp2

            Kint = 0.080
            R = 0.082205  # L atm/K mol

            # Cálculo de Z
            Tr = (T3 / Tc)
            Pr = (P3 / Pc)
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de vmax
            ROg = ((P3 / 1.013) * MM) / (Z * R * T3)
            vmax = Kint * math.sqrt((ROl - ROg) / ROg)

            # Cálculo de Área e Diâmetro
            qv = gasprod * 0.0000018414  # m³/s
            Aknock3 = qv / vmax
            Dknock3 = 1 * math.sqrt((4 * Aknock3) / math.pi)
            #st.write("Área do knockout 3 é " + str("{:.2f}".format(Aknock3)) + " m².")
            #st.write("Diâmetro do Knockout 3 é " + str("{:.2f}".format(Dknock3)) + " m.")

            # Compressor3
            Pcomp3 = P3 * razcomp
            nisen = 0.7
            npoli = 0.75
            nmec = 0.8
            R = 8.314  # KJ/KmolK
            K = 1.72  # Cp/Cv
            M = 7562.99  # Kmol/h AJUSTAR DEPOIS

            # Cálculo de Td
            Td3 = T3 * ((Pcomp3 / Pcomp2) ** (((K - 1) / K) * (1 / npoli)))

            # Cálculo de Z
            Tr = (((T3 + Td3) / 2) * (1 / Tc))
            Pr = (((Pcomp3 + Pcomp2) / 2) * (1 / Pc))
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de Hisen e Pot
            Hisen = Z * R * (K / (K - 1)) * T3 * (((Pcomp3 / Pcomp2) ** ((K - 1) / K)) - 1)
            Pot3 = (Hisen * M) / (nisen * nmec * 3600)

            #st.write("T de descarga do compressor 3 é " + str("{:.0f}".format(Td3)) + " K.")
            #st.write("Potência do compressor 3 é " + str("{:.0f}".format(Pot3)) + " KW.")

            # Resfriador3
            Tci = 293.15  # K
            Tco = 303.15  # K
            Thi = Td3  # K
            Tho = 313.15  # K
            mc = None  # Kg/s
            mh = qv * ROg  # Kg/s

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
            Q3 = None

            # Cálculo do calor requerido e Tco/mc
            if Tco == None:
                Q3 = mh * Cph * (Thi - Tho)
                Tco = (Q3 / (mc * Cpc)) + Tci
            elif mc == None:
                Q3 = mh * Cph * (Thi - Tho)
                mc = (Q3 / (Cpc * (Tco - Tci)))

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
            U = 1 / ((Dext / (Hin * Din)) + ((Rfin * Dext) / Din) + (
                    (Dext * math.log(Dext / Din)) / (2 * K)) + Rfext + (
                             1 / Hext))

            # Cálculo da área de Troca Térmica
            Atroc3 = (Q3 / (DTLM * U)) * 1.1



            # Knockout4
            T4 = 313.15  # K
            P4 = Pcomp3

            Kint = 0.080
            R = 0.082205  # L atm/K mol

            # Cálculo de Z
            Tr = (T4 / Tc)
            Pr = (P4 / Pc)
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de vmax
            ROg = ((P4 / 1.013) * MM) / (Z * R * T4)
            vmax = Kint * math.sqrt((ROl - ROg) / ROg)

            # Cálculo de Área e Diâmetro
            qv = gasprod * 0.0000018414  # m³/s
            Aknock4 = qv / vmax
            Dknock4 = 1 * math.sqrt((4 * Aknock4) / math.pi)


            # Compressor4
            Pcomp4 = P4 * razcomp
            nisen = 0.7
            npoli = 0.75
            nmec = 0.8
            R = 8.314  # KJ/KmolK
            K = 1.72  # Cp/Cv
            M = 7562.99  # Kmol/h AJUSTAR DEPOIS

            # Cálculo de Td
            Td4 = T4 * ((Pcomp4 / Pcomp3) ** (((K - 1) / K) * (1 / npoli)))

            # Cálculo de Z
            Tr = (((T4 + Td4) / 2) * (1 / Tc))
            Pr = (((Pcomp4 + Pcomp3) / 2) * (1 / Pc))
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)

            # Cálculo de Hisen e Pot
            Hisen = Z * R * (K / (K - 1)) * T3 * (((Pcomp4 / Pcomp3) ** ((K - 1) / K)) - 1)
            Pot4 = (Hisen * M) / (nisen * nmec * 3600)



            # Resfriador4
            Tci = 293.15  # K
            Tco = 303.15  # K
            Thi = Td4  # K
            Tho = 313.15  # K
            mc = None  # Kg/s
            mh = qv * ROg  # Kg/s

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
            Q4 = None

            # Cálculo do calor requerido e Tco/mc
            if Tco == None:
                Q4 = mh * Cph * (Thi - Tho)
                Tco = (Q4 / (mc * Cpc)) + Tci
            elif mc == None:
                Q4 = mh * Cph * (Thi - Tho)
                mc = (Q4 / (Cpc * (Tco - Tci)))

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
            U = 1 / ((Dext / (Hin * Din)) + ((Rfin * Dext) / Din) + (
                    (Dext * math.log(Dext / Din)) / (2 * K)) + Rfext + (
                             1 / Hext))

            # Cálculo da área de Troca Térmica
            Atroc4 = (Q4 / (DTLM * U)) * 1.1


        Ttrifasico =30
        Tbifasico = Teletro
        Tflotador = 25

        #datasep = pd.DataFrame(
        #   [["Separador Trifásico", str("{:.2f}".format(Ltrifasico)), str("{:.2f}".format(Dtrifasico)),str("{:.0f}".format(Ttrifasico))],
        #    ["Separador Bifásico", str("{:.2f}".format(Lbifasico)), str("{:.2f}".format(Dbifasico)),str("{:.0f}".format(Tbifasico))],
        #    ["Tratador Eletrostático", str("{:.2f}".format(Leletro)), str("{:.2f}".format(Deletro)),str("{:.0f}".format(Teletro))],
        #    ["Flotador", str("{:.2f}".format(Hflotador)), str("{:.2f}".format(Dtrifasico)),str("{:.0f}".format(Tflotador))]],
        #   columns=['Equipamento', 'Comprimento (m)', 'Diâmetro (m)','Temperatura (°C)'])
        #st.table(datasep)

        dataknock = pd.DataFrame(
            [["Vaso de Knockout 1", str("{:.2f}".format(Aknock1)), str("{:.2f}".format(Dknock1))], ["Vaso de Knockout 2", str("{:.2f}".format(Aknock2)), str("{:.2f}".format(Dknock2))],
             ["Vaso de Knockout 3", str("{:.2f}".format(Aknock3)), str("{:.2f}".format(Dknock3))]],
            columns=['Equipamento', 'Área (m²)', 'Diâmetro (m)'])
        st.table(dataknock)

        datacomp = pd.DataFrame(
            [["Compressor 1", str("{:.2f}".format(Pot1))], ["Compressor 2", str("{:.2f}".format(Pot2))],
             ["Compressor 3", str("{:.2f}".format(Pot3))]],
            columns=['Equipamento', 'Potência (KW)'])
        st.table(datacomp)

        dataresf = pd.DataFrame(
            [["Resfriador 1", str("{:.2f}".format(Q/1e6)), str("{:.2f}".format(Atroc1))], ["Resfriador 2", str("{:.2f}".format(Q2/1e6)), str("{:.2f}".format(Atroc2))],
             ["Resfriador 3", str("{:.2f}".format(Q3/1e6)), str("{:.2f}".format(Atroc3))]],
            columns=['Equipamento',"Carga Térmica (MW)", 'Área de Troca Térmica (m²)'])
        st.table(dataresf)

        #dataciclo = pd.DataFrame(
        #     [["Hidrociclone do Separador Trifásico", str("{:.2f}".format(42)), str("{:.2f}".format(2)),str("{:.0f}".format(ciclonumber))],
        #      ["Hidrociclone do Separador Eletrostático", str("{:.2f}".format(42)), str("{:.2f}".format(2)),str("{:.0f}".format(ciclonumber))]],
        #     columns=['Equipamento', "Diâmetro (m)", 'Comprimento (m)',"Quantidade"])
        #st.table(dataciclo)

        #if (CO2 == True):
        #    flux = Image.open('fluxograma3.png')
        #    st.image(flux)
        #else:
        #    flux = Image.open('fluxograma.png')
        #    st.image(flux)




        #if st.button('Abrir Separador de Teste'):
        #    flux = Image.open('fluxogramapfd-1.png')
        #    st.image(flux)
        #if st.button('Abrir Cooler de Gás Separado'):
        #    flux = Image.open('fluxogramapfd-1.png')
        #    st.image(flux)
        #if st.button('Abrir Estágios de Compressão'):
        #    flux = Image.open('compstages-1.png')
        #    st.image(flux)
        #if st.button('Abrir Controle de Compressor'):
        #    flux = Image.open('compcontrol-1.png')
        #    st.image(flux)
        #if st.button('Abrir Compressão Principal'):
        #    flux = Image.open('maingascomp-1.png')
        #    st.image(flux)
        #if st.button('Abrir Compressor de Exportação'):
        #    flux = Image.open('exporgascomp-1.png')
        #    st.image(flux)
        #if st.button('Abrir Coalescedor'):
        #    flux = Image.open('coalescent-1.png')
        #    st.image(flux)
        #if st.button('Abrir Sistema de Tratamento de Gás'):
        #    flux = Image.open('gasdesid-1.png')
        #    st.image(flux)
        #if st.button('Abrir Hidrociclone'):
        #    flux = Image.open('hidrociclone-1.png')
        #    st.image(flux)








