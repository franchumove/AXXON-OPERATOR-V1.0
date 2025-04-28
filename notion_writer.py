"""
        notion_writer.py

        Módulo de escritura simbólica en Notion para AXXON.
        Crea páginas en bases de datos específicas usando estructura emocional adaptativa.

        Autor: AXXON DevCore
"""

import os
import logging
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)

        # ================================
        # FUNCIÓN PRINCIPAL DE ESCRITURA
        # ================================

def escribir_en_notion(database_id, user_id, mensaje, tipo_evento="evento", extra_tags=None):
            """
            Crea una página en la base de datos Notion correspondiente.

            Args:
                database_id (str): ID de la base de datos destino
                user_id (str): Identificador del usuario simbólico
                mensaje (str): Contenido emocional, reflexión o entrada simbólica
                tipo_evento (str): Clasificación del evento (ej. 'casos', 'mutacion')
                extra_tags (list): Etiquetas simbólicas asociadas (opcional)
            """
            try:
                if not user_id or not mensaje:
                    raise ValueError("user_id y mensaje no pueden estar vacíos.")

                properties = {
                    "Usuario": {
                        "title": [
                            {
                                "text": {
                                    "content": user_id.strip()
                                }
                            }
                        ]
                    },
                    "Mensaje": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": mensaje.strip()
                                }
                            }
                        ]
                    },
                    "Tipo de Evento": {
                        "select": {
                            "name": tipo_evento
                        }
                    }
                }

                if extra_tags:
                    properties["Tags"] = {
                        "multi_select": [{"name": tag.strip()} for tag in extra_tags if tag.strip()]
                    }

                notion.pages.create(
                    parent={"database_id": database_id},
                    properties=properties
                )

                logging.info(f"[Notion Writer] Página creada en Notion para {user_id} | Tipo: {tipo_evento} | Tags: {extra_tags or 'ninguno'}")

            except Exception as e:
                logging.error(f"[Notion Writer] Error al crear página en Notion para {user_id}: {e}")