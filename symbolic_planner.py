# symbolic_planner.py
"""
Generador de rutas simbólicas personalizadas para usuarios AXXON.
- Toma patrones emocionales, motivos y contexto.
- Devuelve una secuencia de pasos simbólicos con sentido narrativo.
"""

from motive_mapper import mapear_motivos
from emocional_detector import detect_emotion
from tono_mapper import determinar_tono

# Plantillas base de rutas simbólicas por tipo de motivación
templates = {
    "búsqueda": [
        "Reconocer lo que falta",
        "Nombrar el anhelo",
        "Visualizar la dirección",
        "Dar el primer paso simbólico"
    ],
    "confianza": [
        "Validar fortalezas previas",
        "Recordar momentos de certeza",
        "Nombrar la duda",
        "Reafirmar compromiso"
    ],
    "reconexión": [
        "Aceptar la desconexión",
        "Escuchar la voz interna",
        "Detectar señales simbólicas del entorno",
        "Establecer pequeño ritual de retorno"
    ],
    "autenticidad": [
        "Identificar lo que se ha silenciado",
        "Honrar lo que emerge",
        "Poner límites simbólicos",
        "Actuar desde el centro"
    ],
    "propósito": [
        "Recordar el para qué",
        "Nombrar los hilos que conectan",
        "Ver el impacto posible",
        "Enunciar acción con sentido"
    ]
}

def planificar_ruta_simbolica(mensaje):
    emocion = detect_emotion(mensaje)
    tono = determinar_tono(emocion)
    motivos = mapear_motivos(mensaje)

    pasos = []
    for motivo in motivos:
        if motivo in templates:
            pasos.extend(templates[motivo])

    if not pasos:
        pasos = ["Escuchar", "Nombrar", "Explorar", "Responder"]  # Ruta genérica

    return {
        "emocion": emocion,
        "tono": tono,
        "motivadores": motivos,
        "ruta_simbolica": pasos
    }

# =============================
# Prueba simbólica directa
# =============================
if __name__ == "__main__":
    test_mensaje = "Siento que he perdido el rumbo, pero quiero volver a conectarme conmigo misma."
    from pprint import pprint
    pprint(planificar_ruta_simbolica(test_mensaje))