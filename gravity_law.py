"""
gravity_law.py

Órgano de juicio simbólico de AXXON Core.
Implementa la Ley de Gravedad Simbólica para decisiones narrativas adaptativas.

Evalúa:
- Masa simbólica (peso emocional + trayectoria narrativa + resonancia)
- Nivel de colisión interpretativa
Y determina:
- Tipo de respuesta simbólica más útil: contención, ruptura, acompañamiento, reencuadre.

Versión: 2.0.0
Autor: AXXON DevCore
"""

# Opcional: librería para trazabilidad futura
import logging


def calcular_masa_simbolica(emocion, trayectoria_score, resonancia_score, tipo_emocion=None):
    """
    Calcula una masa simbólica total con base en tres factores:
    - emoción (peso emocional)
    - trayectoria (frecuencia/constancia del símbolo)
    - resonancia (alineación con núcleo simbólico/arquetipo)

    Aplica ponderación especial según el tipo de emoción (ej. culpa pesa más que duda).

    Args:
        emocion (float): carga emocional de 0.0 a 1.0
        trayectoria_score (float): repetición simbólica de 0.0 a 1.0
        resonancia_score (float): coherencia con núcleo/arquetipo 0.0 a 1.0
        tipo_emocion (str): nombre simbólico de la emoción

    Returns:
        float: masa simbólica entre 0.0 y 1.0
    """
    pesos = {
        "emocion": 0.5,
        "trayectoria": 0.3,
        "resonancia": 0.2
    }

    # Ajustes según emoción
    amplificadores = {
        "culpa": 1.15,
        "miedo": 1.1,
        "tristeza": 1.05,
        "ira": 1.0,
        "duda": 0.95,
        "curiosidad": 0.9,
        "neutral": 0.85
    }

    factor = amplificadores.get(tipo_emocion.lower(), 1.0) if tipo_emocion else 1.0

    masa_base = (
        pesos["emocion"] * emocion +
        pesos["trayectoria"] * trayectoria_score +
        pesos["resonancia"] * resonancia_score
    )

    masa_final = min(1.0, masa_base * factor)
    return round(masa_final, 3)


def juzgar_colision(masa):
    """
    Evalúa el nivel de colisión simbólica según la masa.

    Returns:
        dict: nivel + tipo de acción adaptativa recomendada
    """
    if masa < 0.25:
        return {"nivel": "leve", "accion": "acompañamiento"}
    elif masa < 0.5:
        return {"nivel": "media", "accion": "reencuadre"}
    elif masa < 0.75:
        return {"nivel": "alta", "accion": "contención"}
    else:
        return {"nivel": "crítica", "accion": "ruptura_reestructuracion"}


def evaluar_gravedad(emocion_val, trayectoria_val, resonancia_val, tipo_emocion=None):
    """
    Juicio simbólico completo: evalúa masa, colisión, y retorno interpretativo.

    Args:
        emocion_val (float): carga emocional del mensaje (0-1)
        trayectoria_val (float): score de repetición narrativa (0-1)
        resonancia_val (float): score de coherencia con identidad (0-1)
        tipo_emocion (str): etiqueta emocional como "culpa", "ira", "tristeza", etc.

    Returns:
        dict: juicio simbólico + masa
    """
    masa = calcular_masa_simbolica(
        emocion=emocion_val,
        trayectoria_score=trayectoria_val,
        resonancia_score=resonancia_val,
        tipo_emocion=tipo_emocion
    )

    juicio = juzgar_colision(masa)
    juicio.update({
        "masa_simbolica": masa,
        "etiqueta_emocion": tipo_emocion or "desconocido"
    })

    return juicio


# Prueba directa
if __name__ == "__main__":
    resultado = evaluar_gravedad(
        emocion_val=0.8,
        trayectoria_val=0.6,
        resonancia_val=0.4,
        tipo_emocion="tristeza"
    )
    print("[AXXON :: Juicio Simbólico]")
    print(resultado)