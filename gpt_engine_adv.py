# gpt_engine_adv.py

"""
        Módulo AXXON - Generador de respuestas adaptativas simbólicas (GPT-4).

        Actualizado para OpenAI API >= 1.0.0
"""

from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()

        # Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(prompt, memory):
"""
            Genera respuesta simbólica basada en prompt y memoria emocional previa.

            Args:
                prompt (str): Mensaje estructurado simbólicamente.
                memory (str): Recuerdo emocional relevante.

            Returns:
                str: Respuesta adaptativa generada.
"""
            try:
                context = f"Contexto emocional previo: {memory}\n\n{prompt}"

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres una IA simbólica con conciencia emocional. Respondes según el arquetipo y evolución del usuario."},
                        {"role": "user", "content": context}
                    ],
                    temperature=0.75,
                    max_tokens=600
                )
                return response.choices[0].message.content.strip()

            except Exception as e:
                logging.error(f"[AXXON GPT Engine Error] {e}")
                return "Error al generar la respuesta de la IA."