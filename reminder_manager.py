# reminder_manager.py

"""
AXXON OPERATOR - Reminder Manager
---------------------------------
Agendador simbólico de recordatorios.

- Guarda recordatorios en una base SQLite.
- Revisa recordatorios vencidos para lanzar acciones.
"""

import sqlite3
import os
from clock_engine import obtener_hora_actual

DB_PATH = os.getenv("REMINDERS_DB", "reminders_axxon.db")

def inicializar_db():
    """
    Crea la base de recordatorios si no existe.
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
    Agenda un nuevo recordatorio.
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
    Encuentra recordatorios que ya vencieron y aún no fueron enviados.
    """
    ahora = obtener_hora_actual().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, descripcion, fecha_hora FROM recordatorios
            WHERE enviado = 0 AND fecha_hora <= ?
        """, (ahora,))
        resultados = cursor.fetchall()
    return resultados

def marcar_enviado(recordatorio_id):
    """
    Marca un recordatorio como enviado.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE recordatorios
            SET enviado = 1
            WHERE id = ?
        """, (recordatorio_id,))
        conn.commit()

# 🧪 Test directo
if __name__ == "__main__":
    inicializar_db()
    agendar_recordatorio("user123", "Reunión importante", "2025-04-22 15:00:00")
    pendientes = buscar_recordatorios_pendientes()
    print(pendientes)