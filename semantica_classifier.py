"""
semantica_classifier.py — Clasificador de ejes semánticos para mensajes simbólicos.

Este módulo interpreta el contenido de un mensaje y lo clasifica según núcleos temáticos relevantes
para AXXON: identidad, vínculo, tiempo, transformación, deseo, etc.
"""

import re

EJES_SEMANTICOS = {
    "identidad": ["soy", "no sé quién", "me reconozco", "mi nombre", "mi esencia"],
    "deseo": ["quiero", "necesito", "anhelo", "me gustaría"],
    "transformación": ["cambio", "transformar", "renacer", "evolucionar"],
    "tiempo": ["pasado", "presente", "futuro", "antes", "después"],
    "introspección": ["siento", "pienso", "reflexiono", "me doy cuenta"],
    "vínculo": ["tú", "nosotros", "conectar", "relación", "abrazo"],
    "miedo": ["temo", "me da miedo", "me asusta", "inseguro"],
    "conflicto": ["peleo", "discuto", "lucho", "tensión"],
    "expansión": ["crecer", "expandirme", "ir más allá", "explorar"],
    "caída": ["me derrumbo", "fracaso", "no puedo más", "me apago"]
}

def clasificar_semantica(mensaje: str) -> list:
    """
    Detecta los ejes semánticos principales presentes en un mensaje.

    Args:
        mensaje (str): Entrada textual del usuario.

    Returns:
        list: Lista de categorías semánticas detectadas.
    """
    mensaje = mensaje.lower()
    encontrados = []

    for eje, palabras_clave in EJES_SEMANTICOS.items():
        for palabra in palabras_clave:
            if palabra in mensaje:
                encontrados.append(eje)
                break  # Evitar duplicados

    return list(set(encontrados))

# Prueba directa
if __name__ == "__main__":
    texto = "Quiero crecer, pero me asusta lo que podría descubrir de mí misma."
    resultado = clasificar_semantica(texto)
    print(f"Ejes semánticos detectados: {resultado}")