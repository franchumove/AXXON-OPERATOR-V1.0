import os
import fitz  # PyMuPDF
from fpdf import FPDF
import memory_store
from upload_to_drive import subir_resumen_a_drive  # Asegúrate de tener este archivo funcionando

# Carpetas
CARPETA_PDFS = "pdfs"
CARPETA_TXT = "resumenes"

# Función para leer PDF
def leer_pdf(path):
    doc = fitz.open(path)
    texto_total = ""
    for pagina in doc:
        texto_total += pagina.get_text()
    return texto_total

# Función para resumir texto
def resumir(texto, max_palabras=100):
    palabras = texto.split()
    if len(palabras) <= max_palabras:
        return texto
    return " ".join(palabras[:max_palabras]) + "..."

# Función para generar PDF desde texto
def guardar_como_pdf(texto, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for linea in texto.split("\n"):
        pdf.cell(200, 10, txt=linea, ln=1)
    pdf.output(output_path)

# Crear carpetas si no existen
os.makedirs(CARPETA_TXT, exist_ok=True)

# Procesar todos los PDFs
for archivo in os.listdir(CARPETA_PDFS):
    if archivo.lower().endswith(".pdf"):
        ruta_pdf = os.path.join(CARPETA_PDFS, archivo)
        clave = archivo.replace(".pdf", "").replace(" ", "_").lower()

        if clave in memory_store.MEMORIA_DOCUMENTAL:
            print(f"🟡 Ya existe en memoria: '{clave}' — Skipping")
            continue

        try:
            print(f"📄 Procesando: {archivo}")
            texto = leer_pdf(ruta_pdf)
            resumen = resumir(texto)

            # Guardar en memoria simbólica
            memory_store.guardar_documento(clave, texto)
            memory_store.guardar_documento(f"resumen_{clave}", resumen)

            # Guardar resumen como .txt
            ruta_txt = os.path.join(CARPETA_TXT, f"{clave}_resumen.txt")
            with open(ruta_txt, "w", encoding="utf-8") as f:
                f.write(resumen)

            # Guardar resumen como .pdf
            ruta_pdf_resumen = os.path.join(CARPETA_TXT, f"{clave}_resumen.pdf")
            guardar_como_pdf(resumen, ruta_pdf_resumen)

            # Subir PDF a Drive
            subir_resumen_a_drive(ruta_pdf_resumen)

        except Exception as e:
            print(f"❌ Error procesando {archivo}: {e}")