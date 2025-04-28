# reminder_manager.py

"""
AXXON OPERATOR - Reminder Manager
---------------------------------
Gestor simbólico de recordatorios:

- Guardar nuevos recordatorios.
- Consultar vencidos.
- Marcar enviados.
- (Opcional futuro) Reagendar recordatorios.

Autor: AXXON DevCore
"""

import sqlite3
import os
from clock_engine import obtener_hora_actual

DB_PATH = os.getenv("REMINDERS_DB", "reminders_axxon.db")

def inicializar_db():
    """
    Inicializa la base de datos SQLite si no existe.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recordatorios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                descripcion TEXT,
                fecha_hora TEXT,
                enviado INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def agendar_recordatorio(user_id, descripcion, fecha_hora):
    """
    Agrega un nuevo recordatorio a la base.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO recordatorios (user_id, descripcion, fecha_hora)
            VALUES (?, ?, ?)
        """, (user_id, descripcion, fecha_hora))
        conn.commit()

def buscar_recordatorios_pendientes():
    """
    Devuelve los recordatorios vencidos que aún no se enviaron.
    """
    ahora = obtener_hora_actual().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, descripcion, fecha_hora
            FROM recordatorios
            WHERE enviado = 0 AND fecha_hora <= ?
        """, (ahora,))
        resultados = cursor.fetchall()
    return resultados

def marcar_enviado(recordatorio_id):
    """
    Marca un recordatorio como ya enviado.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE recordatorios
            SET enviado = 1
            WHERE id = ?
        """, (recordatorio_id,))
        conn.commit()

# (Opcional Futuro)
def reagendar_recordatorio(recordatorio_id, nueva_fecha_hora):
    """
    Reagenda un recordatorio para una nueva fecha y hora.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE recordatorios
            SET fecha_hora = ?, enviado = 0
            WHERE id = ?
        """, (nueva_fecha_hora, recordatorio_id))
        conn.commit()

# 🧪 Test rápido
if __name__ == "__main__":
    inicializar_db()
    agendar_recordatorio("user123", "Reunión importante", "2025-04-22 15:00:00")
    pendientes = buscar_recordatorios_pendientes()
    print(pendientes)