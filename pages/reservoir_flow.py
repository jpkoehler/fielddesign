import streamlit as st
import math
import numpy as np
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


def app():
    st.title('Reservatório e Escoamento')
    st.header('Dados de entrada')

    if 'n' in st.session_state:
        n = st.session_state['n']
    else:
        n = 1
    n = st.number_input('Número de poços:', 1, 10, n)
    st.session_state['n'] = n


    def solversingle(K, IP, Psep, Pe):

        x = K * IP
        y = 1
        z = IP*(Psep-Pe)

        delta = y * y - 4 * x * z


        sqrtval = math.sqrt(abs(delta))

        # Output
        if delta > 0:



            return((-y + sqrtval) / (2 * x)*6.2898)





        elif delta == 0:



            return((-y / (2 * x))*6.2898)

            # when discriminant is less than 0

        else:

            st.write("Raízes complexas")

            st.write(- y / (2 * x), " + i", sqrtval)

            st.write(- y / (2 * x), " - i", sqrtval)


    # Input

    K = 10**-5
    IP = []
    newIP=[]
    Psep = []
    newPsep = []
    Pe = []
    newPe = []
    Din = []
    newDin = []
    RGO = []
    newrgo = []
    qi = []
    wells = []

    Doptions = ["4 polegadas","6 polegadas","8 polegadas","10 polegadas"]

    cols = st.columns(n)

    if 'IP' in st.session_state:
        IP = st.session_state['IP'][:n]
        while (len(IP) < n):
            IP.append(26)
    else:
        IP = [26 for i in range(n)]
    if 'Psep' in st.session_state:
        Psep = st.session_state['Psep'][:n]
        while (len(Psep) < n):
            Psep.append(20)
    else:
        Psep = [20 for i in range(n)]
    if 'Pe' in st.session_state:
        Pe = st.session_state['Pe'][:n]
        while (len(Pe) < n):
            Pe.append(210)
    else:
        Pe = [210 for i in range(n)]
    if 'RGO' in st.session_state:
        RGO = st.session_state['RGO'][:n]
        while (len(RGO) < n):
            RGO.append(46)
    else:
        RGO = [46 for i in range(n)]



    for i, x in enumerate(cols):
        inputIP = st.number_input(f'IP{i+1}:', 0, 200, IP[i])
        newIP.append(inputIP)
        inputPsep = st.number_input(f'Pressão de chegada FPSO {i+1}:', 0, 200, Psep[i])
        newPsep.append(inputPsep)
        inputPe = st.number_input(f'Pressão de Reservatório {i+1}:', 0, 300, Pe[i])
        newPe.append(inputPe)
        inputRGO = st.number_input(f'RGO {i + 1}:', 0, 500, RGO[i])
        newrgo.append(inputRGO)
        inputDin = st.radio(f'Diâmetro interno {i + 1}:', Doptions)
        newDin.append(inputDin)
    st.session_state['IP'] = newIP
    st.session_state['Psep'] = newPsep
    st.session_state['Pe'] = newPe
    st.session_state['RGO'] = newrgo
    st.session_state['Din'] = newDin

    prodtotal = 0
    rgofinal = 0
    if st.button('Solver', key ="buttonsolver"):
        for i in range(0,n,1):
            qi.append(solversingle(K, newIP[i], newPsep[i], newPe[i]))
            prodtotal = prodtotal + solversingle(K, newIP[i], newPsep[i], newPe[i])
            wells.append(f'Well{i+1}')
        for i in range(0,n,1):
            rgofinal = rgofinal + newrgo[i] * (qi[i] / prodtotal)
        data = [newIP, qi, newPsep, newPe, newrgo]
        df = pd.DataFrame(data, columns=wells, index=["IP", "Oil Production (bpd)","Psep (bar)","Pe (bar)","RGO (sm³/sm³)"])
        st.dataframe(df.style.format("{:.0f}"))
        st.session_state['dfreservoir'] = df
        st.session_state['wells'] = wells
        st.write("Produção total é de "+str("{:.0f}".format(prodtotal))+" bpd")
        day = [*range(0, 10951, 1)]
        # bpd
        oilprod0 = prodtotal
        st.session_state['prodtotal'] = prodtotal
        tf = 10950  # dias
        i = 0.09  # anual
        b = 0.2 / 365
        T = 0.35
        R = 0.10
        p = 50

        oilprodplateau1 = []
        oilprod = []

        for y in day:
            bsw = 1 - numpy.exp((-0.2 * y)/365)
            oilprod.append((oilprod0 * (1 - bsw)))

        fig, ax = plt.subplots()
        ax.plot(day, oilprod, label="Original")
        #ax.plot(day, oilprodplateau1, label="Patamar")
        ax.legend()

        st.pyplot(fig)









    #x[0] = q1, x[1] = q2, x[2] = Pm

    def functionarray(x):
        K1 = 1e-5
        K2 = 1e-5
        K3 = 4.4e-6
        IP1 = 26
        IP2 = 40
        Pe1 = 230
        Pe2 = 200
        Psep = 20

        return [K1 * (x[0])**2 + (x[0]/IP1) + x[2] - Pe1,
                K2 * (x[1])**2 + (x[1] / IP2) + x[2] - Pe2,
                K3 * (x[0]+x[1])**2 -x[2] + Psep]

    root = fsolve(functionarray, [1, 1, 1])
    liquidprod = root[0]+root[1]

    print (root)

    oilprod = []
    bswref = []
    year = [*range(0,31,1)]
    print (year)

    for i in year:
        bsw = 1-numpy.exp(-0.2*i)
        bswref.append(bsw)
        oilprod.append((liquidprod * (1-bsw))*6.2898)

    print (oilprod)
    fig, ax = plt.subplots(2)
    ax[0].plot(year, bswref, label="BSW")
    ax[1].plot(year, oilprod, label="Oil Production")
    ax[0].legend()
    ax[1].legend()

    plt.show()



