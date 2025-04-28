"""
self_reflection.py
Módulo de autocrítica simbólica para AXXON

Evalúa si la respuesta generada es coherente con:
- La emoción detectada
- El tono mapeado
- La memoria reciente

Retorna una reflexión simbólica o puntuación de autoconciencia.
"""

import re

# Diccionario de expectativas por tono
TONO_EXPECTATIVAS = {
    "protector": ["acompañar", "tranquilidad", "seguridad", "no estás sola", "confía"],
    "motivador": ["puedes", "adelante", "confía", "avance", "reto"],
    "explorador": ["curioso", "descubrir", "camino", "mapa", "mirá esto"],
    "analítico": ["perspectiva", "causa", "reflexionemos", "estructura", "datos"],
    "neutral": []
}

def evaluar_autocritica(mensaje, emocion, tono, respuesta):
    """
    Evalúa si el tono y contenido de la respuesta reflejan bien la emoción y mensaje.
    Retorna un dict con reflexión simbólica.
    """
    reflexiones = []
    score = 0

    # 1. Chequeo de tono esperado
    esperados = TONO_EXPECTATIVAS.get(tono, [])
    if esperados:
        hits = sum(1 for palabra in esperados if palabra.lower() in respuesta.lower())
        score += hits
        if hits == 0:
            reflexiones.append(f"⚠️ No se detectó lenguaje esperado para el tono '{tono}'.")
        elif hits < len(esperados) // 2:
            reflexiones.append(f"🔸 Solo parcialmente se refleja el tono '{tono}'.")
        else:
            reflexiones.append(f"✅ El tono '{tono}' está bien reflejado.")
    else:
        reflexiones.append(f"ℹ️ Tono '{tono}' no tiene criterios definidos aún.")

    # 2. Chequeo de contradicción emocional
    if emocion.lower() in respuesta.lower():
        reflexiones.append(f"🧠 La emoción '{emocion}' fue nombrada explícitamente en la respuesta.")
        score += 1
    else:
        reflexiones.append(f"👀 La emoción '{emocion}' no fue nombrada. Puede ser implícita.")

    # 3. Chequeo de introspección
    if re.search(r"\b(reflexion|profundo|entender|comprender|mirada)\b", respuesta.lower()):
        score += 1
        reflexiones.append("🔍 Se detecta lenguaje introspectivo.")

    return {
        "score": score,
        "max_score": len(esperados) + 2,
        "reflexion": reflexiones,
        "autoconciencia": "alta" if score >= 3 else "media" if score >= 1 else "baja"
    }

# Prueba simbólica directa
if __name__ == "__main__":
    out = evaluar_autocritica(
        mensaje="Me siento confundida y frágil",
        emocion="tristeza",
        tono="protector",
        respuesta="No estás sola. Acompañarte en este camino es lo importante."
    )
    from pprint import pprint
    pprint(out)