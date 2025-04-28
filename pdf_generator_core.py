"""
AXXON CORE OPERATOR - PDF Generator
-----------------------------------
Genera archivos PDF simbólicos a partir de texto emocional o narrativo.

Autor: AXXON DevCore
"""

from fpdf import FPDF
import os

def guardar_como_pdf(texto, nombre_base):
    """
    Genera un PDF a partir de texto y lo guarda localmente.

    Args:
        texto (str): Contenido a incluir en el PDF.
        nombre_base (str): Nombre base del archivo (sin extensión).

    Returns:
        str: Ruta del archivo generado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for linea in texto.split("\n"):
        pdf.multi_cell(0, 10, linea)

    file_path = f"{nombre_base}.pdf"
    pdf.output(file_path)

    return file_path

# 🧪 Test rápido
if __name__ == "__main__":
    ruta = guardar_como_pdf("Este es un test simbólico de PDF.", "test_pdf")
    print(f"PDF generado en: {ruta}")