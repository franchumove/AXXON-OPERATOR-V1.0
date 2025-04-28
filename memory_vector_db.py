"""
AXXON Memory Vector DB
Módulo de gestión y persistencia avanzada de vectores semánticos.
Carga, guarda, busca y actualiza índices FAISS para resonancia simbólica.
"""

import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
import openai

# ==========================
# ⚙️ CONFIGURACIÓN BÁSICA
# ==========================

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-ada-002"
INDEX_PATH = "memory_vector.index"
DATA_PATH = "memory_vector_data.jsonl"

bloques = []
vectores = []
index = None

# ==========================
# EMBEDDING
# ==========================

def generar_embedding(texto):
    try:
        resultado = openai.embeddings.create(
            input=texto,
            model=EMBEDDING_MODEL
        )
        return resultado.data[0].embedding
    except Exception as e:
        print(f"[Embedding Error] {e}")
        return None

# ==========================
# CARGA Y PERSISTENCIA
# ==========================

def cargar_data():
    global bloques, vectores
    bloques.clear()
    vectores.clear()

    if not os.path.exists(DATA_PATH):
        print("No se encontró DATA_PATH, inicializando vacío.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for linea in f:
            data = json.loads(linea)
            bloques.append(data)
            vectores.append(data["vector"])

def guardar_data():
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        for bloque, vector in zip(bloques, vectores):
            bloque_guardar = bloque.copy()
            bloque_guardar["vector"] = vector
            f.write(json.dumps(bloque_guardar, ensure_ascii=False) + "\n")

def cargar_indice():
    global index
    if not os.path.exists(INDEX_PATH):
        print("No se encontró INDEX_PATH, inicializando índice nuevo.")
        return
    index = faiss.read_index(INDEX_PATH)

def guardar_indice():
    if index is not None:
        faiss.write_index(index, INDEX_PATH)

def inicializar_memoria_vectorial():
    cargar_data()
    cargar_indice()
    if not index and vectores:
        construir_indice()
    print("✅ Memoria vectorial inicializada.")

# ==========================
# CONSTRUCCIÓN DE ÍNDICE
# ==========================

def construir_indice():
    global index
    if not vectores:
        return
    dimension = len(vectores[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectores).astype("float32"))
    guardar_indice()

# ==========================
# OPERACIONES DE MEMORIA
# ==========================

def agregar_bloque(texto, metadatos=None):
    emb = generar_embedding(texto)
    if not emb:
        return False
    bloque = {"texto": texto, "metadatos": metadatos or {}, "vector": emb}
    bloques.append(bloque)
    vectores.append(emb)
    if index is None:
        construir_indice()
    else:
        index.add(np.array([emb]).astype("float32"))
        guardar_indice()
    guardar_data()
    return True

def buscar_similares(texto, top_k=3):
    if not index:
        print("Índice no inicializado.")
        return []

    emb = generar_embedding(texto)
    if not emb:
        return []

    D, I = index.search(np.array([emb]).astype("float32"), top_k)
    resultados = []
    for idx in I[0]:
        if idx < len(bloques):
            resultados.append(bloques[idx])
    return resultados