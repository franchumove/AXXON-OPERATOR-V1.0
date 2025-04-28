# clock_engine.py

"""
AXXON OPERATOR - Clock Engine
-----------------------------
Motor de tiempo simbólico para:
- Saber hora y fecha actual
- Operar en zona horaria configurada
"""

import pytz
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

TIMEZONE = os.getenv("TIMEZONE", "UTC")

def obtener_hora_actual():
    """
    Retorna la hora actual ajustada a la zona horaria configurada.
    """
    zona = pytz.timezone(TIMEZONE)
    ahora = datetime.datetime.now(zona)
    return ahora

def formatear_fecha_hora(dt=None):
    """
    Formatea la fecha y hora de manera amigable.
    """
    dt = dt or obtener_hora_actual()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# 🧪 Test directo
if __name__ == "__main__":
    print(f"Hora simbólica ahora: {formatear_fecha_hora()}")