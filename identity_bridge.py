"""
    identity_bridge.py

    Puente simbólico para lectura de identidad desde Notion y Google Sheets.

    Rol:
    - Leer identidad simbólica del usuario (arquetipo, polaridad, propósito, zona simbólica).
    - Prioriza Notion como fuente madre. Si falla o no encuentra, consulta Sheets.
    - Aplica normalización semántica de datos y retorna estructura simbólica lista para usar.

    Autor: Francois Fillette
"""

import logging
from notion_fetcher import fetch_table_rows, get_table_id
from sheet_fetcher import fetch_user_row_from_sheet

    # ==============================================
    # FUNCIÓN PRINCIPAL: obtener identidad simbólica
    # ==============================================

def get_identidad_simbolica(user_id: str) -> dict:
        """
        Devuelve la identidad simbólica completa de un usuario.
        Busca primero en Notion y luego en Sheets si es necesario.

        Args:
            user_id (str): Identificador del usuario

        Returns:
            dict: {
                "arquetipo": str,
                "polaridad": str,
                "proposito": str,
                "zona_simbólica": str
            }
        """
        # === INTENTO 1: desde Notion ===
        try:
            db_id = get_table_id("usuarios")
            if db_id:
                registros = fetch_table_rows(db_id)
                for fila in registros:
                    if str(fila.get("user_id")).strip() == str(user_id).strip():
                        logging.info(f"[AXXON] Identidad simbólica encontrada en Notion para {user_id}")
                        return _normalizar_identidad(fila)
        except Exception as e:
            logging.warning(f"[AXXON] Error al acceder a Notion para identidad de {user_id}: {e}")

        # === INTENTO 2: desde Google Sheets ===
        try:
            fila = fetch_user_row_from_sheet(user_id)
            if fila:
                logging.info(f"[AXXON] Identidad simbólica recuperada desde Google Sheets para {user_id}")
                return _normalizar_identidad(fila)
        except Exception as e:
            logging.warning(f"[AXXON] Error al acceder a Google Sheets para identidad de {user_id}: {e}")

        # === FALLBACK: identidad por defecto ===
        logging.info(f"[AXXON] Usando identidad simbólica por defecto para {user_id}")
        return {
            "arquetipo": "explorer",
            "polaridad": "transformar",
            "proposito": "generar vínculo",
            "zona_simbólica": "emocional"
        }

    # ==============================================
    # FUNCIÓN DE NORMALIZACIÓN
    # ==============================================

def _normalizar_identidad(fila: dict) -> dict:
        """
        Asegura que los campos simbólicos estén presentes y con valores válidos.

        Args:
            fila (dict): Datos crudos desde Notion o Sheets

        Returns:
            dict: Identidad simbólica normalizada
        """
        return {
            "arquetipo": fila.get("arquetipo", "explorer"),
            "polaridad": fila.get("polaridad", "transformar"),
            "proposito": fila.get("proposito", "generar vínculo"),
            "zona_simbólica": fila.get("zona_simbólica", "emocional")
        }