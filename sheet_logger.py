"""
sheet_logger.py

Conector simbólico entre AXXON y Google Sheets.
Registra eventos interpretativos en hojas clasificadas por tipo simbólico.

Incluye autenticación, mapeo de pestañas y función de logging simbólico.

Autor: AXXON DevCore
"""

import gspread
import logging
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# ================================
# CONFIGURACIÓN Y CONEXIÓN
# ================================

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_to_sheets():
    """
    Conecta con Google Sheets usando credenciales locales.
    """
    try:
        logging.info("[AXXON Logger] Conectando con Google Sheets...")
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("SHEET.json", scope)
        client = gspread.authorize(creds)
        logging.info("[AXXON Logger] Autenticación exitosa con Google Sheets.")
        return client
    except Exception as e:
        logging.error(f"[AXXON Logger] Error al conectar con Sheets: {e}")
        raise

# ================================
# MAPEO DE PESTAÑAS POR EVENTO
# ================================

TAB_MAP = {
    "fundacional": "Órganos Cognitivos Fundacionales",
    "polaridad": "Estructura de Contradicciones y Polaridades",
    "diccionario_base": "Diccionario Simbólico Base",
    "expansion": "Espacio de Expansión",
    "diccionario_vivo": "Diccionario Vivo",
    "emergente_interpretativo": "Pensamiento Emergente interpretativo",
    "transversalidad": "Transversalidad Cognitiva",
    "tablero": "tablero_adaptativo",
    "tablero_adaptativo": "tablero_adaptativo",
    "emergente_cognitivo": "Pensamiento Emergente Cognitivo",
    "mutacion": "Mapa de Mutación",
    "casos": "Memoria de Casos",
    "bitacora": "Bitácora Interpretativa",
    "general": "general",
    "usuarios": "USUARIOS"
}

# ================================
# FUNCIÓN PRINCIPAL DE LOGGING
# ================================

def log_event_simbolico(user_id, tipo_evento, contenido, nivel="N/A", tags=None):
    """
    Registra un evento simbólico en la hoja correspondiente.

    Args:
        user_id (str): ID del usuario
        tipo_evento (str): clave del evento simbólico
        contenido (str): mensaje o inferencia a registrar
        nivel (str): intensidad o gravedad simbólica
        tags (list): etiquetas semánticas
    """
    try:
        client = connect_to_sheets()
        hoja = TAB_MAP.get(tipo_evento)

        if not hoja:
            raise ValueError(f"[AXXON Logger] Tipo de evento '{tipo_evento}' no está mapeado en TAB_MAP.")

        sheet = client.open("AXXON CORE")
        worksheet = sheet.worksheet(hoja)

        fila = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id,
            contenido,
            nivel,
            ", ".join(tags) if tags else "Sin etiquetas"
        ]

        worksheet.append_row(fila)
        logging.info(f"[AXXON Logger] Evento registrado en hoja '{hoja}': {fila}")

    except Exception as e:
        logging.error(f"[AXXON Logger] Fallo al registrar evento simbólico en tipo '{tipo_evento}': {e}")