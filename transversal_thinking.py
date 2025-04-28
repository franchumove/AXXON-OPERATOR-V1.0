        # transversal_thinking.py

"""
        AXXON - Pensamiento Transversal Cognitivo

        Detecta puentes simbólicos entre patrones de usuario, memorias previas,
        emociones dominantes y contradicciones narrativas.

        Integra:
        - Historia emocional
        - Contradicciones registradas
        - Conceptos simbólicos
        - Resultados de módulos previos

        Devuelve insights cruzados o alertas de ruptura simbólica.
        """

import logging
from memory_engine import get_recent_memory
from semantica_classifier import clasificar_simbolicamente
from pattern_inference import inferir_patron_simbolico

def pensamiento_transversal(user_id, mensaje_actual):
            """
            Busca conexiones semánticas profundas con memorias previas del usuario.

            Args:
                user_id (str): Identificador del usuario.
                mensaje_actual (str): Último mensaje recibido.

            Returns:
                dict: Conexiones transversales detectadas o None.
            """
            try:
                memoria = get_recent_memory(user_id)
                conexiones = []

                patron_actual = inferir_patron_simbolico(mensaje_actual)

                for mensaje_pasado, respuesta_pasada in memoria:
                    patron_pasado = inferir_patron_simbolico(mensaje_pasado)
                    conexion = clasificar_simbolicamente(patron_pasado, patron_actual)

                    if conexion:
                        conexiones.append({
                            "mensaje_pasado": mensaje_pasado,
                            "patron_pasado": patron_pasado,
                            "patron_actual": patron_actual,
                            "conexion": conexion
                        })

                if conexiones:
                    logging.info(f"[Transversalidad] {len(conexiones)} conexiones simbólicas detectadas.")
                    return {
                        "transversalidad_detectada": True,
                        "detalles": conexiones
                    }

                return {"transversalidad_detectada": False}

            except Exception as e:
                logging.error(f"[Transversalidad] Fallo en análisis transversal: {e}")
                return {"transversalidad_detectada": False}