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

    if 'oilprodp' in st.session_state:
        oilprodp = st.session_state['oilprodp']
    else:
        oilprodp = 15000

    qprodp = st.number_input('Capacidade da planta (STB/d):', 1, 1000000, oilprodp)
    st.session_state['oilprodp'] = qprodp

    Psep = st.number_input('Pressão do separador (bar):', 1, 100, 10)
    Pexp = st.number_input('Pressão de exportação (bar):', 1, 1000, 300)
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

        if 'rgofinal' in st.session_state:
            RGO = st.session_state['rgofinal']
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
        st.write(f'O VPN é {vpn}.')
        st.write(f'O CAPEX para o navio é {capexn}.')
        st.write(f'O CAPEX para os poços é de {capexp}.')
        st.write(f'O CAPEX para arranjo subsea é {capexs}.')
        st.write(f'O VPL é {vpl}.')




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
        st.write("O diâmetro do separador trifásico é " + str("{:.2f}".format(Dtrifasico)) + " m.")
        st.write("O comprimento do separador trifásico é " + str("{:.2f}".format(Ltrifasico)) + " m.")
        st.write("O diâmetro dos separadores bifásicos é " + str("{:.2f}".format(Dbifasico)) + " m.")
        st.write("O comprimento dos separadores bifásicos é " + str("{:.2f}".format(Lbifasico)) + " m.")
        st.write("O diâmetro do separador eletrostático é " + str("{:.2f}".format(Deletro)) + " m.")
        st.write("O comprimento do separador eletrostático é " + str("{:.2f}".format(Leletro)) + " m.")
        st.write("O número de hidrociclones do separador trifásico são " + str(ciclonumber))

        gasprod = oilprodp * RGO
        nestag = math.ceil(math.log(Pexp/Psep)/math.log(4))
        st.write("O sistema de compressão possui "+str(nestag)+" estágios.")
        razcomp = (Pexp / Psep) ** (1 / nestag)
        st.write("O sistema de compressão possui razão de compressão de " + str(razcomp) + ".")

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
            st.write("Área do knockout 1 é " + str("{:.2f}".format(Aknock1)) + " m².")
            st.write("Diâmetro do Knockout 1 é " + str("{:.2f}".format(Dknock1)) + " m.")

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

            st.write("T de descarga do compressor 1 é " + str("{:.0f}".format(Td1)) + " K.")
            st.write("Potência do compressor 1 é " + str("{:.0f}".format(Pot1)) + " KW.")

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

            st.write("Área de troca térmica do resfriador 1 é " + str("{:.0f}".format(Atroc1)) + " m².")
            st.write("A carga térmica do resfriador 1 é " + str("{:.0f}".format(Q)) + " W.")

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
            st.write("Área do knockout 2 é " + str("{:.2f}".format(Aknock2)) + " m².")
            st.write("Diâmetro do Knockout 2 é " + str("{:.2f}".format(Dknock2)) + " m.")

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

            st.write("T de descarga do compressor 2 é " + str("{:.0f}".format(Td2)) + " K.")
            st.write("Potência do compressor 2 é " + str("{:.0f}".format(Pot2)) + " KW.")

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

            st.write("Área de troca térmica do resfriador 2 é " + str("{:.0f}".format(Atroc2)) + " m².")
            st.write("A carga térmica do resfriador 2 é " + str("{:.0f}".format(Q2)) + " W.")

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
            st.write("Área do knockout 3 é " + str("{:.2f}".format(Aknock3)) + " m².")
            st.write("Diâmetro do Knockout 3 é " + str("{:.2f}".format(Dknock3)) + " m.")

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

            st.write("T de descarga do compressor 3 é " + str("{:.0f}".format(Td3)) + " K.")
            st.write("Potência do compressor 3 é " + str("{:.0f}".format(Pot3)) + " KW.")

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

            st.write("Área de troca térmica do resfriador 3 é " + str("{:.0f}".format(Atroc3)) + " m².")
            st.write("A carga térmica do resfriador 3 é " + str("{:.0f}".format(Q3)) + " W.")

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
            st.write("Área do knockout 1 é " + str("{:.2f}".format(Aknock1)) + " m².")
            st.write("Diâmetro do Knockout 1 é " + str("{:.2f}".format(Dknock1)) + " m.")

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

            st.write("T de descarga do compressor 1 é " + str("{:.0f}".format(Td1)) + " K.")
            st.write("Potência do compressor 1 é " + str("{:.0f}".format(Pot1)) + " KW.")

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

            st.write("Área de troca térmica do resfriador 1 é " + str("{:.0f}".format(Atroc1)) + " m².")
            st.write("A carga térmica do resfriador 1 é " + str("{:.0f}".format(Q)) + " W.")

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
            st.write("Área do knockout 2 é " + str("{:.2f}".format(Aknock2)) + " m².")
            st.write("Diâmetro do Knockout 2 é " + str("{:.2f}".format(Dknock2)) + " m.")

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

            st.write("T de descarga do compressor 2 é " + str("{:.0f}".format(Td2)) + " K.")
            st.write("Potência do compressor 2 é " + str("{:.0f}".format(Pot2)) + " KW.")

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

            st.write("Área de troca térmica do resfriador 2 é " + str("{:.0f}".format(Atroc2)) + " m².")
            st.write("A carga térmica do resfriador 2 é " + str("{:.0f}".format(Q2)) + " W.")

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
            st.write("Área do knockout 3 é " + str("{:.2f}".format(Aknock3)) + " m².")
            st.write("Diâmetro do Knockout 3 é " + str("{:.2f}".format(Dknock3)) + " m.")

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

            st.write("T de descarga do compressor 3 é " + str("{:.0f}".format(Td3)) + " K.")
            st.write("Potência do compressor 3 é " + str("{:.0f}".format(Pot3)) + " KW.")

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

            st.write("Área de troca térmica do resfriador 3 é " + str("{:.0f}".format(Atroc3)) + " m².")
            st.write("A carga térmica do resfriador 3 é " + str("{:.0f}".format(Q3)) + " W.")

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
            st.write("Área do knockout 4 é " + str("{:.2f}".format(Aknock4)) + " m².")
            st.write("Diâmetro do Knockout 4 é " + str("{:.2f}".format(Dknock4)) + " m.")

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

            st.write("T de descarga do compressor 4 é " + str("{:.0f}".format(Td4)) + " K.")
            st.write("Potência do compressor 4 é " + str("{:.0f}".format(Pot4)) + " KW.")

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

            st.write("Área de troca térmica do resfriador 4 é " + str("{:.0f}".format(Atroc4)) + " m².")
            st.write("A carga térmica do resfriador 4 é " + str("{:.0f}".format(Q4)) + " W.")


















