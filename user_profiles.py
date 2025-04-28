"""
AXXON - Módulo de Perfiles Cognitivos

Define el arquetipo simbólico base de cada usuario y su configuración emocional.
"""

import os
import json

PERFILES_PATH = "data/user_profiles.json"

# Crear la carpeta 'data/' si no existe
os.makedirs(os.path.dirname(PERFILES_PATH), exist_ok=True)

# Crear el archivo 'user_profiles.json' vacío si no existe
if not os.path.isfile(PERFILES_PATH):
    with open(PERFILES_PATH, "w") as f:
        json.dump({}, f)

def cargar_perfiles():
    with open(PERFILES_PATH, "r") as f:
        return json.load(f)

def guardar_perfiles(perfiles):
    with open(PERFILES_PATH, "w") as f:
        json.dump(perfiles, f, indent=4)

def obtener_perfil(user_id):
    perfiles = cargar_perfiles()
    return perfiles.get(user_id, {
        "arquetipo": "explorer",
        "sensibilidad": "media",
        "tono_preferido": "explorador"
    })

def actualizar_perfil(user_id, arquetipo=None, sensibilidad=None, tono=None):
    perfiles = cargar_perfiles()
    perfil = perfiles.get(user_id, {})
    if arquetipo:
        perfil["arquetipo"] = arquetipo
    if sensibilidad:
        perfil["sensibilidad"] = sensibilidad
    if tono:
        perfil["tono_preferido"] = tono
    perfiles[user_id] = perfil
    guardar_perfiles(perfiles)
    return perfil

def evaluar_perfil_usuario(user_id, mensaje, emocion, tono):
    """
    Heurística básica para actualizar el perfil simbólico de usuario.
    """
    perfil = obtener_perfil(user_id)

    # Ajustes heurísticos simples (puedes expandir)
    if emocion in ["frustración", "ansiedad"]:
        perfil["sensibilidad"] = "alta"
    elif emocion in ["curiosidad", "interés"]:
        perfil["sensibilidad"] = "media"

    if tono:
        perfil["tono_preferido"] = tono

    actualizar_perfil(user_id, perfil.get("arquetipo"), perfil.get("sensibilidad"), perfil.get("tono_preferido"))
    return perfil