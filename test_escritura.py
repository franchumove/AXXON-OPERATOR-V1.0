from notion_writer import escribir_en_notion

escribir_en_notion(
    database_id="1d125466-211e-8072-8986-fc18d2a26890",  # <- Pega el verdadero de notion_config.json
    user_id="AXXON TEST",
    mensaje="Esto es un test de conexión simbólica.",
    tipo_evento="tablero_adaptativo",
    extra_tags=["debug", "test"]
)