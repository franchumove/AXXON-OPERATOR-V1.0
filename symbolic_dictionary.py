"""
    symbolic_dictionary.py — Diccionario simbólico vivo desde Sheets y Notion.

    Accede dinámicamente a expresiones simbólicas registradas en Google Sheets y Notion,
    y las convierte en campos arquetípicos operativos para AXXON Core.

    Usa:
    - Notion: estructura expandida de campos simbólicos y arquetipos.
    - Sheets: campos activos, resonancias y energías actualizadas por observadores humanos.
"""

import logging
from sheet_logger import connect_to_sheets
from notion_fetcher import fetch_table_rows, get_table_id

    # ===========================
    # Sheet Config (Memoria de Diccionario Vivo)
    # ===========================

SHEET_NAME = "AXXON CORE"
TAB_DICCIONARIO = "Diccionario Vivo"

def cargar_diccionario_desde_sheet():
        try:
            client = connect_to_sheets()
            sheet = client.open(SHEET_NAME)
            worksheet = sheet.worksheet(TAB_DICCIONARIO)
            rows = worksheet.get_all_records()
            logging.info(f"[SimbolicDict] {len(rows)} símbolos cargados desde Sheets.")
            return {
                row["símbolo"].strip().lower(): {
                    "campo": row.get("campo", "desconocido"),
                    "energía": row.get("energía", "neutra"),
                    "arquetipo": row.get("arquetipo", "indeterminado")
                } for row in rows if row.get("símbolo")
            }
        except Exception as e:
            logging.warning(f"[SimbolicDict] Error al cargar desde Sheets: {e}")
            return {}

    # ===========================
    # Notion Config (Estructura base de simbolismo)
    # ===========================

NOTION_ALIAS = "diccionario_simbolico_1"

def cargar_diccionario_desde_notion():
        try:
            db_id = get_table_id(NOTION_ALIAS)
            rows = fetch_table_rows(db_id)
            logging.info(f"[SimbolicDict] {len(rows)} símbolos cargados desde Notion.")
            simbolos = {}
            for row in rows:
                props = row.get("properties", {})
                simbolo = props.get("Símbolo", {}).get("title", [{}])[0].get("text", {}).get("content", "").lower()
                if simbolo:
                    simbolos[simbolo] = {
                        "campo": props.get("Campo", {}).get("select", {}).get("name", "desconocido"),
                        "energía": props.get("Energía", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "neutra"),
                        "arquetipo": props.get("Arquetipo", {}).get("select", {}).get("name", "indeterminado")
                    }
            return simbolos
        except Exception as e:
            logging.warning(f"[SimbolicDict] Error al cargar desde Notion: {e}")
            return {}

    # ===========================
    # Interpretación simbólica
    # ===========================

def escanear_texto(texto, fuente="sheet"):
        texto = texto.lower()
        base = cargar_diccionario_desde_sheet() if fuente == "sheet" else cargar_diccionario_desde_notion()
        detectados = []
        for simbolo, atributos in base.items():
            if simbolo in texto:
                detectados.append({simbolo: atributos})
        return detectados

    # ===========================
    # Test directo
    # ===========================

if __name__ == "__main__":
        frase = "A veces siento fuego y sombra, como un eco de mi interior."
        sheet = escanear_texto(frase, fuente="sheet")
        notion = escanear_texto(frase, fuente="notion")
        print("\n[Desde Sheet]", sheet)
        print("\n[Desde Notion]", notion)