"""
                AXXON - Generador de respuestas adaptativas simbólicas (GPT-4).
                Versión: 2.2.1 - gpt_engine_adv.py
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

def generate_response(prompt: str, memory: str = "") -> str:
                    """
                    Genera respuesta simbólica basada en prompt y memoria previa.

                    Parámetros:
                    - prompt (str): Pregunta o situación simbólica planteada.
                    - memory (str): Contexto emocional y simbólico acumulado.

                    Retorna:
                    - str: Respuesta simbólica adaptativa.
                    """
                    try:
                        contexto = f"Contexto emocional previo: {memory}\n\n{prompt}"

                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "Sos AXXON, un agente simbólico emocional, narrativo y adaptativo. "
                                        "Respondés con profundidad emocional, expansión simbólica y eco humano."
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

                        return response.choices[0].message.content.strip()

                    except Exception as e:
                        logging.error(f"[AXXON GPT Engine Adv Error] {e}")
                        return (
                            "Estoy aquí para resonar con tu mensaje. "
                            "Ocurrió un error técnico, pero sigo acompañándote simbólicamente."
                        )