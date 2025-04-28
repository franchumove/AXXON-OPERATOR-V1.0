"""
module_router.py — Enrutador simbólico de mensajes para AXXON Core

Este módulo distribuye inteligentemente los mensajes recibidos hacia
los distintos módulos simbólicos: emociones, tono, memoria, planificación y respuesta.
"""

import logging

from emocional_detector import detect_emotion
from tono_mapper import determinar_tono
from motive_mapper import mapear_motivos
from symbolic_planner import planificar_ruta_simbolica
from generate_response import generate_response
from logger_jsonl import guardar_log_emocional
from sheet_logger import log_event_simbolico
from memory_engine import guardar_en_sqlite, memoria_combinada_para_contexto

def route_message(user_id: str, mensaje: str, contexto: str = "") -> dict:
    """
    Ruta simbólica central: analiza, interpreta y distribuye un mensaje en AXXON Core.

    Args:
        user_id (str): Identificador simbólico del usuario.
        mensaje (str): Entrada textual a interpretar.
        contexto (str): Contexto o memoria previa (opcional).

    Returns:
        dict: Resultado simbólico con claves: emoción, tono, plan, respuesta.
    """
    try:
        logging.info("[Router] Iniciando ruteo simbólico de mensaje...")

        # 1. Emoción
        emocion = detect_emotion(mensaje)
        logging.info(f"[Router] Emoción detectada: {emocion}")

        # 2. Tono
        tono = determinar_tono(emocion)
        logging.info(f"[Router] Tono interpretativo: {tono}")

        # 3. Motivos simbólicos
        motivadores = mapear_motivos(mensaje)
        logging.info(f"[Router] Motivadores simbólicos: {motivadores}")

        # 4. Contexto combinado
        contexto_completo = contexto or memoria_combinada_para_contexto(user_id, mensaje)

        # 5. Plan simbólico
        ruta = planificar_ruta_simbolica(mensaje)
        logging.info(f"[Router] Ruta simbólica: {ruta}")

        # 6. Respuesta simbólica
        respuesta = generate_response(
            user_id=user_id,
            mensaje=mensaje,
            emocion=emocion,
            tono=tono,
            memoria=contexto_completo
        )

        # 7. Log simbólico
        guardar_en_sqlite(user_id, mensaje, respuesta)
        guardar_log_emocional(user_id, mensaje, emocion, tono, respuesta)

        log_event_simbolico(
            user_id=user_id,
            tipo_evento="casos",
            contenido=f"{mensaje} --> {respuesta}\nPLAN: {ruta}",
            nivel="medio",
            tags=motivadores + [tono, emocion]
        )

        return {
            "emocion": emocion,
            "tono": tono,
            "plan": ruta,
            "respuesta": respuesta
        }

    except Exception as e:
        logging.error(f"[Router] Fallo simbólico en ruteo: {e}", exc_info=True)
        return {"error": f"Fallo en ruteo simbólico: {str(e)}"}