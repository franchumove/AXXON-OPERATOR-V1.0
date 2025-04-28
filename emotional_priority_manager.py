"""
AXXON CONSCIOUS - Emotional Priority Manager- emotional_priority_manager.py
---------------------------------------------
Maneja los pesos simbólicos de emociones según interacciones
para modificar adaptativamente el comportamiento.

Autor: AXXON DevCore
"""

import json
import os

PESOS_EMOCIONALES_PATH = "pesos_emocionales.json"

def inicializar_pesos():
    """
    Crea archivo inicial de pesos emocionales si no existe.
    """
    if not os.path.exists(PESOS_EMOCIONALES_PATH):
        pesos = {
            "alegría": 1.0,
            "tristeza": 1.0,
            "miedo": 1.0,
            "ira": 1.0,
            "inspiración": 1.0
        }
        with open(PESOS_EMOCIONALES_PATH, "w") as f:
            json.dump(pesos, f)

def actualizar_peso_emocion(emocion, incremento=0.1):
    """
    Aumenta el peso simbólico de una emoción tras interacción.
    """
    with open(PESOS_EMOCIONALES_PATH, "r") as f:
        pesos = json.load(f)

    if emocion in pesos:
        pesos[emocion] += incremento
    else:
        pesos[emocion] = 1.0 + incremento

    with open(PESOS_EMOCIONALES_PATH, "w") as f:
        json.dump(pesos, f)

def obtener_emocion_prioritaria():
    """
    Devuelve la emoción con mayor peso actual.
    """
    with open(PESOS_EMOCIONALES_PATH, "r") as f:
        pesos = json.load(f)

    return max(pesos, key=pesos.get)