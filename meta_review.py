# meta_review.py
import logging

# Evalúa y corrige respuesta si no está alineada con la narrativa simbólica
def review_response(response, interpreted_prompt):
    reviewed_response = response

    # Si contiene comandos autoritarios, agrega suavizador simbólico
    if "hazlo ya" in response.lower():
        reviewed_response += " (Nota: Evita imperativos. El usuario necesita guía, no presión.)"
        logging.warning(f"Review applied: Removed imperative from response: '{response}' -> '{reviewed_response}'")

    # Si la respuesta es muy corta, sugiere extender
    elif len(response.split()) < 10:
        reviewed_response += " (Extiende tu mensaje con una metáfora o reflexión simbólica.)"
        logging.warning(f"Review applied: Extended short response: '{response}' -> '{reviewed_response}'")

    else:
        logging.info(f"Response passed review: '{response}'")

    return reviewed_response