"""
AXXON CORE OPERATOR - Email Sender
-----------------------------------
Permite enviar correos simbólicos a través de SMTP configurado.

Autor: AXXON DevCore
"""

import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def enviar_correo(destinatario, asunto, cuerpo):
    """
    Envía un correo emocional simbólico.

    Args:
        destinatario (str): Correo destino.
        asunto (str): Asunto del correo.
        cuerpo (str): Cuerpo del mensaje.
    """
    try:
        mensaje = MIMEText(cuerpo)
        mensaje["Subject"] = asunto
        mensaje["From"] = SMTP_USER
        mensaje["To"] = destinatario

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, destinatario, mensaje.as_string())

        return {"status": "enviado"}

    except Exception as e:
        return {"error": str(e)}

# 🧪 Test rápido
if __name__ == "__main__":
    resultado = enviar_correo(
        destinatario="test@example.com",
        asunto="Test AXXON",
        cuerpo="Este es un correo de prueba simbólico."
    )
    print(resultado)