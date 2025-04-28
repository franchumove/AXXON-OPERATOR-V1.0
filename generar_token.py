from google_auth_oauthlib.flow import InstalledAppFlow
import os
import json

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def generar_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)

    # 🔗 Este flujo es manual, y sí funciona en Replit
    auth_url, _ = flow.authorization_url(prompt='consent')
    print("🔗 ABRE ESTE LINK EN TU NAVEGADOR:")
    print(auth_url)

    code = input("🔐 PEGA AQUÍ EL CÓDIGO DE AUTORIZACIÓN: ")
    flow.fetch_token(code=code)

    creds = flow.credentials
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    print("✅ Token generado y guardado en token.json")

if __name__ == "__main__":
    generar_token()
