"""
sync_manager.py
Gestor de sincronización simbólica bidireccional

Sincroniza eventos simbólicos entre Google Sheets, Notion y FAISS.
Recarga vectores semánticos para mantener memoria viva actualizada.
"""

import logging
from exportar_bloques_jsonl import exportar_todo
from sync_sheet_to_notion import sincronizar_sheet_a_notion
from memory_engine import cargar_y_vectorizar

def sincronizar_bi_direccional(tipo="casos"):
    try:
        logging.info(f"[SYNC] Iniciando sincronización total para tipo: {tipo}")
        sincronizar_sheet_a_notion(tipo)
        exportar_todo()
        cargar_y_vectorizar()
        logging.info("✅ Memoria simbólica sincronizada entre Sheet, Notion y FAISS.")
    except Exception as e:
        logging.error(f"❌ Error en sincronización bidireccional simbólica: {e}")