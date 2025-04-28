"""
        sync_sheet_to_notion.py

        Sincronizador simbólico de eventos entre Google Sheets y Notion.
        Soporta múltiples tipos: casos, usuarios, mutaciones, bitácoras...

        Usa `notion_writer` como canal de escritura y `notion_config.json` como mapa simbólico.

        Autor: Francois Fillette
"""

import json
import logging
from notion_writer import escribir_en_notion
from sheet_logger import connect_to_sheets, TAB_MAP
from notion_fetcher import get_table_id

        # Configurar logging simbólico
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        # Cargar config Notion
with open("notion_config.json") as f:
            NOTION_CONFIG = json.load(f)

        # ========================
        # MÉTODO PRINCIPAL
        # ========================

def sincronizar_sheet_a_notion(tipo_evento: str, subtabla: str = None):
            """
            Sincroniza datos desde Sheets a Notion según tipo de evento o identidad.
            """

            try:
                logging.info(f"[AXXON SYNC] Iniciando sincronización para tipo: {tipo_evento}...")

                # 1. Conectar con Sheets
                client = connect_to_sheets()
                hoja = TAB_MAP.get(tipo_evento)

                if not hoja:
                    raise ValueError(f"[AXXON SYNC] No se encontró hoja en TAB_MAP para tipo_evento: {tipo_evento}")

                # 2. Obtener ID del database de Notion
                database_id = None

                if subtabla:
                    database_id = get_table_id(subtabla)
                else:
                    database_id = get_table_id(tipo_evento)

                if not database_id:
                    raise ValueError(f"[AXXON SYNC] No se encontró database_id en notion_config para: {tipo_evento} (subtabla: {subtabla})")

                # 3. Extraer datos desde Sheets
                sheet = client.open("AXXON CORE")
                worksheet = sheet.worksheet(hoja)
                rows = worksheet.get_all_values()

                if not rows or len(rows) <= 1:
                    raise ValueError(f"[AXXON SYNC] La hoja '{hoja}' está vacía o no tiene datos.")

                headers = rows[0]
                registros = rows[1:]  # Saltar encabezado

                # 4. Procesar fila por fila
                for row in registros:
                    fila = dict(zip(headers, row))

                    user_id = fila.get("user_id") or fila.get("usuario") or ""
                    mensaje = fila.get("mensaje") or fila.get("comentario") or fila.get("input") or ""
                    tags = fila.get("tags") or fila.get("etiquetas") or ""
                    tags_list = tags.split(",") if tags else []

                    escribir_en_notion(
                        database_id=database_id,
                        user_id=user_id.strip(),
                        mensaje=mensaje.strip(),
                        tipo_evento=tipo_evento,
                        extra_tags=[t.strip() for t in tags_list if t.strip()]
                    )

                logging.info(f"✅ Sincronización simbólica completa: '{tipo_evento}' → Notion (tabla: {subtabla or tipo_evento})")

            except Exception as e:
                logging.error(f"❌ Error en sincronización simbólica [{tipo_evento}]: {e}")