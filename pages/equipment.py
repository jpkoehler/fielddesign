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
    st.header('Dados de Entrada')

    def show_pdf(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    if 'oilprodp' in st.session_state:
        oilprodp = st.session_state['oilprodp']
    else:
        oilprodp = 100000
        
    if 'rgofinal' in st.session_state:
        RGO = st.session_state['rgofinal']
    else:
        RGO = 50



    qprodp = st.number_input('Capacidade da planta (STB/d):', 1, 1000000, oilprodp)
    st.session_state['oilprodp'] = qprodp
    
    RGO = st.number_input('RGO:', 1, 200, 50)
    st.session_state['rgofinal'] = RGO

    Psep = st.number_input('Pressão do separador (bar):', 1, 100, 10)
    Pexp = st.number_input('Pressão de exportação (bar):', 1, 1000, 300)
    C1 = st.number_input('Fração molar de C1(%):', 0, 100, 65)
    C2 = st.number_input('Fração molar de C2(%):', 0, 100, 8)
    C3 = st.number_input('Fração molar de C3(%):', 0, 100, 6)
    iC4 = st.number_input('Fração molar de i-C4(%):', 0, 100, 3)
    nC4 = st.number_input('Fração molar de n-C4(%):', 0, 100, 0)
    iC5 = st.number_input('Fração molar de i-C5(%):', 0, 100, 1)
    nC5 = st.number_input('Fração molar de n-C5(%):', 0, 100, 0)
    nC6 = st.number_input('Fração molar de n-C6(%):', 0, 100, 0)
    nC7 = st.number_input('Fração molar de n-C7(%):', 0, 100, 0)
    nC8 = st.number_input('Fração molar de n-C8(%):', 0, 100, 0)
    n2 = st.number_input('Fração molar de N2(%):', 0, 100, 0)
    co2 = st.number_input('Fração molar de CO2(%):', 0, 100, 10)
    h2s = st.number_input('Fração molar de H2S(%):', 0, 100, 0)
    h2o = st.number_input('Fração molar de H2O(%):', 0, 100, 7)
    #st.write("Processos adicionais:")
    #CO2 = st.checkbox("CO2")
    #H2S = st.checkbox("H2S")
    #lavagem = st.checkbox("Lavagem de óleo")

    button1 = st.button('Dimensionar planta')

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
        MM = (C1*16.04 + C2*30.07 + C3*44.1 + iC4*58.12 + nC4*58.12 + iC5*72.15 + nC5*72.15 + nC6*86.18 + nC7*100.21 + nC8*114.23 + n2*28.014 + co2*44.01 + h2s*34.1 + h2o*18.01)/100
        Tc = (C1*190.58 + C2*305.42 + C3*369.82 + iC4*408.14 + nC4*425.18 + iC5*692 + nC5*469.65 + nC6*507.43 + nC7*540.26 + nC8*568.83 + n2*126.10 + co2*304.19 + h2s*373.55 + h2o*647.13)/100
        Pc = (C1*46.04 + C2*48.80 + C3*42.49 + iC4*36.48 + nC4*37.97 + iC5*35.60 + nC5*33.69 + nC6*30.12 + nC7*27.36 + nC8*24.86 + n2*33.94 + co2*73.82 + h2s*90.08 + h2o*220.55)/100
        Kheat = (C1*1.32 + C2*1.18 + C3*1.13 + iC4*1.19 + nC4*1.18 + iC5*1.08 + nC5*1.08 + nC6*1.06 + nC7*1.05 + nC8*1.05 + n2*1.40 + co2*1.28 + h2s*1.32 + h2o*1.33)/100
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
        
        #Functions
        def Zcalc(T,P):
            T = float(T)
            P = float(P)
            Tr = (T / Tc)
            Pr = (P / Pc)
            B0 = 0.083 - (0.422 / (Tr ** 1.6))
            B1 = 0.139 - (0.172 / (Tr ** 4.2))
            w = -1 - math.log(Pr, 10)
            Z = 1 + B0 * (Pr / Tr) + w * B1 * (Pr / Tr)
            return Z
        
        def Knockoutcalc(T,P):
            T = float(T)
            P = float(P)
            Kint = 0.080
            R = 0.082205  #L atm/K mol
            ROl = 800 #kg/m³

            # Cálculo de Z
            Z = Zcalc(T,P)

            # Cálculo de vmax
            ROg = (((P/1.013) * MM) / (Z * R * T))   #kg/m³
            vmax = Kint * math.sqrt((ROl - ROg) / ROg)

            # Cálculo de Área e Diâmetro
            R = 8.314462e-5  # m³ bar / K mol
            qv = (Z*gasprodM*R*T)/P  #m³/s
            Aknock = qv / vmax
            Dknock = 1 * math.sqrt((4 * Aknock) / math.pi)
            return Aknock, Dknock, ROg
        
        def Compressorcalc(T,P):
            T = float(T)
            P = float(P)
            Pcomp = P * razcomp
            nisen = 0.7
            npoli = 0.75
            nmec = 0.8
            R = 8.314  # KJ/KmolK
            M = gasprodM/3.6   # Kmol/h 

            # Cálculo de Td
            Td = T * ((Pcomp / P) ** (((Kheat - 1) / Kheat) * (1 / npoli)))

            # Cálculo de Z
            Z = Zcalc(((T+Td)/2), P)

            # Cálculo de Hisen e Pot
            Hisen = Z * R * (Kheat / (Kheat - 1)) * T * (((Pcomp / P) ** ((Kheat - 1) / Kheat)) - 1)
            Pot = (Hisen * M) / (nisen * nmec * 3600)
            return Pot, Td, Pcomp
        
        def Resfriadorcalc(Td,Pcomp,ROg):
            Td = float(Td)
            Pcomp = float(Pcomp)
            Tci = 293.15  # K
            Tco = 303.15  # K
            Thi = Td  # K
            Tho = 313.15  # K
            mc = None  # Kg/s
            R = 8.314462e-5  # m³ bar / K mol
            Z = Zcalc(Td, Pcomp)
            qv = (Z*gasprodM*R*((Thi+Tho)/2))/Pcomp  #m³/s
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
            Atroc = (Q / (DTLM * U)) * 1.1
            return Atroc, Q

        gasprod = ((qprodp * RGO)/2) * 0.0000018414    #dois trens idênticos de produção. m³/s
        Z = Zcalc(313.15, Psep)
        R = 8.314462e-5  #m³ bar / K mol
        
        gasprodM = (Psep*gasprod)/(Z*R*313.15)   #vazão molar de gás, em mol/s. Calcula a vazão vol em cada equip
        nestag = math.ceil(math.log(Pexp/Psep)/math.log(4))
        razcomp = (Pexp / Psep) ** (1 / nestag)

        if (nestag == 3):

            #Knockout1
            T1 = 313.15  # K
            P1 = Psep    # bar
            Aknock1, Dknock1, ROg = Knockoutcalc(T1,P1)

            #Compressor1
            Pot1, Td1, Pcomp1 = Compressorcalc(T1,P1)

            #Resfriador1
            Atroc1, Q1 = Resfriadorcalc(Td1,Pcomp1,ROg)
            Atroc1 = float(Atroc1)
            Q1 = float(Q1)

            # Knockout2
            T2 = 313.15  # K
            P2 = Pcomp1
            Aknock2, Dknock2, ROg  = Knockoutcalc(T2,P2)

            # Compressor2
            Pot2, Td2, Pcomp2 = Compressorcalc(T2,P2)

            # Resfriador2
            Atroc2, Q2 = Resfriadorcalc(Td2,Pcomp2,ROg)
            Atroc2 = float(Atroc2)
            Q2 = float(Q2)

            # Knockout3
            T3 = 313.15  # K
            P3 = Pcomp2
            Aknock3, Dknock3, ROg  = Knockoutcalc(T3,P3)

            # Compressor3
            Pot3, Td3, Pcomp3 = Compressorcalc(T3,P3)

            # Resfriador3
            Atroc3, Q3 = Resfriadorcalc(Td3,Pcomp3,ROg)
            Atroc3 = float(Atroc3)
            Q3 = float(Q3)



        elif (nestag == 4):

            #Knockout1
            T1 = 313.15  # K
            P1 = Psep          
            Aknock1, Dknock1, ROg  = Knockoutcalc(T1,P1)

            #Compressor1
            Pot1, Td1, Pcomp1 = Compressorcalc(T1,P1)

            #Resfriador1
            Atroc1, Q1 = Resfriadorcalc(Td1,Pcomp1)

            # Knockout2
            T2 = 313.15  # K
            P2 = Pcomp1
            Aknock2, Dknock2, ROg  = Knockoutcalc(T2,P2)

            # Compressor2
            Pot2, Td2, Pcomp2 = Compressorcalc(T2,P2)

            # Resfriador2
            Atroc2, Q2 = Resfriadorcalc(Td2,Pcomp2)

            # Knockout3
            T3 = 313.15  # K
            P3 = Pcomp2
            Aknock3, Dknock3, ROg  = Knockoutcalc(T3,P3)

            # Compressor3
            Pot3, Td3, Pcomp3 = Compressorcalc(T3,P3)

            # Resfriador3
            Atroc3, Q3 = Resfriadorcalc(Td3,Pcomp3)
            
            # Knockout4
            T4 = 313.15  # K
            P4 = Pcomp3
            Aknock4, Dknock4, ROg  = Knockoutcalc(T4,P4)

            # Compressor4
            Pot4, Td4, Pcomp4 = Compressorcalc(T4,P4)

            # Resfriador4
            Atroc4, Q4 = Resfriadorcalc(Td4,Pcomp4)


        Ttrifasico =30
        Tbifasico = Teletro
        Tflotador = 25

        dataknock = pd.DataFrame(
            [["Vaso de Knockout 1", str("{:.2f}".format(P1)), str("{:.2f}".format(Aknock1)), str("{:.2f}".format(Dknock1))], ["Vaso de Knockout 2", str("{:.2f}".format(P2)),str("{:.2f}".format(Aknock2)), str("{:.2f}".format(Dknock2))],
             ["Vaso de Knockout 3", str("{:.2f}".format(P3)), str("{:.2f}".format(Aknock3)), str("{:.2f}".format(Dknock3))]],
            columns=['Equipamento','Pressão Nominal (bar)', 'Área (m²)', 'Diâmetro (m)'])
        dataknock.index += 1
        st.table(dataknock)

        datacomp = pd.DataFrame(
            [["Compressor 1", str("{:.2f}".format(Pot1))], ["Compressor 2", str("{:.2f}".format(Pot2))],
             ["Compressor 3", str("{:.2f}".format(Pot3))]],
            columns=['Equipamento', 'Potência (KW)'])
        datacomp.index += 1
        st.table(datacomp)

        dataresf = pd.DataFrame(
            [["Resfriador 1", str("{:.2f}".format(Q1/1e6)), str("{:.2f}".format(Atroc1))], ["Resfriador 2", str("{:.2f}".format(Q2/1e6)), str("{:.2f}".format(Atroc2))],
             ["Resfriador 3", str("{:.2f}".format(Q3/1e6)), str("{:.2f}".format(Atroc3))]],
            columns=['Equipamento',"Carga Térmica (MW)", 'Área de Troca Térmica (m²)'])
        dataresf.index += 1
        st.table(dataresf)








