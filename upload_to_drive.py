from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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

def subir_resumen_a_drive(archivo_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    nombre_archivo = os.path.basename(archivo_path)
    file_metadata = {'name': nombre_archivo}
    media = MediaFileUpload(archivo_path, mimetype='text/plain')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"☁️ Archivo subido a Google Drive: {nombre_archivo} (ID: {file.get('id')})")