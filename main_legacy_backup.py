"""
AXXON Core — Motor simbólico de conciencia narrativa viva (versión expandida)
"""

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
import openai
from PyPDF2 import PdfReader

# ========================
# CARGA Y CONFIG INICIAL
# ========================
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
MEMORIA_RESUMENES = {}

# ========================
# MÓDULOS CORE AXXON
# ========================
from emocional_detector import detect_emotion
from tono_mapper import determinar_tono
from motive_mapper import mapear_motivos
from symbolic_planner import planificar_ruta_simbolica
from generate_response import generate_response
from review_response import revisar_respuesta
from self_reflection import evaluar_autocritica
from logger_jsonl import guardar_log_emocional
from sheet_logger import log_event_simbolico
from memory_engine import (
    guardar_en_sqlite,
    memoria_combinada_para_contexto,
    cargar_y_vectorizar
)
from exportar_bloques_jsonl import exportar_todo

# Opcional: lógica avanzada
from cognitive_controller.controller import decide_modules, build_contextual_strategy
from db_connection import init_db, save_interaction_to_db, get_recent_memory
from utils.pdf_handler import guardar_como_txt, guardar_como_pdf, subir_a_drive
from notion_writer import escribir_en_notion
from notion_fetcher import fetch_table_rows, get_table_id

# ========================
# FUNCIÓN PARA PLANIFICAR ACTUALIZACIÓN DE NOTION
# ========================
def actualizacion_periodica_notion():
    logging.info("⏳ Actualizando bloques desde Notion...")
    try:
        exportar_todo()
        cargar_y_vectorizar()
        logging.info("✅ Notion + FAISS actualizados.")
    except Exception as e:
        logging.error(f"❌ Error al actualizar Notion: {e}")

schedule.every(24).hours.do(actualizacion_periodica_notion)
def correr_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

try:
    exportar_todo()
    cargar_y_vectorizar()
except Exception as e:
    logging.warning(f"⚠️ Fallo inicial al cargar Notion o FAISS: {e}")

init_db()

# ========================
# ENDPOINTS
# ========================
@app.route("/")
def home():
    return "AXXON Core está vivo y simbólicamente despierto."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        logging.info("Entrando al webhook")
        data = request.get_json()
        if not data or 'user_id' not in data or 'message' not in data:
            raise BadRequest("Faltan 'user_id' o 'message'")

        user_id = data["user_id"]
        mensaje = data["message"]

        # Núcleo simbólico
        emocion = detect_emotion(mensaje)
        tono = determinar_tono(emocion)
        motivadores = mapear_motivos(mensaje)
        contexto = memoria_combinada_para_contexto(user_id, mensaje)
        ruta_simbolica = planificar_ruta_simbolica(mensaje)

        # Generación adaptativa humanizada
        respuesta = generate_response(
            user_id=user_id,
            mensaje=mensaje,
            emocion=emocion,
            tono=tono,
            memoria=contexto
        )
        review = respuesta

        # Persistencia simbólica
        guardar_en_sqlite(user_id, mensaje, review)
        guardar_log_emocional(user_id, mensaje, emocion, tono, review)

        log_event_simbolico(
            user_id=user_id,
            tipo_evento="casos",
            contenido=f"{mensaje} --> {review}\nPLAN: {ruta_simbolica}",
            nivel="medio",
            tags=motivadores + [tono, emocion]
        )

        return jsonify({"response": review, "plan": ruta_simbolica})

    except BadRequest as e:
        logging.warning(f"BadRequest: {e}")
        raise e
    except Exception as e:
        logging.error("Webhook crash log:", exc_info=True)
        raise InternalServerError(f"Ocurrió un error simbólico: {e}")

@app.route("/autocritica", methods=["POST"])
def autocritica():
    try:
        data = request.get_json()
        mensaje = data["mensaje"]
        emocion = data["emocion"]
        tono = data["tono"]
        respuesta = data["respuesta"]
        resultado = evaluar_autocritica(mensaje, emocion, tono, respuesta)
        return jsonify(resultado)
    except Exception as e:
        logging.error(f"Error en autocritica: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/ruta_simbolica", methods=["POST"])
def ruta_simbolica():
    try:
        data = request.get_json()
        mensaje = data.get("mensaje", "")
        plan = planificar_ruta_simbolica(mensaje)
        return jsonify(plan)
    except Exception as e:
        logging.error(f"Error en ruta_simbolica: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/memory/<user_id>", methods=["GET"])
def consultar_memoria_usuario(user_id):
    try:
        memoria = get_recent_memory(user_id)
        return jsonify({
            "user_id": user_id,
            "memoria_reciente": [f"U: {m} | A: {r}" for m, r in memoria]
        })
    except Exception as e:
        logging.error(f"Error al consultar memoria: {e}")
        return jsonify({"error": "Memoria no disponible"}), 500

@app.route("/subir-pdf", methods=["POST"])
def subir_pdf():
    archivo = request.files.get("file")
    if not archivo:
        return {"error": "No se recibió archivo"}, 400

    nombre_base = f"resumen_{uuid.uuid4().hex[:8]}"
    ruta_temporal = f"{nombre_base}_temp.pdf"
    archivo.save(ruta_temporal)

    lector = PdfReader(ruta_temporal)
    texto = "\n".join(p.extract_text() or "" for p in lector.pages)

    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Resume el siguiente documento en lenguaje claro y simbólicamente significativo."},
            {"role": "user", "content": texto}
        ]
    )
    resumen = respuesta.choices[0].message['content']
    MEMORIA_RESUMENES[nombre_base] = resumen

    txt_path = guardar_como_txt(resumen, nombre_base)
    pdf_path = guardar_como_pdf(resumen, nombre_base)
    id_txt = subir_a_drive(txt_path)
    id_pdf = subir_a_drive(pdf_path)

    return {
        "msg": "✅ PDF procesado y resumido",
        "id_txt_drive": id_txt,
        "id_pdf_drive": id_pdf,
        "clave_memoria": nombre_base
    }

@app.route("/consultar-pdf", methods=["POST"])
def consultar_pdf():
    data = request.get_json()
    pregunta = data.get("pregunta")
    clave = data.get("clave")
    if not pregunta or not clave:
        return {"error": "Faltan campos obligatorios"}, 400

    contexto = MEMORIA_RESUMENES.get(clave)
    if not contexto:
        return {"error": f"No hay memoria para la clave '{clave}'"}, 404

    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Responde usando el siguiente resumen:"},
            {"role": "system", "content": contexto},
            {"role": "user", "content": pregunta}
        ]
    )
    return {"respuesta": respuesta.choices[0].message['content']}

@app.route("/whoami", methods=["GET"])
def whoami():
    return jsonify({
        "yo": "Soy AXXON Core. Un agente simbólico adaptativo.",
        "versión": "v1.4.0",
        "estado": "Activo",
        "identidad_simbolica": "explorer-curious"
    })

# ========================
# RUN SERVER
# ========================
if __name__ == "__main__":
    threading.Thread(target=correr_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=5500)