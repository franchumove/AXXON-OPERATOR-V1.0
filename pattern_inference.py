"""
pattern_inference.py — Inferencia de patrones simbólicos en lenguaje natural.

Este módulo detecta estructuras narrativas arquetípicas en los mensajes del usuario.
Ej: contradicciones, repeticiones, reinicios, invocaciones simbólicas, etc.
"""

import re

PATRONES_SIMBOLICOS = {
    "contradiccion": r"\b(pero|aunque|sin embargo|no obstante)\b",
    "reinicio": r"(comenzar de nuevo|empezar otra vez|todo desde cero)",
    "bucle": r"(siempre\s.*\s(mismo|igual))|(una y otra vez)",
    "invocacion": r"(encontrar mi|descubrir mi|reconectar con|despertar el)",
    "ambivalencia": r"(quiero.*pero.*)|(tengo.*pero.*)",
    "confesion": r"(nunca lo dije|nunca lo hablé|necesito contarlo)",
    "urgencia simbólica": r"(ya no puedo|esto tiene que cambiar|es ahora o nunca)"
}

def inferir_patrones_simbolicos(mensaje: str) -> list:
    """
    Detecta patrones narrativos simbólicos en un mensaje.

    Args:
        mensaje (str): Texto del usuario.

    Returns:
        list: Lista de etiquetas de patrones encontrados.
    """
    mensaje = mensaje.lower()
    patrones_detectados = []

    for etiqueta, patron in PATRONES_SIMBOLICOS.items():
        if re.search(patron, mensaje):
            patrones_detectados.append(etiqueta)

    return patrones_detectados

# Prueba directa
if __name__ == "__main__":
    prueba = "Siempre vuelvo al mismo lugar, pero esta vez necesito encontrar mi fuego interior."
    patrones = inferir_patrones_simbolicos(prueba)
    print(f"Patrones detectados: {patrones}")