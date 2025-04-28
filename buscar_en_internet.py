"""
AXXON CORE - Web Search Engine
-------------------------------
Módulo para realizar búsquedas simbólicas en Internet usando SerpAPI (Google Custom Search).

Autor: AXXON DevCore
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def buscar_en_internet(query, num_resultados=3):
    """
    Realiza una búsqueda simbólica en Internet usando SerpAPI.

    Args:
        query (str): Término o pregunta de búsqueda.
        num_resultados (int): Número de resultados deseados.

    Returns:
        list: Lista de resultados relevantes o mensaje de error simbólico.
    """
    if not SERPAPI_KEY:
        raise Exception("Falta SERPAPI_KEY en el archivo .env")

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": num_resultados
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        resultados = response.json().get("organic_results", [])
        links = [{"titulo": r.get("title", "Sin título"), "link": r.get("link", "#")} for r in resultados]
        return links if links else [{"titulo": "No encontré resultados relevantes.", "link": "#"}]
    except requests.RequestException as e:
        print(f"[Buscar Internet] Error en conexión: {e}")
        return [{"titulo": "Hubo un problema al buscar en Internet.", "link": "#"}]
    except Exception as e:
        print(f"[Buscar Internet] Error general: {e}")
        return [{"titulo": "Error inesperado buscando información.", "link": "#"}]

# ======================
# 🧪 Test rápido
# ======================

if __name__ == "__main__":
    resultados = buscar_en_internet("últimas tendencias en inteligencia artificial emocional")
    for r in resultados:
        print(f"🔹 {r['titulo']} - {r['link']}")