# axxon_inference.py
import logging
import requests

# Simulación de lectura técnica desde Drive o Notion (reemplazar por fuentes reales)
def get_technical_knowledge():
    try:
        drive_url = "https://drive.google.com/uc?id=TU_ID_AQUI&export=download"  # <- reemplazar
        response = requests.get(drive_url)
        if response.status_code == 200:
            return response.text[:1000]  # Limita para que no sature el prompt
        else:
            return ""
    except Exception as e:
        logging.error(f"Error retrieving technical knowledge: {e}")
        return ""

def interpret_message(message, archetype, emotion, memory):
    base = ""
    if archetype == "Guerrero":
        base = "Estrategia y coraje ante la duda."
    elif archetype == "Sabio":
        base = "Observa sin juicio y responde desde la introspección."
    elif archetype == "Explorador":
        base = "Activa el deseo de descubrir desde lo incierto."
    elif archetype == "Mago":
        base = "Transmuta lo caótico en posibilidad."
    elif archetype == "Huérfano":
        base = "Reconoce el dolor como guía narrativa."
    else:
        base = "Encuentra el símbolo detrás del síntoma."

    technical_knowledge = get_technical_knowledge()

    interpreted_message = f"{base}\n\nMensaje: {message}\n\nPerfil emocional: {emotion}\nMemoria simbólica: {memory}\n\nBase técnica relevante:\n{technical_knowledge}"
    logging.info(f"Interpreted message: '{interpreted_message}'")
    return interpreted_message