from fpdf import FPDF
from manageyourdata.utils import constants


def heading(pdf: FPDF) -> None:
    """Encabezado del reporte."""
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=constants.REPORT_TITLE, ln=True, align="C")
    pdf.ln(7)  # Add space below the title.


def general_info(pdf: FPDF, metrics: dict) -> None:
    """Información general del reporte."""
    # Headers of the table.
    pdf.set_font("Arial", size=12)
    for key in metrics.keys():
        pdf.cell(38, 10, key, align="C")
    pdf.ln()

    # Loop through the data and create rows.
    pdf.set_font("Arial", "B", size=12)
    for value in metrics.values():
        pdf.cell(38, 10, value, border=1, align="C")
    pdf.ln()
    
    pdf.cell(200, 10, txt=constants.REPORT_COLUMNS, ln=True, align="L")

    pdf.ln(7) # Add space below the table.


def fields_info(pdf: FPDF, fields: list[dict]) -> None:
    pdf.set_font("Arial", "B", size=12)
    pdf.set_font("Arial", "B", 16)
    for column in fields:
        pdf.add_page()
        pdf.cell(50, 10, txt=column["Nombre"], ln=True, align="L")
    pdf.ln()
    