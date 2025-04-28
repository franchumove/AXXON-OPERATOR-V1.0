# collision_detector.py
"""
Detector de colisiones simbólicas AXXON.

Interpreta masa simbólica y asigna nivel de colisión:
- leve → acompañar
- media → reencuadrar
- alta → contener
- crítica → reestructurar
"""

def detectar_colision(masa_simbolica):
    """
    Evalúa nivel de colisión simbólica.

    Args:
        masa_simbolica (float): Valor entre 0.0 y 1.0

    Returns:
        dict: Nivel de impacto y tipo de intervención.
    """
    if masa_simbolica < 0.2:
        return {"nivel": "leve", "accion": "acompañar"}
    elif masa_simbolica < 0.5:
        return {"nivel": "media", "accion": "reencuadrar"}
    elif masa_simbolica < 0.8:
        return {"nivel": "alta", "accion": "contener"}
    else:
        return {"nivel": "crítica", "accion": "reestructurar"}