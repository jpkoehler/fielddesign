from PIL import Image
import streamlit as st
import utils as utl

# Custom imports
from multipage import MultiPage
from pages import equipment # import your pages here

# Create an instance of the app
app = MultiPage()

# Title of the main page
# st.title("Field Design")
utl.local_css("style.css")

# Add all your applications (pages) here
app.add_page("Características do Projeto", oilproperties.py)
app.add_page("Reservatório e Escoamento", reservoir_flow.py)
app.add_page("Subsea e Naval", subsea.py)
app.add_page("Poços", wells.py)
app.add_page("Planta de Processo - Equipamentos", equipment.py)
app.add_page("Planta de Processo - Arranjo", layout.py)
app.add_page("Análise de Risco", risk.py)
app.add_page("Análise Econômica", economic.py)
app.add_page("SMS", SMS.py)
app.add_page("Resultados", results.py)




# The main app
app.run()
