# emocional_detector.py

"""
Órgano de Percepción Emocional de AXXON Core.

Detecta emoción dominante en un mensaje usando NLP.
Modelo base: DistilBERT fine-tuned para clasificación emocional.
Adaptado al diccionario emocional AXXON para integración narrativa.

Autor: Francois Fillette
"""

from transformers import pipeline
import logging

# Inicialización del pipeline de clasificación emocional
try:
    emotion_classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=False
    )
except Exception as e:
    logging.error(f"[AXXON - EmotionDetector] Fallo al cargar modelo: {e}")
    emotion_classifier = None

def detect_emotion(message: str) -> str:
    """
    Detecta la emoción principal de un mensaje en lenguaje natural.

    Args:
        message (str): Texto del usuario.

    Returns:
        str: Emoción dominante (ajustada al mapa emocional simbólico AXXON).
    """
    if not emotion_classifier:
        return "indefinida"

    try:
        result = emotion_classifier(message)[0]
        label = result["label"].lower()

        # Mapeo simbólico AXXON
        emotion_map = {
            "joy": "alegría",
            "anger": "enojo",
            "sadness": "tristeza",
            "fear": "miedo",
            "disgust": "rechazo",
            "surprise": "sorpresa",
            "neutral": "neutralidad",
            "love": "afecto"
        }

        return emotion_map.get(label, label)

    except Exception as e:
        logging.error(f"[AXXON - EmotionDetector] Error al detectar emoción: {e}")
        return "indefinida"

# Prueba directa
if __name__ == "__main__":
    mensaje = "Estoy muy decepcionado con lo que pasó"
    emocion = detect_emotion(mensaje)
    print(f"Emoción detectada: {emocion}")