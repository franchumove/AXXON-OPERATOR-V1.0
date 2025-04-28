"""
AXXON CORE OPERATOR - Credenciales Manager
------------------------------------------
Administra las credenciales externas de los agentes (Drive, SMTP, etc.).

Autor: AXXON DevCore
"""

import json
import os

CREDENCIALES_PATH = "operator_credenciales.json"

def guardar_credenciales(agent_id, servicio, credenciales):
    """
    Guarda credenciales para un servicio específico.

    Args:
        agent_id (str): ID simbólico del agente.
        servicio (str): Nombre del servicio ("drive", "smtp", etc.).
        credenciales (dict): Datos sensibles necesarios.
    """
    entrada = {
        "agent_id": agent_id,
        "servicio": servicio,
        "credenciales": credenciales
    }

    with open(CREDENCIALES_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

# 🧪 Test rápido
if __name__ == "__main__":
    guardar_credenciales(
        agent_id="aurora_operator",
        servicio="drive",
        credenciales={"access_token": "FAKE-TOKEN-123"}
    )
    print("✅ Credenciales de prueba guardadas.")