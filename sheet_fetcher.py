"""
sheet_fetcher.py

Lector de identidad simbólica desde Google Sheets para AXXON Core.
Extrae la fila correspondiente a un user_id y devuelve sus atributos arquetípicos.

Autor: AXXON DevCore
"""

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

# Configuración de autenticación
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds_path = os.getenv("GOOGLE_CREDS_JSON", "SHEET.json")

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    logging.info("[AXXON SheetFetcher] Autenticación con Google Sheets exitosa.")
except Exception as e:
    logging.error(f"[AXXON SheetFetcher] Error en autenticación: {e}")
    client = None

def fetch_user_row_from_sheet(user_id: str) -> dict:
    """
    Busca el user_id en la hoja "usuarios" y devuelve la fila como dict plano.

    Returns:
        dict con claves simbólicas si existe, o None si no se encuentra.
    """
    try:
        if not client:
            raise RuntimeError("Cliente de Google Sheets no inicializado correctamente.")

        sheet_name = os.getenv("GOOGLE_SHEET_NAME", "AXXON CORE")
        hoja = client.open(sheet_name).worksheet("usuarios")
        registros = hoja.get_all_records()

        for fila in registros:
            if str(fila.get("user_id")).strip() == str(user_id).strip():
                return fila

    except Exception as e:
        logging.error(f"[AXXON SheetFetcher] Error al buscar usuario: {e}")

    return None