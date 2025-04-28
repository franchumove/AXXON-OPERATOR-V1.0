# embedding_engine_adv.py

"""
Módulo AXXON - Motor de generación y búsqueda de embeddings simbólicos.

Actualizado para OpenAI API >= 1.0.0

Versión: 2.1.0
Autor: Francois Fillette
"""

import os
import logging
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def generar_embedding(texto: str, model: str = "text-embedding-ada-002") -> list:
    """
    Genera un embedding vectorial desde un texto dado.

    Args:
        texto (str): Texto a vectorizar.
        model (str): Modelo de embeddings de OpenAI.

    Returns:
        list: Vector de embedding.
    """
    try:
        response = client.embeddings.create(
            model=model,
            input=texto
        )
        embedding = response.data[0].embedding
        logging.info(f"[AXXON Embedding] Embedding generado exitosamente.")
        return embedding
    except Exception as e:
        logging.error(f"[AXXON Embedding Error] {e}")
        return []


def calcular_similitud(vector_a: list, vector_b: list) -> float:
    """
    Calcula la similitud coseno entre dos embeddings.

    Args:
        vector_a (list): Primer embedding.
        vector_b (list): Segundo embedding.

    Returns:
        float: Valor de similitud entre -1 y 1.
    """
    try:
        a = np.array(vector_a)
        b = np.array(vector_b)
        similitud = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        return similitud
    except Exception as e:
        logging.error(f"[AXXON Similarity Error] {e}")
        return 0.0


def buscar_mas_cercano(embedding_consulta: list, memoria_embeddings: dict, umbral: float = 0.75) -> dict:
    """
    Busca el mensaje más similar en la memoria simbólica.

    Args:
        embedding_consulta (list): Embedding del nuevo mensaje.
        memoria_embeddings (dict): Diccionario {id: embedding}.
        umbral (float): Similitud mínima aceptada.

    Returns:
        dict: {'id': id_mensaje, 'similitud': valor}
    """
    mejor_id = None
    mejor_similitud = -1

    for id_mensaje, emb_mem in memoria_embeddings.items():
        similitud = calcular_similitud(embedding_consulta, emb_mem)
        if similitud > mejor_similitud and similitud >= umbral:
            mejor_similitud = similitud
            mejor_id = id_mensaje

    return {"id": mejor_id, "similitud": mejor_similitud}


# Test rápido
if __name__ == "__main__":
    consulta = "Quiero encontrar el sentido a este cambio."
    ejemplo_memoria = {
        "1": generar_embedding("Todo cambio trae nuevas posibilidades."),
        "2": generar_embedding("Hoy me siento vacío."),
        "3": generar_embedding("Las transformaciones duelen al principio.")
    }
    emb_consulta = generar_embedding(consulta)
    resultado = buscar_mas_cercano(emb_consulta, ejemplo_memoria)
    print(f"Resultado de búsqueda: {resultado}")