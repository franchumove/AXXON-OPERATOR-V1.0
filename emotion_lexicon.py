# emotion_lexicon.py
"""
Evaluador simbólico de carga emocional.

Este módulo no solo detecta emociones explícitas, sino que asigna un peso simbólico
en función de la densidad emocional del lenguaje, usando una escala 0.0 - 1.0.

Inspirado en campos como:
- arquetipos jungianos
- afectividad lingüística
- topología emocional de AXXON
"""

import re

# Léxico simbólico base: emoción -> peso entre 0.1 (leve) y 1.0 (crítica)
LEXICO_EMOCIONAL = {
    "muerte": 1.0,
    "desaparecer": 0.9,
    "soledad": 0.8,
    "ansiedad": 0.7,
    "tristeza": 0.6,
    "vacío": 0.5,
    "cansancio": 0.5,
    "duda": 0.4,
    "extrañar": 0.4,
    "esperanza": 0.3,
    "curiosidad": 0.2,
    "alegría": 0.2,
    "paz": 0.1
}

def evaluar_carga_emocional(texto):
    """
    Evalúa el nivel de carga emocional de un texto en función de la presencia simbólica.

    Args:
        texto (str): Mensaje o input a analizar.

    Returns:
        float: Valor entre 0.0 (neutral) y 1.0 (simbólicamente intenso).
    """
    texto = texto.lower()
    total = 0.0
    cuenta = 0

    for palabra, peso in LEXICO_EMOCIONAL.items():
        if re.search(rf"\b{re.escape(palabra)}\b", texto):
            total += peso
            cuenta += 1

    if cuenta == 0:
        return 0.0

    return round(total / cuenta, 3)