# db_connection.py
"""
Módulo para manejar conexión y operaciones con la base de datos SQLite de AXXON.

Responsabilidad:
- Crear tabla si no existe.
- Guardar interacciones simbólicas.
- Recuperar memoria simbólica reciente o total.
"""

import sqlite3
from datetime import datetime
import os

DB_PATH = "memory_axxon.db"  # Se puede mover a variable de entorno si se quiere

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                respuesta TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()

def save_interaction_to_db(user_id, message, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO interacciones (user_id, mensaje, respuesta, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_id, message, response, timestamp))
        conn.commit()

def get_recent_memory(user_id, limit=5):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT mensaje, respuesta FROM interacciones
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))
        return cursor.fetchall()