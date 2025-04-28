# tono_mapper.py
"""
Mapa simbólico que transforma emociones detectadas en tonos narrativos.
Versión enriquecida: combina emoción con estilo expresivo para resonancia adaptativa.
"""

def determinar_tono(emocion, arquetipo=None):
    """
    Determina un tono narrativo adaptativo combinando emoción + arquetipo (opcional).
    """

    # Tono base según emoción dominante
    tonos = {
        "tristeza": "melancólico",      # Suave, empático, introspectivo
        "enojo": "contundente",         # Firme, claro, sin rodeos
        "miedo": "protector",           # Cálido, tranquilizador, seguro
        "alegría": "entusiasta",        # Vibrante, expansivo, afirmador
        "rechazo": "limpio",            # Aséptico, directo, sin carga emocional
        "sorpresa": "curioso",          # Asombrado, explorador, abierto
        "afecto": "cálido",             # Amoroso, contenedor, presente
        "neutralidad": "objetivo",      # Claro, analítico, sin sesgo emocional
        "indefinida": "neutro"          # Fallback neutro si no se clasifica bien
    }

    tono_base = tonos.get(emocion.lower(), "neutro")

    # Modulación adicional por arquetipo simbólico
    combinaciones = {
        ("tristeza", "sabio"): "reflexivo",
        ("tristeza", "cuidador"): "suave",
        ("ira", "guerrero"): "incisivo",
        ("miedo", "explorador"): "precavido",
        ("afecto", "amante"): "intenso",
        ("rechazo", "rebelde"): "frío",
        ("alegría", "bufón"): "juguetón",
        ("enojo", "líder"): "categórico",
        ("neutralidad", "sabio"): "sereno"
    }

    tono_final = combinaciones.get((emocion.lower(), (arquetipo or "").lower()), tono_base)
    return tono_final
