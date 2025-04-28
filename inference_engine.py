"""
    Órgano de Inferencia Simbólica Unificada – Núcleo AXXON Core v1.7.3

    Mejoras clave:
    - Detección temática avanzada
    - Gestión robusta de símbolos
    - Sistema de resonancia mejorado
    - Validación estricta de arquetipos
    - Tipado fuerte y validación de estructura
"""

from typing import TypedDict, Literal
import logging

from emocional_detector import detect_emotion
from tono_mapper import determinar_tono
from motive_mapper import mapear_motivos
from symbolic_planner import planificar_ruta_simbolica
from gravity_law import evaluar_gravedad
from cognitive_controller.controller import decide_modules
from emotion_lexicon import evaluar_carga_emocional
from db_connection import get_recent_memory
from identity_bridge import get_identidad_simbolica
from symbolic_dictionary import escanear_texto

    # =============================
    # Definición de tipos simbólicos
    # =============================

class EstructuraSimbolica(TypedDict):
        emocion: str
        tono: str
        motivos: list[str]
        plan_simbólico: str
        gravedad: dict
        modulos_activados: list[str]
        arquetipo: str
        identidad_completa: dict
        simbolos_detectados: list[dict]

ArquetipoValido = Literal['explorer', 'guardian', 'alchemist', 'oracle', 'companion']
NivelGravedad = Literal[1, 2, 3, 4, 5]

    # =============================
    # Núcleo de inferencia simbólica
    # =============================

def calcular_fuerza_simbolica(mensaje: str, user_id: str, tipo_emocion: str = None) -> dict:
        """
        Calcula masa simbólica con resonancia basada en identidad.
        """
        emocion_val = evaluar_carga_emocional(mensaje)
        trayectoria_val = _calcular_repeticion(user_id, mensaje)
        resonancia_val = _calcular_resonancia(user_id, mensaje)

        return evaluar_gravedad(
            emocion_val,
            trayectoria_val,
            resonancia_val,
            tipo_emocion=tipo_emocion
        )

def _calcular_resonancia(user_id: str, mensaje: str) -> float:
        """
        Cálculo de resonancia simbólica entre identidad y mensaje.
        """
        identidad = get_identidad_simbolica(user_id)
        temas_identidad = identidad.get("temas_clave", [])
        temas_mensaje = mapear_motivos(mensaje)

        intersección = len(set(temas_identidad) & set(temas_mensaje))
        return min(intersección / 3, 1.0)

def _calcular_repeticion(user_id: str, mensaje: str) -> float:
        """
        Repetición narrativa basada en temas detectados.
        """
        historial = get_recent_memory(user_id)
        temas_mensaje = set(mapear_motivos(mensaje))
        repetido = 0

        for m, _ in historial:
            temas_previos = set(mapear_motivos(m))
            if temas_previos & temas_mensaje:
                repetido += 1

        return min(repetido / 3, 1.0)

def _validar_arquetipo(arquetipo: str) -> ArquetipoValido:
        """
        Valida arquetipo o asigna 'explorer' por defecto.
        """
        validos = getattr(ArquetipoValido, '__args__', ['explorer', 'guardian', 'alchemist', 'oracle', 'companion'])
        return arquetipo if arquetipo in validos else 'explorer'

def inferir_estructura_simbolica(user_id: str, mensaje: str) -> EstructuraSimbolica:
        """
        Genera la estructura simbólica interpretativa de la interacción.
        """
        emocion = detect_emotion(mensaje)
        identidad = get_identidad_simbolica(user_id)

        arquetipo = _validar_arquetipo(identidad.get("arquetipo", "explorer"))
        tono = determinar_tono(emocion, arquetipo=arquetipo)

        motivos = mapear_motivos(mensaje)
        plan_simb = planificar_ruta_simbolica(mensaje)
        gravedad = calcular_fuerza_simbolica(mensaje, user_id, tipo_emocion=emocion)
        modulos = decide_modules(arquetipo, emocion)

        simbolos_detectados = escanear_texto(mensaje, fuente="notion") or []
        if simbolos_detectados:
            logging.info(f"[AXXON-Inferencia] Símbolos detectados: {[list(s.keys())[0] for s in simbolos_detectados]}")

        return EstructuraSimbolica(
            emocion=emocion,
            tono=tono,
            motivos=motivos,
            plan_simbólico=plan_simb,
            gravedad=gravedad,
            modulos_activados=modulos,
            arquetipo=arquetipo,
            identidad_completa=identidad,
            simbolos_detectados=simbolos_detectados
        )

def construir_prompt_simbolico(estructura: EstructuraSimbolica, mensaje: str) -> str:
        """
        Construye un prompt interpretativo y emocional para la generación de respuesta.
        """
        gravedad_txt = estructura["gravedad"]["accion"].replace('_', ' ').capitalize()
        nivel_gravedad = estructura["gravedad"]["nivel"]
        motivos_txt = ", ".join(estructura["motivos"]) or "Sin motivos detectados"
        simbolos_txt = ", ".join(
            next(iter(s.keys()), 'símbolo_no_clasificado') for s in estructura["simbolos_detectados"]
        ) if estructura["simbolos_detectados"] else "ninguno"

        prompt = (
            f"Mensaje recibido: [{mensaje}]\n\n"
            f"Interpretación simbólica AXXON:\n"
            f"- Emoción: {estructura['emocion']} ({nivel_gravedad}/5)\n"
            f"- Tono sugerido: {estructura['tono']}\n"
            f"- Motivos detectados: {motivos_txt}\n"
            f"- Símbolos activados: {simbolos_txt}\n"
            f"- Plan simbólico: {estructura['plan_simbólico']}\n"
            f"- Arquetipo interpretativo: {estructura['arquetipo'].upper()}\n\n"
            f"Directiva: {estructura['arquetipo'].upper()}::{estructura['gravedad']['accion'].replace('_', '::')}\n"
            f"Modo de respuesta: {estructura['tono'].upper()} (enfasis: {estructura['plan_simbólico'].split(':')[0].lower()})\n\n"
            f"Instrucciones: Responder integrando mínimo 2 símbolos, respetando el tono y gravitación emocional."
        )

        return prompt

