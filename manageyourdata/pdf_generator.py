import os
from fpdf import FPDF
from manageyourdata.utils import constants, styles


def heading(pdf: FPDF) -> None:
    """Encabezado del reporte."""
    pdf.add_page()

    # Heading background.
    pdf.set_fill_color(*styles.Color.BLUE.value)
    pdf.rect(0, 0, 210, 25, style="F")

    # Left-aligned welcome heading.
    pdf.set_font(styles.Font.ARIAL.value, "B", size=styles.Size.MEDIUM_BIG.value)
    pdf.set_text_color(*styles.Color.WHITE.value)
    pdf.cell(0, 10, "ManageYourData ha generado el siguiente reporte", align="L")

    # Right-aligned link.
    pdf.set_xy(-60, 10)
    pdf.set_font(styles.Font.ARIAL.value, "U", size=styles.Size.MEDIUM.value)
    pdf.set_text_color(*styles.Color.LIGHT_BLUE.value)
    pdf.cell(50, 10, "Enlace a la herramienta", align="R", link=constants.GITHUB_URL)
    pdf.ln(25)  # Bottom margin.

    styles.reset_palette(pdf)  # Reset colors and text font.


def general_info(pdf: FPDF, metrics: dict, file_name: str) -> None:
    """Información general del reporte."""
    # Headers of the table.
    pdf.set_font(styles.Font.ARIAL.value, size=styles.Size.MEDIUM.value)
    for key in metrics.keys():
        pdf.cell(38, 10, key, align="C")
    pdf.ln()

    # Loop through the data and create rows.
    pdf.set_font(styles.Font.ARIAL.value, "B", size=styles.Size.MEDIUM.value)
    for value in metrics.values():
        pdf.cell(38, 10, value, border=1, align="C")
    pdf.ln()
    pdf.ln(7)  # Bottom margin.

    # Plot from images generated.
    show_graphs(pdf, file_name)

    # Page footer.
    footer(pdf)
    

def fields_info(pdf: FPDF, fields: list[dict], file_name: str) -> None:
    """Detalles concretos de cada columna del dataframe."""
    for field in fields:
        pdf.add_page()

        # Heading.
        pdf.set_font(styles.Font.ARIAL.value, "B", size=styles.Size.BIG.value)
        pdf.set_fill_color(*styles.Color.DARK_BLUE.value)
        pdf.set_text_color(*styles.Color.WHITE.value)
        pdf.cell(190, styles.Size.MEDIUM.value, txt=field["Nombre"], border=1, align="C", fill=True)
        pdf.ln(15)  # Bottom margin.

        styles.reset_palette(pdf)

        # Details displayed for each field.
        field_info(pdf, field, "Tipo de dato")
        field_info(pdf, field, "Valores nulos")
        field_info(pdf, field, "Valores únicos")
        field_info(pdf, field, "Moda")
        field_info(pdf, field, "Percentiles")
        field_info(pdf, field, "Mediana")
        field_info(pdf, field, "Media")
        field_info(pdf, field, "Máximo")
        field_info(pdf, field, "Mínimo")
        field_info(pdf, field, "DE")

        # Plot from images generated.
        show_graphs(pdf, file_name, field["Nombre"])

        # Page footer.
        footer(pdf)

    pdf.ln()


def field_info(pdf: FPDF, field: dict, title: str) -> None:
    """Entradas para cada uno de los campos del dataframe."""
    pdf.set_font(styles.Font.ARIAL.value, style="B", size=styles.Size.MEDIUM.value)
    pdf.cell(50, 10, title, ln=False, align="C")
    pdf.set_font(styles.Font.ARIAL.value, size=styles.Size.MEDIUM.value)
    pdf.cell(styles.Size.MEDIUM_BIG.value, 10, txt=field[title], ln=True)
    styles.line_break(pdf)


def show_graphs(pdf: FPDF, file_name: str, field="") -> None:
    """Mostrar las imagenes generadas en el pdf."""
    images = dict()
    path = f"images/{file_name}/{field}" if field != "" else f"images/{file_name}"
    images[f"{field}"] = [f"{path}/{image}" for image in os.listdir(path) if image.endswith(".png")] 

    # Grid parameters (2x2).
    x_positions = [25, 110]  # Left and right columns.
    y_position = pdf.get_y() + 10  # Current position.

    for i, img in enumerate(next(iter(images.values()))):
        x_position = x_positions[i % 2]
        pdf.image(img, x=x_position, y=y_position, w=70, h=60)
        if i % 2 == 1:  # Slide below.
            y_position += 70


def footer(pdf: FPDF) -> None:
    """Pie de página con numeración centrada."""
    pdf.auto_page_break = False  # Stick to bottom.
    pdf.set_y(-15)  # Padding from bottom.
    pdf.set_font(styles.Font.ARIAL.value, "I", size=styles.Size.SMALL.value)
    pdf.set_draw_color(*styles.Color.GRAY.value)
    # Display content.
    page_number = f"Página {pdf.page_no()}"
    pdf.cell(0, 10, page_number, align="C")
    