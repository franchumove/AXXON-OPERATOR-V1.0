from sheet_logger import log_event_simbolico

log_event_simbolico(
    user_id="debug_test",
    tipo_evento="casos",
    contenido="Test manual desde test_logger",
    nivel="alto",
    tags=["debug", "manual"]
)