"""
AXXON OPERATOR - Telegram Sender PRO
-------------------------------------
Envío avanzado de recordatorios y mensajes simbólicos vía Telegram.

Funciones:
- Mensaje normal (Markdown/HTML).
- Mensaje con botones de acción.
- Manejo de errores robusto.

Autor: AXXON DevCore
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje, parse_mode="Markdown", botones=None):
    """
    Envía un mensaje simbólico al chat configurado en Telegram.

    Args:
        mensaje (str): Mensaje simbólico a enviar.
        parse_mode (str): "Markdown", "HTML" o None.
        botones (list, optional): Lista de botones. Ejemplo:
            [
                {"text": "Aceptar", "callback_data": "aceptar"},
                {"text": "Reagendar", "callback_data": "reagendar"}
            ]
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise Exception("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en .env")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": parse_mode
    }

    if botones:
        keyboard = {"inline_keyboard": [[boton] for boton in botones]}
        payload["reply_markup"] = keyboard

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Error enviando mensaje Telegram: {response.status_code} - {response.text}")

    result = response.json()
    if not result.get("ok"):
        raise Exception(f"Telegram API Error: {result.get('description')}")

    return result.get("result", {})

# 🧪 Test simbólico de ejemplo
if __name__ == "__main__":
    try:
        # Mensaje simple
        enviar_telegram("🧠 *AXXON Operator* te impulsa hoy a expandir tu consciencia simbólica.", parse_mode="Markdown")

        # Mensaje con botones
        botones = [
            {"text": "✅ Aceptar Recordatorio", "callback_data": "aceptar"},
            {"text": "🕒 Reagendar", "callback_data": "reagendar"}
        ]
        enviar_telegram(
            "⏰ *¿Qué deseas hacer con tu recordatorio?*", 
            parse_mode="Markdown", 
            botones=botones
        )

        print("✅ Mensajes simbólicos enviados exitosamente.")
    except Exception as e:
        print(f"❌ Error en envío simbólico: {e}")