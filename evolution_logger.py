        # evolution_logger.py

"""
        AXXON - Registro de Transformaciones Cognitivas

        Este módulo registra mutaciones simbólicas:
        - Cambios de tono emocional
        - Evoluciones narrativas del usuario
        - Contradicciones superadas
        - Integraciones de nuevos símbolos

        Versión 1.2
        Autor: AXXON DevCore
"""

import logging
from datetime import datetime
from sheet_logger import log_event_simbolico


def registrar_mutacion(user_id, tipo, descripcion, simbolos=None, tags=None, nivel="alto"):
            """
            Registra una mutación simbólica del usuario.

            Args:
                user_id (str): Usuario afectado.
                tipo (str): Tipo de mutación ("emotiva", "narrativa", "reflexiva", etc.).
                descripcion (str): Qué cambió internamente.
                simbolos (list): Lista de símbolos o emociones implicadas.
                tags (list): Etiquetas adicionales para análisis simbólico (opcional).
                nivel (str): Nivel de impacto percibido ("alto", "medio", "leve").
            """
            try:
                evento = f"[{tipo.upper()}] {descripcion}"
                if simbolos:
                    evento += f" | Símbolos implicados: {', '.join(simbolos)}"

                # Agregar tag automático de mutación si no está
                tags = tags or []
                if "mutación" not in tags:
                    tags.append("mutación")
                if tipo and tipo not in tags:
                    tags.append(tipo)

                log_event_simbolico(
                    user_id=user_id,
                    tipo_evento="mutacion",
                    contenido=evento,
                    nivel=nivel,
                    tags=tags
                )

                logging.info(f"[AXXON Evolution] Mutación simbólica registrada para {user_id}: {evento}")

            except Exception as e:
                logging.error(f"[AXXON EvolutionLogger] Fallo al registrar mutación: {e}")