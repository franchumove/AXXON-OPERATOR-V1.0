# telegram_webhook_receiver.py

"""
AXXON OPERATOR - Telegram Webhook Receiver
-------------------------------------------
Recibe eventos de botones (callback_query) desde Telegram.

- Procesa respuestas de recordatorios (confirmar o reagendar).
- Opcional: actualizar o eliminar recordatorios si se desea.

Autor: AXXON DevCore
"""

import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from reminder_manager import marcar_enviado

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

@app.route("/telegram_webhook", methods=["POST"])
def recibir_telegram():
    """
    Procesa eventos entrantes de Telegram Bot.
    """
    data = request.get_json()

    if "callback_query" in data:
        callback = data["callback_query"]
        mensaje = callback.get("data")
        chat_id = callback["message"]["chat"]["id"]

        if mensaje.startswith("recordatorio_confirmado_"):
            id_recordatorio = int(mensaje.split("_")[-1])
            marcar_enviado(id_recordatorio)

            enviar_mensaje(chat_id, "✅ Recordatorio confirmado y registrado. ¡Gracias!")

        elif mensaje.startswith("recordatorio_reagendar_"):
            id_recordatorio = int(mensaje.split("_")[-1])
            # Opcional: lógica futura de reagendamiento
            enviar_mensaje(chat_id, "🔄 Funcionalidad de reagendamiento aún no disponible.")

        else:
            enviar_mensaje(chat_id, "❓ Acción no reconocida.")

    return jsonify({"status": "ok"})

def enviar_mensaje(chat_id, texto):
    """
    Envía un mensaje al usuario vía Telegram.
    """
    import requests

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto
    }
    requests.post(url, json=payload)

# 🧪 Test local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5502)