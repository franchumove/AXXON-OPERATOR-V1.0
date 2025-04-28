"""
AXXON CONSCIOUS - Resonance Tree- resonance_tree.py
---------------------------------
Gestiona las asociaciones simbólicas internas del agente
para mantener coherencia emocional expandida.

Autor: AXXON DevCore
"""

import json
import os

ARS_PATH = "arbol_resonancias.json"

def inicializar_ars():
    """
    Crea estructura inicial del ARS si no existe.
    """
    if not os.path.exists(ARS_PATH):
        ars = {}
        with open(ARS_PATH, "w") as f:
            json.dump(ars, f)

def asociar_conceptos(emocion, concepto):
    """
    Asocia un nuevo concepto a una emoción.
    """
    with open(ARS_PATH, "r") as f:
        ars = json.load(f)

    if emocion not in ars:
        ars[emocion] = []

    ars[emocion].append(concepto)

    with open(ARS_PATH, "w") as f:
        json.dump(ars, f)

def recuperar_asociaciones(emocion):
    """
    Recupera conceptos asociados a una emoción.
    """
    with open(ARS_PATH, "r") as f:
        ars = json.load(f)

    return ars.get(emocion, [])