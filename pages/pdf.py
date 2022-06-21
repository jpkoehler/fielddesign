from fpdf import FPDF
import fpdf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('logo_branco.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(80, 10, 'Relatório de Resultados', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')




pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 12)

df = pd.DataFrame(np.random.random((10,3)), columns = ("col 1", "col 2", "col 3"))
fig, ax =plt.subplots(figsize=(12,4))
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
plt.savefig('table.png', dpi=200, bbox_inches='tight')

pdf.cell(0, 10, 'Resultados de Reservatório e Escoamento:', 0, 1)
pdf.image('table.png', x = None, y = None, w = 200, h = 100, type = '', link = '')
for i in range(1, 41):
    pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
pdf.output('Relatório - Caso X.pdf', 'F')