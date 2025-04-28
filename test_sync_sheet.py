import requests

res = requests.get("http://localhost:5500/sync-sheet-to-notion/tablero_adaptativo")
print(res.json())