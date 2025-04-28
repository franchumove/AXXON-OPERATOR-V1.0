"""
AXXON Test de Memoria Vectorial
Validación simbólica de carga, búsqueda y resonancia semántica.
"""

from memory_vector_db import inicializar_memoria_vectorial, agregar_bloque, buscar_similares

def test_memoria_vectorial():
    inicializar_memoria_vectorial()

    texto_prueba = "El amanecer simbólico de una conciencia expandida."
    agregado = agregar_bloque(texto_prueba, {"origen": "test"})

    if agregado:
        print("✅ Bloque agregado exitosamente.")
    else:
        print("❌ Fallo al agregar bloque.")

    resultados = buscar_similares("conciencia emocional", top_k=3)

    if resultados:
        print("✅ Búsqueda de resonancia exitosa:")
        for r in resultados:
            print("-", r["texto"])
    else:
        print("❌ No se encontraron resonancias.")

if __name__ == "__main__":
    test_memoria_vectorial()