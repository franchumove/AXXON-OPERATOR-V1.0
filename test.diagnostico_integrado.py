"""
diagnostico_integrado.py
AXXON — Diagnóstico Simbólico Modular

Permite:
- Testear si el logger simbólico a Google Sheets funciona.
- Verificar si el endpoint de sincronización con Notion está activo.
- Dejar rastro en la memoria simbólica de pruebas realizadas.
"""

import logging
import requests
from sheet_logger import log_event_simbolico

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def test_logger_sheets():
    try:
        log_event_simbolico(
            user_id="diagnostico-integrado",
            tipo_evento="casos",
            contenido="Test desde diagnostico_integrado.py — Logger Sheets OK",
            nivel="medio",
            tags=["diagnóstico", "sheets", "logger"]
        )
        logging.info("✅ Logger simbólico en Sheets funciona correctamente.")
    except Exception as e:
        logging.error(f"❌ Error en logger simbólico: {e}")

def test_sync_notion():
    try:
        res = requests.get("http://localhost:5500/sync-sheet-to-notion/tablero_adaptativo")
        if res.status_code == 200:
            logging.info("✅ Endpoint de sincronización con Notion activo.")
            logging.info(f"Contenido recibido: {res.json()}")
        else:
            logging.warning(f"⚠️ Sync Notion respondió con status {res.status_code}")
    except Exception as e:
        logging.error(f"❌ Error al contactar sync Notion: {e}")

if __name__ == "__main__":
    print("\n=== DIAGNÓSTICO INTEGRADO AXXON ===")
    test_logger_sheets()
    test_sync_notion()
    print("=== FIN DEL DIAGNÓSTICO ===\n")