# runner.py

"""
AXXON OPERATOR - Runner Maestro
-------------------------------
Inicia el Orquestador Flask y el Trigger Manager de Recordatorios simultáneamente.

Autor: AXXON DevCore
"""

import threading
import time
from main_orquestador import app  # Tu servidor Flask
from trigger_manager import loop_infinito_triggers

def lanzar_flask_server():
    """
    Lanza el servidor Flask principal.
    """
    app.run(host="0.0.0.0", port=5500)

def lanzar_trigger_loop():
    """
    Lanza el loop infinito de triggers de recordatorios.
    """
    loop_infinito_triggers()

if __name__ == "__main__":
    print("🚀 Iniciando AXXON OPERATOR...")

    # Lanzar server Flask
    flask_thread = threading.Thread(target=lanzar_flask_server)
    flask_thread.start()

    # Lanzar trigger manager
    trigger_thread = threading.Thread(target=lanzar_trigger_loop)
    trigger_thread.start()

    # (Opcional) Futuro: otros hilos de servicios

    # Mantener vivo el proceso principal
    while True:
        time.sleep(60)