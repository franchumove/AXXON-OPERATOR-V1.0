# memory_store.py
import logging

# Memoria emocional en tiempo real (puede escalarse a base de datos o persistencia externa)
MEMORY_USERS = {}

def retrieve_memory(user_id):
    memory = MEMORY_USERS.get(user_id, "Sin memoria previa")
    logging.info(f"Retrieved memory '{memory}' for user_id: {user_id}")
    return memory

def save_memory(user_id, message, response):
    MEMORY_USERS[user_id] = f"Último mensaje: {message} | Última respuesta: {response}"
    logging.info(f"Saved memory for user_id: {user_id} - Message: '{message}', Response: '{response[:50]}...'")

# ==========================
# MEMORIA DOCUMENTAL (ej: PDFs, documentos, conocimiento externo)
# ==========================

MEMORIA_DOCUMENTAL = {}

def guardar_documento(clave, contenido):
    MEMORIA_DOCUMENTAL[clave] = contenido
    logging.info(f"[MEMORIA DOC] Guardado bajo clave '{clave}'")

def recuperar_documento(clave):
    return MEMORIA_DOCUMENTAL.get(clave, "Documento no encontrado.")
