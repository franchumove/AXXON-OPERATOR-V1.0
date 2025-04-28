"""
notion_fetcher.py

Fetcher simbólico para AXXON – Lector de tablas Notion.
Traduce propiedades Notion en estructuras interpretables por la arquitectura simbólica.

Incluye:
- get_table_id(): Busca tabla desde alias simbólico
- fetch_table_rows(): Extrae filas como dicts planos

Autor: AXXON DevCore
"""

import os
import json
import logging
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)

with open("notion_config.json") as f:
    CONFIG = json.load(f)


def get_table_id(alias):
    for page in CONFIG["pages"].values():
        if alias in page.get("tables", {}):
            return page["tables"][alias]
    logging.warning(f"[AXXON] Tabla alias '{alias}' no encontrada en configuración.")
    return None


def fetch_table_rows(database_id):
    try:
        response = notion.databases.query(database_id=database_id)
        results = response.get("results", [])

        filas = []
        for row in results:
            props = row["properties"]
            fila = {}
            for key, val in props.items():
                tipo = val["type"]
                if tipo == "title":
                    fila[key] = val["title"][0]["text"]["content"] if val["title"] else ""
                elif tipo == "rich_text":
                    fila[key] = val["rich_text"][0]["text"]["content"] if val["rich_text"] else ""
                elif tipo == "select":
                    fila[key] = val["select"]["name"] if val["select"] else ""
                elif tipo == "multi_select":
                    fila[key] = [v["name"] for v in val["multi_select"]]
                elif tipo == "number":
                    fila[key] = val["number"]
                elif tipo == "checkbox":
                    fila[key] = val["checkbox"]
                elif tipo == "url":
                    fila[key] = val["url"]
                elif tipo == "email":
                    fila[key] = val["email"]
                elif tipo == "people":
                    fila[key] = [p["name"] for p in val["people"]]
                else:
                    fila[key] = None
            filas.append(fila)

        return filas

    except Exception as e:
        logging.error(f"[AXXON] Error al obtener filas de Notion: {e}")
        return []