    # bot.py

import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

    # ================================
    # 1. Configuración Inicial
    # ================================

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AXXON_ENDPOINT = os.getenv("AXXON_ENDPOINT")  # <- La URL de tu server AXXON
TIMEZONE = os.getenv("TIMEZONE", "America/Bogota")

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # ================================
    # 2. Funciones del Bot
    # ================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('¡Hola! Soy AXXON Operator. Estoy simbólicamente conectado.')

async def responder_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
        mensaje_usuario = update.message.text
        user_id = str(update.message.chat_id)

        try:
            payload = {
                "user_id": user_id,
                "message": mensaje_usuario
            }
            response = requests.post(f"{AXXON_ENDPOINT}/webhook", json=payload, timeout=20)

            if response.status_code == 200:
                data = response.json()
                respuesta_simbolica = data.get("response", "Respuesta simbólica no disponible.")
            else:
                respuesta_simbolica = "⚠️ No pude contactar al núcleo simbólico."

        except Exception as e:
            logging.error(f"Error al conectar con AXXON Operator: {e}")
            respuesta_simbolica = "⚠️ Error simbólico interno."

        await context.bot.send_message(chat_id=user_id, text=respuesta_simbolica)

    # ================================
    # 3. Main Loop
    # ================================

def main():
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensaje))

        logging.info("AXXON Operator conectado a Telegram.")
        application.run_polling()

if __name__ == "__main__":
        main()