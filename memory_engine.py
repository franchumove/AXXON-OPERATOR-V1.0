"""
Motor simbólico de memoria AXXON:
- Guarda interacciones en SQLite (episódico literal)
- Indexa y busca resonancias en FAISS (semántico emocional actualizado, si disponible)
"""

import os
import json
import sqlite3
import numpy as np
import logging
from datetime import datetime
from dotenv import load_dotenv
import openai

# Intento seguro de cargar FAISS
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"[AXXON Memory Engine] FAISS no disponible ({e}). Solo operará memoria episódica.")
    FAISS_AVAILABLE = False

# =====================
# ⚙️ CONFIGURACIÓN BASE
# =====================

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DB_PATH = "memory_axxon.db"
JSONL_PATH = "notion_bloques.jsonl"
EMBEDDING_MODEL = "text-embedding-ada-002"

# ======================
# 🧠 MEMORIA LITERAL
# ======================

def guardar_en_sqlite(user_id, mensaje, respuesta):
    """Guarda una interacción en la base de datos SQLite."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(respuesta, (dict, list)):
        respuesta = json.dumps(respuesta, ensure_ascii=False)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                mensaje TEXT,
                respuesta TEXT,
                timestamp TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO interacciones (user_id, mensaje, respuesta, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_id, mensaje, respuesta, timestamp))
        conn.commit()

def recuperar_memoria_lit(user_id, limite=5):
    """Recupera las últimas interacciones de un usuario."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT mensaje, respuesta FROM interacciones
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limite))
        resultados = cursor.fetchall()
    return [f"U: {m} | A: {r}" for m, r in resultados]

# ======================
# 🧠 MEMORIA SEMÁNTICA
# ======================

bloques = []
vectores = []

def cargar_y_vectorizar(jsonl_path=JSONL_PATH):
    """Carga bloques simbólicos desde un .jsonl y genera sus embeddings."""
    global bloques, vectores
    bloques.clear()
    vectores.clear()

    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for linea in f:
                data = json.loads(linea)
                texto = data.get("bloque")
                if texto:
                    emb = generar_embedding(texto)
                    if emb:
                        bloques.append(data)
                        vectores.append(emb)
    except Exception as e:
        logging.error(f"[AXXON Memory Engine Error] Error al cargar y vectorizar: {e}")

def generar_embedding(texto):
    """Genera un embedding para un texto utilizando OpenAI API."""
    try:
        response = openai.Embedding.create(
            input=[texto],
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"[AXXON Embedding Error] {e}")
        return None

def construir_indice():
    """Construye el índice FAISS si está disponible."""
    if not vectores or not FAISS_AVAILABLE:
        return None
    dimension = len(vectores[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectores).astype("float32"))
    return index

def buscar_por_resonancia_semantica(mensaje, top_k=3):
    """Busca bloques simbólicos más resonantes."""
    if not FAISS_AVAILABLE:
        logging.warning("[AXXON Memory Engine] Resonancia semántica no disponible. Retornando vacío.")
        return []

    emb = generar_embedding(mensaje)
    if not emb:
        return []

    index = construir_indice()
    if not index:
        return []

    D, I = index.search(np.array([emb]).astype("float32"), top_k)
    return [bloques[i] for i in I[0] if i < len(bloques)]

# ======================
# 🧬 MEMORIA COMBINADA
# ======================

def memoria_combinada_para_contexto(user_id, mensaje):
    """Integra memoria episódica literal + resonancias semánticas."""
    reciente = recuperar_memoria_lit(user_id)
    similares = buscar_por_resonancia_semantica(mensaje)
    resumen_vectorial = "\n".join([f"[{b['pagina']}] {b['bloque']}" for b in similares]) if similares else "No hay resonancias."
    return "\n".join(reciente + ["--- BLOQUES SIMBÓLICOS ---", resumen_vectorial])