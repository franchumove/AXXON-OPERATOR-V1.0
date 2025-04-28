# trigger_manager.py

"""
AXXON OPERATOR - Trigger Manager
---------------------------------
Lanzador automático de eventos cuando vencen recordatorios.

Acciones simbólicas:
- Enviar recordatorio por Email.
- Enviar recordatorio por Telegram.

Autor: AXXON DevCore
"""

import time
from reminder_manager import buscar_recordatorios_pendientes, marcar_enviado
from email_sender import enviar_email_simple
from telegram_sender import enviar_telegram

def procesar_triggers():
    """
    Procesa todos los recordatorios vencidos y lanza acciones.
    """
    pendientes = buscar_recordatorios_pendientes()

    if not pendientes:
        return  # No hace falta procesar si no hay nada

    for recordatorio in pendientes:
        id_recordatorio, user_id, descripcion, fecha_hora = recordatorio

        mensaje = f"⏰ Recordatorio:\n\n{descripcion}\n\n⏳ Programado para: {fecha_hora}"

        # Enviar Email
        try:
            enviar_email_simple(
                destino="user@correo.com",  # ← Aquí buscar correo real si quieres futuro
                asunto="Recordatorio AXXON Operator",
                cuerpo=mensaje
            )
            print(f"[TriggerManager] ✅ Email enviado: {descripcion}")
        except Exception as e:
            print(f"[TriggerManager] ⚠️ Error enviando Email: {e}")

        # Enviar Telegram
        try:
            enviar_telegram(mensaje)
            print(f"[TriggerManager] ✅ Telegram enviado: {descripcion}")
        except Exception as e:
            print(f"[TriggerManager] ⚠️ Error enviando Telegram: {e}")

        # Marcar como enviado simbólicamente
        marcar_enviado(id_recordatorio)

def loop_infinito_triggers():
    """
    Loop simbólico que chequea cada 60 segundos.
    """
    while True:
        procesar_triggers()
        time.sleep(60)

# 🧪 Test directo
if __name__ == "__main__":
    procesar_triggers()