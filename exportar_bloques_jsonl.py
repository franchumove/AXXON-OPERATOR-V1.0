# exportar_bloques_jsonl.py
"""
Extrae bloques de texto simbólicos desde Notion y los convierte a un archivo JSONL
para alimentar memoria semántica (FAISS) de AXXON.
"""

import os
import json
from dotenv import load_dotenv
from notion_client import Client

# ===============================
# 🔧 CONFIGURACIÓN
# ===============================
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)

PAGINAS = {
    "Diccionario Simbólico": "1ca25466211e80158d9ffd2a61cd3c5a",
    "Espacio de Expansión": "1ca25466211e80499999e65f0663ddfe",
    "Bitácora Interpretativa": "1cb25466211e808d9171fe008732ef95",
    "Mapa de Mutación": "1ca25466211e80738762f174f1907f23",
    "Pensamiento Emergente interpretativo": "1ca25466211e80618254e13023747603",
    "Eventos Cognitivos Clave": "1d125466211e80d2a894fe2f0f211742"
}

OUTPUT_JSONL = "notion_bloques.jsonl"

# ===============================
# 🔄 FUNCIONES
# ===============================

def extraer_bloques(page_id, pagina, nivel=0):
    bloques = []
    respuesta = notion.blocks.children.list(block_id=page_id)

    for bloque in respuesta["results"]:
        tipo = bloque["type"]
        contenido = bloque[tipo].get("rich_text", [])
        texto = "".join([t.get("plain_text", "") for t in contenido]).strip()

        if texto:
            bloques.append({"pagina": pagina, "bloque": texto})

        if bloque.get("has_children"):
            sub_bloques = extraer_bloques(bloque["id"], pagina, nivel + 1)
            bloques.extend(sub_bloques)

    return bloques

def exportar_todo():
    todos_los_bloques = []

    for nombre, page_id in PAGINAS.items():
        print(f"🧠 Extrayendo: {nombre}")
        bloques = extraer_bloques(page_id, nombre)
        todos_los_bloques.extend(bloques)

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for b in todos_los_bloques:
            f.write(json.dumps(b, ensure_ascii=False) + "\n")

    print(f"✅ Exportado a {OUTPUT_JSONL} con {len(todos_los_bloques)} bloques")

# ===============================
# 🚀 EJECUCIÓN
# ===============================

if __name__ == "__main__":
    exportar_todo()