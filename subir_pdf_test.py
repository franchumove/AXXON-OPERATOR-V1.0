from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def subir_a_drive(archivo_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    nombre_archivo = os.path.basename(archivo_path)
    file_metadata = {'name': nombre_archivo, 'mimeType': 'application/pdf'}
    media = MediaFileUpload(archivo_path, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    print(f"✅ PDF subido: {nombre_archivo}")
    print(f"🔗 Link: {file['webViewLink']}")

# CAMBIA este nombre al archivo que tengas en tu carpeta
subir_a_drive("resumenes/ejemplo_resumen.pdf")