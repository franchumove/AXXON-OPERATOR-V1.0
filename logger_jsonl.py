# logger_jsonl.py

"""
AXXON - Registro emocional simbólico en formato .jsonl

Este módulo guarda interacciones clave para entrenamiento reflexivo y análisis simbólico posterior.
Cada entrada incluye:
- user_id
- mensaje recibido
- emoción detectada
- tono asignado
- respuesta generada
- fuente (e.g., webhook, test, batch)
- categoría (e.g., interacción, mutación, contradicción)

Este log puede ser usado para:
- Evaluación de estilo narrativo
- Entrenamiento de IA simbólica interna
- Visualización de evolución emocional

Autor: AXXON DevCore
"""

import json
from datetime import datetime
import os

LOG_PATH = "logs_emocionales.jsonl"

def guardar_log_emocional(
    user_id,
    mensaje,
    emocion,
    tono,
    respuesta,
    fuente="webhook",
    categoria="interaccion",
    simbolos_implicados=None,
    plan_narrativo=None
):
    """
    Guarda un evento emocional simbólico como entrada .jsonl

    Args:
        user_id (str): ID simbólico del usuario.
        mensaje (str): Mensaje recibido.
        emocion (str): Emoción principal detectada.
        tono (str): Tono narrativo dominante.
        respuesta (str): Respuesta generada por AXXON.
        fuente (str): Origen del evento (webhook, test, etc.).
        categoria (str): Tipo de evento (interaccion, mutacion, etc.).
        simbolos_implicados (list): Lista opcional de símbolos clave.
        plan_narrativo (str): Ruta simbólica o intención narrativa aplicada.
    """
    evento = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "fuente": fuente,
        "categoria": categoria,
        "mensaje": mensaje,
        "emocion": emocion,
        "tono": tono,
        "respuesta": respuesta,
        "simbolos": simbolos_implicados or [],
        "plan": plan_narrativo or ""
    }

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[logger_jsonl] Error al guardar evento: {e}")