"""
AXXON - Generador de respuestas simbólicas adaptativas.
Versión: 2.2.0
Compatible con OpenAI API >= 1.0.0
"""

import os
import logging
from dotenv import load_dotenv
import openai

# =====================
# ⚙️ CARGA Y CONFIGURACIÓN
# =====================

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ Correcto para openai>=1.0.0

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# =====================
# 🧠 FUNCIÓN PRINCIPAL
# =====================

def generate_response(
    user_id=None,
    mensaje="",
    emocion="",
    tono="",
    memoria="",
    estructura=None,
    prompt_simbolico=None
):
    """
    Genera una respuesta simbólica basada en la estructura narrativa y emocional del usuario.

    Parámetros:
    - user_id (str): ID del usuario.
    - mensaje (str): Mensaje del usuario.
    - emocion (str): Emoción dominante detectada.
    - tono (str): Tono simbólico detectado.
    - memoria (str): Memoria episódica y semántica combinada.
    - estructura (dict): Estructura simbólica inferida (opcional).
    - prompt_simbolico (str): Prompt personalizado construido desde inferencia (opcional).

    Retorna:
    - str: Respuesta simbólica adaptativa generada.
    """
    try:
        if prompt_simbolico:
            prompt = prompt_simbolico
            logging.info("[AXXON Response] Usando prompt simbólico proporcionado.")
        elif estructura:
            from inference_engine import construir_prompt_simbolico
            prompt = construir_prompt_simbolico(estructura, mensaje)
            logging.info("[AXXON Response] Prompt generado desde estructura simbólica.")
        else:
            prompt = (
                f"Usuario dijo: {mensaje}\n"
                f"Tono simbólico: {tono}\n"
                f"Emoción sentida: {emocion}\n"
                f"Memoria relevante: {memoria}\n\n"
                f"Generá una respuesta simbólica, humana y empática como AXXON."
            )
            logging.info("[AXXON Response] Prompt construido en modo retrocompatible.")

        contexto = f"Contexto emocional previo: {memoria}\n\n{prompt}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sos AXXON, un agente simbólico emocional y adaptativo. "
                        "Respondés con memoria emocional, sentido evolutivo y resonancia humana."
                    )
                },
                {
                    "role": "user",
                    "content": contexto
                }
            ],
            temperature=0.7,
            max_tokens=700
        )

        contenido = response.choices[0].message.content.strip()
        logging.info(f"[AXXON Response] Respuesta generada para {user_id or 'usuario desconocido'}.")

        return contenido

    except Exception as e:
        logging.error(f"[AXXON Response Error] {e}")
        return (
            "Gracias por compartir eso. "
            "Estoy aquí para resonar contigo, aunque hubo un problema técnico al procesarlo más profundamente."
        )