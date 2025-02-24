from fpdf import FPDF
from manageyourdata.utils import constants, styles


def heading(pdf: FPDF) -> None:
    """Encabezado del reporte."""
    pdf.add_page()

    # Heading background.
    pdf.set_fill_color(*styles.Color.BLUE.value)
    pdf.rect(0, 0, 210, 25, style="F")

    # Left-aligned welcome heading.
    pdf.set_font("Arial", "B", size=14)
    pdf.set_text_color(*styles.Color.WHITE.value)
    pdf.cell(0, 10, "ManageYourData ha generado el siguiente reporte", align="L")

    # Right-aligned link.
    pdf.set_xy(-60, 10)
    pdf.set_font("Arial", "U", size=12)
    pdf.set_text_color(*styles.Color.LIGHT_BLUE.value)
    pdf.cell(50, 10, "Enlace a la herramienta", align="R", link=constants.GITHUB_URL)
    pdf.ln(25)  # Bottom margin.

    styles.reset_palette(pdf)  # Reset colors and text font.


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
    pdf.ln(7)  # Bottom margin.

    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Información general sobre el conjunto de los datos: ", ln=True, align="L")
    pdf.ln(7)  # Add space below the title.
    

def fields_info(pdf: FPDF, fields: list[dict]) -> None:
    """Detalles concretos de cada columna del dataframe."""
    for column in fields:
        pdf.add_page()

        # Heading.
        pdf.set_font("Arial", "B", size=16)
        pdf.set_fill_color(*styles.Color.DARK_BLUE.value)
        pdf.set_text_color(*styles.Color.WHITE.value)
        pdf.cell(190, 12, txt=column["Nombre"], border=1, align="C", fill=True)
        pdf.ln(15)  # Bottom margin.

        styles.reset_palette(pdf)

        # Show pandas data type and easy readable.
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(50, 10, "Tipo de dato", ln=False, align="C")
        pdf.set_font("Arial", size=12)
        df_type = column["Tipo de dato"]
        easy_type = constants.TIPO_DATO.get(df_type, "Desconocido")
        pdf.cell(140, 10, f"{easy_type} ({df_type})", ln=True)

        styles.line_break(pdf)

        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(50, 10, "Valores únicos", ln=False, align="C")
        pdf.set_font("Arial", size=12)
        pdf.cell(50, 10, txt=column["Valores únicos"], ln=True)

        styles.line_break(pdf)

        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(50, 10, "Valores nulos", ln=False, align="C")
        pdf.set_font("Arial", size=12)
        pdf.cell(50, 10, txt=column["Valores nulos"], ln=True)

        styles.line_break(pdf)

    pdf.ln()


def footer(pdf: FPDF) -> None:
    """Pie de página con numeración centrada."""
    pdf.set_y(-15)  # Padding from bottom.
    pdf.set_font("Arial", "I", size=10)
    pdf.set_draw_color(*styles.Color.GRAY.value)

    # Display content.
    page_number = f"Página {pdf.page_no()}"
    pdf.cell(0, 10, page_number, align="C")
    