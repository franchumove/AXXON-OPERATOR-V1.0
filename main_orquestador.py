"""
AXXON Orquestador Simbólico
Versión unificada y evolutiva - main_orquestador.py
Autor: AXXON DevCore
"""

# ========================
# ⚙️ CARGA Y CONFIGURACIÓN
# ========================

import os
import json
import logging
import schedule
import threading
import time
import uuid
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import OpenAI


# Cargar variables de entorno
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Inicializar servidor Flask y logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Memoria temporal de resúmenes
MEMORIA_RESUMENES = {}

# ========================
# 🔥 MÓDULOS CORE AXXON
# ========================

from generate_response import generate_response
from review_response import revisar_respuesta
from logger_jsonl import guardar_log_emocional
from sheet_logger import log_event_simbolico
from memory_engine import guardar_en_sqlite, memoria_combinada_para_contexto, cargar_y_vectorizar
from exportar_bloques_jsonl import exportar_todo
from evolution_logger import registrar_mutacion
from inference_engine import inferir_estructura_simbolica, construir_prompt_simbolico
from sync_sheet_to_notion import sincronizar_sheet_a_notion
from notion_writer import escribir_en_notion
from notion_fetcher import fetch_table_rows, get_table_id
from db_connection import init_db
from utils.pdf_handler import guardar_como_txt, guardar_como_pdf, subir_a_drive

# ========================
# 🔄 SINCRONIZADOR COGNITIVO
# ========================

def sincronizar_bi_direccional(tipo="casos"):
    try:
        sincronizar_sheet_a_notion(tipo)
        exportar_todo()
        cargar_y_vectorizar()
        logging.info("✅ Memoria simbólica sincronizada entre Sheets, Notion y FAISS.")
    except Exception as e:
        logging.error(f"❌ Error en sincronización simbólica: {e}")

def actualizacion_periodica_notion():
    logging.info("⏳ Actualizando bloques simbólicos desde Notion...")
    try:
        exportar_todo()
        cargar_y_vectorizar()
        logging.info("✅ Bloques simbólicos actualizados.")
    except Exception as e:
        logging.error(f"❌ Error en actualización periódica: {e}")

schedule.every(24).hours.do(actualizacion_periodica_notion)

def correr_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Inicialización temprana
try:
    exportar_todo()
    cargar_y_vectorizar()
except Exception as e:
    logging.warning(f"⚠️ Fallo inicial al cargar memoria simbólica: {e}")

init_db()

# ========================
# 🚀 ENDPOINTS FLASK
# ========================

@app.route("/")
def home():
    return "AXXON Orquestador simbólico vivo."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'message' not in data:
            raise BadRequest("Faltan 'user_id' o 'message' en el payload.")

        user_id = data["user_id"]
        mensaje = data["message"]

        estructura = inferir_estructura_simbolica(user_id, mensaje)
        contexto = memoria_combinada_para_contexto(user_id, mensaje)

        prompt = construir_prompt_simbolico(estructura, mensaje)
        respuesta = generate_response(
            user_id=user_id,
            mensaje=mensaje,
            estructura=estructura,
            memoria=contexto,
            prompt_simbolico=prompt
        )

        review = revisar_respuesta(respuesta, estructura["emocion"], estructura["tono"])

        guardar_en_sqlite(user_id, mensaje, review)

        guardar_log_emocional(
            user_id=user_id,
            mensaje=mensaje,
            emocion=estructura["emocion"],
            tono=estructura["tono"],
            respuesta=review,
            simbolos_implicados=estructura["motivos"],
            plan_narrativo=estructura["plan_simbólico"]
        )

        log_event_simbolico(
            user_id,
            "casos",
            f"{mensaje} --> {review}\nPLAN: {estructura['plan_simbólico']}",
            "medio",
            estructura["motivos"] + [estructura["tono"], estructura["emocion"]]
        )

        registrar_mutacion(
            user_id=user_id,
            tipo="reflexiva",
            descripcion="Mutación simbólica registrada tras inferencia emocional.",
            simbolos=[estructura["tono"]],
            tags=estructura["motivos"]
        )

        sincronizar_bi_direccional("casos")

        return jsonify({
            "response": review,
            "estructura": estructura,
            "prompt": prompt
        })

    except BadRequest as e:
        logging.warning(f"[AXXON Webhook] BadRequest: {e}")
        raise e
    except Exception as e:
        logging.error("[AXXON Webhook] Error crítico:", exc_info=True)
        raise InternalServerError(f"Error simbólico: {e}")

@app.route("/sync-sheet", methods=["GET"])
def sync_sheet():
    try:
        exportar_todo()
        return {"status": "✅ Sincronización exitosa."}
    except Exception as e:
        return {"error": str(e)}

@app.route("/subir-pdf", methods=["POST"])
def subir_pdf():
    try:
        archivo = request.files.get("file")
        if not archivo:
            return {"error": "No se recibió archivo"}, 400

        nombre_base = f"resumen_{uuid.uuid4().hex[:8]}"
        ruta_temporal = f"{nombre_base}_temp.pdf"
        archivo.save(ruta_temporal)

        lector = PdfReader(ruta_temporal)
        texto = "\n".join(p.extract_text() or "" for p in lector.pages)

        respuesta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Resume el siguiente documento en lenguaje claro, simbólico y expandido."},
                {"role": "user", "content": texto}
            ]
        )

        resumen = respuesta.choices[0].message.content.strip()
        MEMORIA_RESUMENES[nombre_base] = resumen

        txt_path = guardar_como_txt(resumen, nombre_base)
        pdf_path = guardar_como_pdf(resumen, nombre_base)

        id_txt = subir_a_drive(txt_path)
        id_pdf = subir_a_drive(pdf_path)

        os.remove(ruta_temporal)

        return {
            "msg": "✅ PDF procesado simbólicamente.",
            "id_txt_drive": id_txt,
            "id_pdf_drive": id_pdf,
            "clave_memoria": nombre_base
        }

    except Exception as e:
        logging.error(f"[AXXON UploadPDF] Error: {e}")
        return {"error": str(e)}

@app.route("/whoami", methods=["GET"])
def whoami():
    return jsonify({
        "yo": "Soy AXXON Core Orquestador.",
        "versión": "v2.1.0",
        "estado": "Activo",
        "identidad": "simbólico-evolutivo"
    })

# ========================
# 🛡️ SERVER RUN
# ========================

if __name__ == "__main__":
    threading.Thread(target=correr_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=5500)