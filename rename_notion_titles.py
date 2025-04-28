import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generar_nombre_titulo(texto):
    prompt = f"""Extrae un título simbólico y representativo de máximo 5 palabras para este contenido de una sesión cognitiva:

    Texto: {texto}

    Título:"""

    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return respuesta['choices'][0]['message']['content'].strip()