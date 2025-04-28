# motive_mapper.py
"""
Módulo simbólico para detección de motivadores profundos en lenguaje natural.

Toma frases introspectivas del usuario y clasifica qué fuerzas simbólicas lo mueven:
- Búsqueda, miedo, deseo, protección, reconocimiento, evasión, libertad, pertenencia...

Ideal para coaching, diseño narrativo adaptativo y generación de rutas simbólicas.
"""

import re

# Definición de motivadores simbólicos
MOTIVADORES = {
    "búsqueda": ["encontrar", "buscar", "hallar", "descubrir", "reconectar", "sentido", "camino"],
    "protección": ["proteger", "resguardar", "seguridad", "refugio", "defender", "cuidar"],
    "reconocimiento": ["reconocer", "valorar", "aprobación", "ser vista", "demostrar", "elogio"],
    "evasión": ["escapar", "huir", "olvidar", "evadir", "soltar", "desaparecer"],
    "libertad": ["libre", "libertad", "sin límites", "expandir", "volar", "salir de"],
    "pertenencia": ["pertenecer", "encajar", "unirme", "ser parte", "tribu", "comunidad"],
    "miedo": ["miedo", "temor", "angustia", "pánico", "inseguridad"],
    "deseo": ["quiero", "anhelo", "sueño", "me gustaría", "deseo", "me motiva"],
    "reto": ["lograr", "desafío", "objetivo", "meta", "superar", "alcanzar"]
}

def mapear_motivos(texto):
    """
    Analiza un mensaje y retorna una lista de motivadores simbólicos detectados.
    """
    motivos_detectados = []

    for motivo, palabras_clave in MOTIVADORES.items():
        for palabra in palabras_clave:
            if re.search(rf"\b{palabra}\b", texto.lower()):
                motivos_detectados.append(motivo)
                break  # Si una palabra ya activa un motivo, seguimos con el siguiente

    return list(set(motivos_detectados)) or ["indefinido"]

# Prueba directa
if __name__ == "__main__":
    prueba = "Siento que necesito encontrarme. Estoy buscando algo más profundo, algo que me devuelva el sentido."
    print(mapear_motivos(prueba))