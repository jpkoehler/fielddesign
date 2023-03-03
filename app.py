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
# app.add_page("Características do Projeto", oilproperties.app)
# app.add_page("Reservatório e Escoamento", reservoir_flow.app)
# app.add_page("Subsea e Naval", subsea.app)
# app.add_page("Poços", wells.app)
app.add_page("Planta de Processo - Equipamentos", equipment.app)
# app.add_page("Planta de Processo - Arranjo", layout.app)
# app.add_page("Análise de Risco", risk.app)
# app.add_page("Análise Econômica", economic.app)
# app.add_page("SMS", SMS.app)
# app.add_page("Resultados", results.app)




# The main app
app.run()
