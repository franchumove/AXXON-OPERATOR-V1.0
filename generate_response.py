# generate_response.py

"""
Módulo AXXON - Generador de respuestas simbólicas adaptativas.

Compatible con OpenAI API >= 1.0.0
"""

import logging
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def generate_response(
    user_id=None,
    mensaje="",
    emocion="",
    tono="",
    memoria="",
    estructura=None,
    prompt_simbolico=None
):
    """Genera una respuesta simbólica basada en estructura narrativa y emocional."""
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

        # Generación de respuesta con cliente moderno
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sos AXXON, un agente simbólico emocional y adaptativo. "
                        "Respondé con calidez, sentido, memoria emocional y contención narrativa."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
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
        return "Gracias por compartir eso. Estoy aquí y lo recibo, aunque hubo un problema técnico al procesar más profundamente."