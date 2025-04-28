"""
AXXON CORE OPERATOR - Operational Engine
----------------------------------------
Maneja operaciones simbólicas automáticas: generación, envío y almacenamiento de información emocional.

Autor: AXXON DevCore
"""

from pdf_generator_core import guardar_como_pdf
from drive_connector_core import subir_a_drive
from email_sender_core import enviar_correo

def flujo_operativo_completo(texto_simbolico, destinatario=None):
    """
    Flujo operativo:
    1. Generar PDF simbólico.
    2. Subir a Drive.
    3. Enviar correo opcionalmente.

    Args:
        texto_simbolico (str): Texto emocional o narrativo.
        destinatario (str, opcional): Email de destino.
    """
    try:
        # 1. Guardar PDF
        nombre_base = "documento_simbolico"
        ruta_pdf = guardar_como_pdf(texto_simbolico, nombre_base)

        # 2. Subir a Drive
        resultado_drive = subir_a_drive(ruta_pdf)

        # 3. Opcional: Enviar por correo
        if destinatario:
            enviar_correo(
                destinatario=destinatario,
                asunto="Documento Simbólico AXXON",
                cuerpo=f"Tu documento simbólico ha sido creado y subido.\nRuta local: {ruta_pdf}"
            )

        return {
            "pdf": ruta_pdf,
            "upload": resultado_drive
        }

    except Exception as e:
        return {"error": str(e)}

# 🧪 Test rápido
if __name__ == "__main__":
    print(flujo_operativo_completo(
        texto_simbolico="Texto emocional profundo generado por AXXON Core Operator.",
        destinatario=None  # Opcional: poner email real si quieres enviar.
    ))