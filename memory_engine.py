"""
AXXON Memory Engine:
- Memoria episódica en SQLite
- Memoria semántica simbólica con FAISS
- Indexación emocional simbólica
Versión: 2.2
"""

import os
import json
import sqlite3
import numpy as np
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# =====================
# ⚙️ CONFIGURACIÓN BASE
# =====================

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Configuración correcta

DB_PATH = "memory_axxon.db"
JSONL_PATH = "notion_bloques.jsonl"
EMBEDDING_MODEL = "text-embedding-ada-002"

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    logging.warning("[AXXON Memory Engine] FAISS no disponible.")
    FAISS_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ======================
# 🧠 MEMORIA EPISÓDICA
# ======================

def guardar_en_sqlite(user_id: str, mensaje: str, respuesta: str):
    """Guarda interacción literal en SQLite."""
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

def recuperar_memoria_lit(user_id: str, limite: int = 5) -> list:
    """Recupera últimas interacciones de un usuario."""
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

def cargar_y_vectorizar(jsonl_path: str = JSONL_PATH):
    """Carga bloques simbólicos y vectoriza."""
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
        logging.error(f"[AXXON Memory Engine Error] {e}")

def generar_embedding(texto: str) -> list:
    """Genera embedding simbólico usando OpenAI."""
    try:
        response = client.embeddings.create(  # ✅ Método actualizado
            model=EMBEDDING_MODEL,
            input=texto
        )
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"[AXXON Embedding Error] {e}")
        return []

def construir_indice():
    """Construye índice FAISS."""
    if not vectores or not FAISS_AVAILABLE:
        return None
    dimension = len(vectores[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectores).astype("float32"))
    return index

def buscar_por_resonancia_semantica(mensaje: str, top_k: int = 3) -> list:
    """Busca bloques simbólicos resonantes."""
    if not FAISS_AVAILABLE:
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

def memoria_combinada_para_contexto(user_id: str, mensaje: str) -> str:
    """Integra memoria episódica y semántica."""
    reciente = recuperar_memoria_lit(user_id)
    similares = buscar_por_resonancia_semantica(mensaje)
    resumen_vectorial = "\n".join(
        [f"[{b['pagina']}] {b['bloque']}" for b in similares]
    ) if similares else "No hay resonancias simbólicas."

    return "\n".join(reciente + ["--- BLOQUES SIMBÓLICOS ---", resumen_vectorial])