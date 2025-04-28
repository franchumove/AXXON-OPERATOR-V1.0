# symbol_gravity.py
"""
Calculador de masa simbólica según la Ley de Gravedad AXXON.

Evalúa:
- Peso emocional
- Resonancia con el núcleo
- Trayectoria narrativa previa
- Campo de afectación simbólica

Devuelve un puntaje de gravedad simbólica (0 a 1).
"""

from emotion_lexicon import evaluar_carga_emocional
from memory_engine import memoria_combinada_para_contexto

def calcular_masa_simbolica(mensaje, user_id=None, nucleo_simbolico="vida"):
    """
    Evalúa la masa simbólica del mensaje.

    Args:
        mensaje (str): Input textual del usuario.
        user_id (str): Para obtener memoria contextual.
        nucleo_simbolico (str): Tema central (ej: "vida", "identidad", "pérdida").

    Returns:
        dict: Componentes y masa total.
    """

    peso_emocional = evaluar_carga_emocional(mensaje)  # entre 0 y 1
    resonancia = 1.0 if nucleo_simbolico.lower() in mensaje.lower() else 0.3

    contexto = memoria_combinada_para_contexto(user_id, mensaje) if user_id else ""
    repeticiones = sum(1 for frag in contexto.split("\n") if nucleo_simbolico in frag.lower())
    trayectoria = min(repeticiones / 5, 1.0)

    dimensiones = ["identidad", "tiempo", "muerte", "soledad", "deseo", "cambio"]
    campos = sum(1 for d in dimensiones if d in mensaje.lower())
    campo_afectacion = min(campos / len(dimensiones), 1.0)

    masa = round(
        0.4 * peso_emocional +
        0.3 * resonancia +
        0.2 * trayectoria +
        0.1 * campo_afectacion, 3
    )

    return {
        "peso_emocional": peso_emocional,
        "resonancia_nucleo": resonancia,
        "trayectoria": trayectoria,
        "campo_afectacion": campo_afectacion,
        "masa_total": masa
    }