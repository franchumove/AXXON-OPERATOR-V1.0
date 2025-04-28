# AXXON OPERATOR - README OPERATIVO

**Versión:** MVP+ 2025  
**Autor:** AXXON DevCore

---

## ¿Qué es AXXON OPERATOR?

Sistema simbólico modular para:

- Procesar mensajes emocionales.
- Crear y lanzar recordatorios automáticos.
- Generar respuestas simbólicas adaptativas.
- Enviar mensajes de recordatorio por Email o Telegram.
- Exportar contenidos a PDF y Word.
- Buscar información simbólica en Internet.
- Sincronizar memoria viva con Google Sheets y Notion.

---

## Estructura de Carpetas

/core/
generate_response.py
memory_engine.py
inference_engine.py
/operadores/
email_sender.py
word_generator.py
pdf_generator.py
web_scraper.py
reminder_manager.py
trigger_manager.py
telegram_sender.py
/main_orquestador.py
/runner.py
/.env
requirements.txt

---

## Instalación y Configuración

1. **Descargar proyecto**.
2. **Crear archivo `.env`** basado en el modelo de ejemplo.
3. **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Configurar servicios**:
    - OpenAI
    - Notion
    - Google Drive/Sheets
    - SMTP Email
    - SerpAPI
    - Telegram Bot

---

## Comandos principales

- Levantar sistema completo:
    ```bash
    python runner.py
    ```

- Webhook para recibir mensajes:
    ```http
    POST /webhook
    {
      "user_id": "usuario1",
      "message": "Tengo dudas sobre mi propósito"
    }
    ```

- Subir un PDF y resumirlo simbólicamente:
    ```http
    POST /subir-pdf
    ```

- Sincronizar memorias:
    ```http
    GET /sync-sheet
    ```

---

## Funciones Automáticas

- Revisar recordatorios vencidos cada 1 minuto.
- Actualizar memoria simbólica cada 24 horas.
- Disparar recordatorios vía Email y Telegram.

---

## Recomendaciones

- Subir a producción con Render, Railway o Replit Deploy.
- Mantener copias de seguridad de la base de datos y la memoria viva.
- Mantener actualizadas las credenciales externas.

---

> **AXXON OPERATOR ahora vibra simbólicamente en cada acción que realiza.**

---