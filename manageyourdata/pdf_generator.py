from fpdf import FPDF
from utils import constants

def heading(pdf: FPDF):
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=constants.REPORT_TITLE, ln=True, align="C")
    pdf.ln(7)


def general_info(pdf: FPDF, metrics: dict):
    pdf.set_font("Arial", size=12)
    # Header of the table.
    for key in metrics.keys():
        pdf.cell(38, 10, key, align="C")
    pdf.ln()

    pdf.set_font("Arial", "B", size=12)
    # Loop through the data and create rows.
    for value in metrics.values():
        pdf.cell(38, 10, value, border=1, align="C")
    pdf.ln()

    pdf.ln(7)

def columns_info(pdf: FPDF, columns: str):
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt=constants.REPORT_COLUMNS, ln=True, align="L")
    pdf.set_font("Arial", "B", 16)
    for column in columns:
        pdf.add_page()
        pdf.cell(50, 10, txt=column, ln=True, align="L")
    pdf.ln()
    