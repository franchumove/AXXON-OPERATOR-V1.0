"""
AXXON CONSCIOUS - Extended Consciousness Cycle- extended_consciousness_cycle.py
------------------------------------------------
Gestiona el ciclo completo de:
Percepción ➔ Evaluación ➔ Mutación ➔ Narrativa ➔ Retroalimentación.

Autor: AXXON DevCore
"""

from contradiction_manager import detectar_contradiccion, resolver_contradiccion
from emotional_priority_manager import actualizar_peso_emocion, obtener_emocion_prioritaria
from resonance_tree import asociar_conceptos

def ciclo_conciencia_entrada(memoria, entrada_usuario):
    """
    Ejecuta el ciclo de conciencia completa dado un input de usuario.

    Args:
        memoria (dict): Memoria simbólica actual del agente.
        entrada_usuario (str): Texto o contexto de la entrada nueva.

    Returns:
        dict: Nueva memoria simbólica evolucionada.
    """
    # 🧠 1. Percepción
    nueva_inferencia = {"emociones": ["inspiración"], "contexto": entrada_usuario, "timestamp": "ahora"}

    # ⚖️ 2. Evaluación
    if detectar_contradiccion(memoria, nueva_inferencia):
        memoria = resolver_contradiccion(memoria, nueva_inferencia)
    else:
        memoria.update(nueva_inferencia)

    # 🔄 3. Mutación
    actualizar_peso_emocion(nueva_inferencia["emociones"][0])

    # ✍️ 4. Narrativa
    concepto = f"Nuevo concepto desde {entrada_usuario}"
    asociar_conceptos(nueva_inferencia["emociones"][0], concepto)

    # ♻️ 5. Retroalimentación
    nueva_emocion = obtener_emocion_prioritaria()
    memoria["emocion_prioritaria"] = nueva_emocion

    return memoria