from fpdf import FPDF
from enum import Enum


class Color(Enum):
    BLUE = (10, 60, 120)
    DARK_BLUE = (42, 42, 100) 
    LIGHT_BLUE = (173, 216, 230)
    GRAY = (180, 180, 180)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


def reset_palette(pdf: FPDF) -> None:
        pdf.set_text_color(*Color.BLACK.value)
        pdf.set_font("Arial", size=12)


def line_break(pdf: FPDF) -> None:
        pdf.set_draw_color(*Color.GRAY.value)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(1)