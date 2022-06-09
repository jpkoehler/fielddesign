from PIL import Image
import streamlit as st

# Custom imports
from multipage import MultiPage
from pages import reservoir_flow, oilproperties, equipment, layout, wells, subsea, results, risk, SMS # import your pages here

# Create an instance of the app
app = MultiPage()

# Title of the main page
image = Image.open('logo_branco.png')
st.image(image)
st.title("Field Design")

# Add all your applications (pages) here
app.add_page("Reservatório e Escoamento", reservoir_flow.app)
app.add_page("Propriedades do Óleo", oilproperties.app)
app.add_page("Planta de Processo - Equipamentos", equipment.app)
app.add_page("Planta de Processo - Arranjo", layout.app)
app.add_page("Poços", wells.app)
app.add_page("Subsea", subsea.app)
app.add_page("Análise de Risco", risk.app)
app.add_page("SMS", SMS.app)
app.add_page("Resultados", results.app)


# The main app
app.run()
