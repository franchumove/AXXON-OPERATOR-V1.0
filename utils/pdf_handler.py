from fpdf import FPDF
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def guardar_como_txt(texto, nombre_base):
    ruta = f"{nombre_base}.txt"
    with open(ruta, "w") as f:
        f.write(texto)
    return ruta

def guardar_como_pdf(texto, nombre_base):
    ruta = f"{nombre_base}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for linea in texto.split("\n"):
        pdf.cell(200, 10, txt=linea, ln=1)
    pdf.output(ruta)
    return ruta

def subir_a_drive(ruta_archivo):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    nombre = os.path.basename(ruta_archivo)
    file_metadata = {'name': nombre}
    media = MediaFileUpload(ruta_archivo, resumable=True)
    archivo = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return archivo.get('id')
