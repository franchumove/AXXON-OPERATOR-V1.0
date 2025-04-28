"""
AXXON - Generador de respuestas adaptativas simbólicas (GPT-4).

Versión: 2.2.0
Compatible con OpenAI API >= 1.0.0
"""

import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# =====================
# CARGA Y CONFIGURACIÓN
# =====================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=None
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# =====================
# FUNCIÓN PRINCIPAL
# =====================

def generate_response(prompt: str, memory: str = "") -> str:
    """
    Genera respuesta simbólica basada en prompt y memoria emocional previa.

    Args:
        prompt (str): Mensaje estructurado simbólicamente.
        memory (str): Contexto emocional previo.

    Returns:
        str: Respuesta adaptativa generada.
    """
    try:
        contexto = f"Contexto emocional previo: {memory}\n\n{prompt}"

        response = client.chat.completions.create(
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
            temperature=0.75,
            max_tokens=700
        )

        generated_text = response.choices[0].message.content.strip()
        logging.info(f"[AXXON GPT Response] Respuesta generada exitosamente.")
        return generated_text

    except Exception as e:
        logging.error(f"[AXXON GPT Engine Error] {e}")
        return "Gracias por tu mensaje. Estoy aquí, aunque tuve un problema al procesarlo profundamente."
