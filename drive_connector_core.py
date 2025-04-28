"""
AXXON CORE OPERATOR - Drive Connector
-------------------------------------
Permite subir archivos generados simbólicamente (txt, pdf) a Google Drive.

Autor: AXXON DevCore
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_DRIVE_UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=media"
GOOGLE_ACCESS_TOKEN = os.getenv("GOOGLE_ACCESS_TOKEN")

def subir_a_drive(file_path, mime_type="application/pdf"):
    """
    Sube un archivo a Google Drive utilizando el token de acceso.

    Args:
        file_path (str): Ruta local del archivo.
        mime_type (str): Tipo MIME del archivo (por defecto PDF).

    Returns:
        dict: Respuesta de la API de Google Drive o error.
    """
    try:
        headers = {
            "Authorization": f"Bearer {GOOGLE_ACCESS_TOKEN}",
            "Content-Type": mime_type
        }
        with open(file_path, "rb") as f:
            response = requests.post(GOOGLE_DRIVE_UPLOAD_URL, headers=headers, data=f)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}

    except Exception as e:
        return {"error": str(e)}

# 🧪 Test rápido
if __name__ == "__main__":
    resultado = subir_a_drive("prueba.pdf")
    print(resultado)