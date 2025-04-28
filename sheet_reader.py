"""
AXXON - Módulo de Lectura Simbólica desde Google Sheets

Permite consultar eventos simbólicos, mutaciones y rutas desde Sheets
para recuperar contexto histórico o resonancia emocional por usuario.
"""

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"
SHEET_NAME = "AXXON_LOG"

# Autenticación
def autenticar_google_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

# Leer todos los eventos
def leer_eventos_completos():
    hoja = autenticar_google_sheet()
    registros = hoja.get_all_records()
    return registros

# Filtrar eventos por user_id
def obtener_eventos_por_usuario(user_id):
    registros = leer_eventos_completos()
    return [r for r in registros if str(r.get("user_id", "")).strip() == str(user_id)]

# Obtener últimos N eventos
def ultimos_eventos(user_id, n=5, tipo_evento=None):
    eventos = obtener_eventos_por_usuario(user_id)
    if tipo_evento:
        eventos = [e for e in eventos if e.get("tipo_evento") == tipo_evento]
    return eventos[-n:]

# Extraer últimas rutas simbólicas
def ultimas_rutas(user_id, n=3):
    eventos = ultimos_eventos(user_id, n=20, tipo_evento="casos")
    rutas = []
    for ev in eventos:
        contenido = ev.get("contenido", "")
        if "PLAN:" in contenido:
            plan = contenido.split("PLAN:")[-1].strip()
            rutas.append(plan)
    return rutas[-n:]