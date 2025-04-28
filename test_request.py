import requests

url = "http://localhost:5000/log_event"

payload = {
    "user_id": "usuario_001",
    "tipo_evento": "fundacional",  # Usa las claves del dict: "fundacional", "polariad", etc.
    "contenido": "Descubrimiento clave sobre arquetipo del explorador.",
    "nivel": "Alto",
    "tags": ["arquetipo", "descubrimiento"]
}

response = requests.post(url, json=payload)

print("Código de respuesta:", response.status_code)
print("Respuesta del servidor:", response.json())