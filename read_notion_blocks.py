import os
import json
from notion_client import Client
from dotenv import load_dotenv

# Cargar variables del entorno (.env)
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# Iniciar cliente de Notion
notion = Client(auth=NOTION_TOKEN)

# Diccionario con nombres y page_ids
PAGINAS = {
    "AXXON — Núcleo Cognitivo / Metaestructura": "1ca25466211e8024aa64e37cea6a9d23",
    "ÓRGANOS COGNITIVOS FUNDACIONALES": "1ca25466211e80ecad8fcd5c3978e7dd",
    "Tablero Adaptativo": "1ca25466211e80518ed4e037305991b5",
    "Diccionario Simbólico": "1ca25466211e80158d9ffd2a61cd3c5a",
    "Pensamiento Emergente interpretativo": "1ca25466211e80618254e13023747603",
    "Espacio de Expansión": "1ca25466211e80499999e65f0663ddfe",
    "Hoja de Ruta Técnica": "1ca25466211e805db74ec6c98de52489",
    "Mapa de Mutación": "1ca25466211e80738762f174f1907f23",
    "Memoria de Casos": "1ca25466211e804cb30beeda9e2d1457",
    "Bitácora Interpretativa": "1cb25466211e808d9171fe008732ef95",
    "Eventos Cognitivos Clave": "1d125466211e80d2a894fe2f0f211742"
}

# Guardar como .txt
def guardar_en_txt(nombre_archivo, contenido):
    with open(f"{nombre_archivo}.txt", "w", encoding="utf-8") as f:
        f.write(contenido)

# Guardar como .jsonl
def guardar_en_jsonl(nombre_archivo, lista_bloques):
    with open(f"{nombre_archivo}.jsonl", "a", encoding="utf-8") as f:
        for bloque in lista_bloques:
            f.write(json.dumps(bloque, ensure_ascii=False) + "\n")

# Función principal
for nombre, page_id in PAGINAS.items():
    print(f"\n\n===== 📘 LEYENDO: {nombre} =====\n")
    contenido_total = []
    bloques_jsonl = []

    def leer_bloques(block_id, nivel=0):
        response = notion.blocks.children.list(block_id=block_id)
        for block in response['results']:
            tipo = block['type']
            indent = "    " * nivel
            texto = ""

            if tipo in ['paragraph', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item']:
                contenido = block[tipo].get('rich_text', [])
                texto = ''.join([t['plain_text'] for t in contenido])
                if texto.strip():
                    icono = {
                        'paragraph': "📝",
                        'heading_1': "🔷",
                        'heading_2': "🔹",
                        'heading_3': "▫️",
                        'bulleted_list_item': "•",
                        'numbered_list_item': "#"
                    }.get(tipo, "🧩")
                    linea = f"{indent}{icono} {texto}"
                    print(linea)
                    contenido_total.append(linea)
                    bloques_jsonl.append({"pagina": nombre, "bloque": linea})

            if block.get("has_children"):
                leer_bloques(block["id"], nivel + 1)

    # Ejecutar lectura por página
    leer_bloques(page_id)

    # Guardar .txt y .jsonl
    guardar_en_txt(nombre.replace(" ", "_").replace("—", "-"), "\n".join(contenido_total))
    guardar_en_jsonl("notion_bloques", bloques_jsonl)

