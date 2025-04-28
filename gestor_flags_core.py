"""
AXXON CORE OPERATOR - Gestor de Flags
-------------------------------------
Administra activación simbólica de módulos adicionales: Drive, PDF, Email.

Autor: AXXON DevCore
"""

import json
import os

FLAGS_PATH = "operator_flags.json"

def inicializar_flags_core(agent_id):
    """
    Inicializa flags simbólicos para un agente.

    Args:
        agent_id (str): ID simbólico del agente.
    """
    flags = {
        "agent_id": agent_id,
        "drive_enabled": False,
        "pdf_enabled": False,
        "email_enabled": False
    }

    with open(FLAGS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(flags, ensure_ascii=False) + "\n")

def activar_modulo(agent_id, modulo):
    """
    Activa un módulo operativo para el agente.

    Args:
        agent_id (str): ID del agente.
        modulo (str): "drive", "pdf", "email"
    """
    try:
        if not os.path.exists(FLAGS_PATH):
            return False

        # Leer todos los flags
        with open(FLAGS_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        nuevos_flags = []
        for line in lines:
            flag = json.loads(line)
            if flag["agent_id"] == agent_id:
                flag[f"{modulo}_enabled"] = True
            nuevos_flags.append(flag)

        # Guardar actualización
        with open(FLAGS_PATH, "w", encoding="utf-8") as f:
            for flag in nuevos_flags:
                f.write(json.dumps(flag, ensure_ascii=False) + "\n")

        return True

    except Exception as e:
        print(f"[GestorFlags Error] {e}")
        return False

# 🧪 Test rápido
if __name__ == "__main__":
    inicializar_flags_core("aurora_operator")
    activar_modulo("aurora_operator", "drive")