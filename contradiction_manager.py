"""
AXXON CONSCIOUS - Contradiction Manager- contradiction_manager.py
----------------------------------------
Detecta contradicciones entre emociones, memorias o inferencias,
y decide simbólicamente cómo integrarlas.

Autor: AXXON DevCore
"""

def detectar_contradiccion(memoria_actual, nueva_inferencia):
    """
    Detecta si existe contradicción entre memoria actual y nueva inferencia.

    Args:
        memoria_actual (dict): Memoria simbólica previa.
        nueva_inferencia (dict): Nueva estructura simbólica inferida.

    Returns:
        bool: True si hay contradicción relevante, False si son compatibles.
    """
    emociones_actuales = set(memoria_actual.get("emociones", []))
    emociones_nuevas = set(nueva_inferencia.get("emociones", []))

    return not emociones_actuales.isdisjoint(emociones_nuevas) == False

def resolver_contradiccion(memoria_actual, nueva_inferencia):
    """
    Resuelve contradicción simbólica generando integración adaptativa.
    """
    # 🔵 Estrategia simple: fusionar emociones priorizando últimas emociones vividas.
    emociones_fusionadas = list(set(memoria_actual.get("emociones", [])) | set(nueva_inferencia.get("emociones", [])))

    nueva_memoria = {
        "emociones": emociones_fusionadas,
        "contexto": nueva_inferencia.get("contexto", memoria_actual.get("contexto")),
        "ultima_actualizacion": nueva_inferencia.get("timestamp")
    }
    return nueva_memoria