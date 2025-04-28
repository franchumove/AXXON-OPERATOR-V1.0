"""
sync_inferer.py — Motor de inferencia sincronizada para AXXON

Evalúa la coherencia simbólica entre:
- mensaje original
- emoción detectada
- tono aplicado
- memoria evocada
- respuesta generada

Detecta disonancias y propone ajustes simbólicos o alertas.
"""

from difflib import SequenceMatcher

def evaluar_coherencia_simbólica(mensaje, emocion, tono, memoria, respuesta):
    """
    Evalúa el alineamiento semántico y emocional entre los componentes simbólicos.

    Args:
        mensaje (str): Input original del usuario.
        emocion (str): Emoción detectada.
        tono (str): Tono simbólico aplicado.
        memoria (str): Memoria relevante traída del usuario.
        respuesta (str): Respuesta generada por el sistema.

    Returns:
        dict: Resultado de la evaluación con nivel de coherencia, alerta y recomendación.
    """

    def similitud(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    score_memo = similitud(mensaje, memoria)
    score_resp = similitud(mensaje, respuesta)

    alerta = None
    if score_resp < 0.3 and emocion in ["tristeza", "confusión"]:
        alerta = "Posible desconexión entre emoción detectada y respuesta generada."

    if score_memo < 0.2:
        alerta = "Memoria recuperada poco relevante al mensaje actual."

    if emocion == "ira" and tono in ["suave", "contemplativo"]:
        alerta = "Tono aplicado podría ser inadecuado para emoción intensa."

    return {
        "coherencia_mensaje_memoria": round(score_memo, 2),
        "coherencia_mensaje_respuesta": round(score_resp, 2),
        "alerta": alerta,
        "recomendacion": "Revisar respuesta o ajustar tono" if alerta else "Sin anomalías detectadas"
    }

# Prueba simbólica directa
if __name__ == "__main__":
    resultado = evaluar_coherencia_simbólica(
        mensaje="Estoy cansado de repetir lo mismo",
        emocion="frustración",
        tono="contemplativo",
        memoria="Últimos registros muestran esperanza y calma.",
        respuesta="Recuerda que siempre puedes volver a empezar."
    )
    print("[SYNC INFERER TEST]", resultado)