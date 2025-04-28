"""
    review_response.py

    Módulo de evaluación de respuesta simbólica:
    - Evalúa si la emoción y el tono están presentes en la respuesta generada.
    - Calcula un índice de autoconciencia narrativa y adaptativa.
    - Puede expandirse para evaluar metáforas, coherencia y lenguaje espejo.

    Autor: AXXON DevCore
"""

def revisar_respuesta(respuesta, emocion, tono):
        reflexiones = []
        score = 0

        if not respuesta:
            return {
                "reflexion": ["❌ Respuesta vacía o fallida. No se puede evaluar."],
                "score": 0,
                "max_score": 4,
                "autoconciencia": "nula"
            }

        # 1. Evaluación emocional explícita
        if emocion and emocion.lower() in respuesta.lower():
            reflexiones.append(f"✅ La emoción '{emocion}' está explícitamente presente.")
            score += 1
        else:
            reflexiones.append(f"👀 La emoción '{emocion}' no fue nombrada. Puede estar implícita.")

        # 2. Evaluación de tono narrativo
        if tono and tono.lower() in respuesta.lower():
            reflexiones.append(f"✅ El tono '{tono}' está bien reflejado.")
            score += 1
        else:
            reflexiones.append(f"🔍 El tono '{tono}' no está explícito. Evaluar reformulación.")

        # 3. Presencia de impulso emocional afirmativo
        if any(f in respuesta.lower() for f in ["tú puedes", "ánimo", "confía", "te acompaño"]):
            reflexiones.append("🌱 Se incluye impulso afirmativo. Buen refuerzo emocional.")
            score += 1

        # 4. Presencia de estímulo introspectivo o reflexivo
        if any(f in respuesta.lower() for f in ["reflexiona", "piensa", "observá", "considerá"]):
            reflexiones.append("🧠 Hay llamado a introspección. Apoya autoconciencia.")
            score += 1

        autoconciencia = (
            "alta" if score >= 3 else
            "media" if score == 2 else
            "baja" if score == 1 else
            "nula"
        )

        return {
            "reflexion": reflexiones,
            "score": score,
            "max_score": 4,
            "autoconciencia": autoconciencia
        }