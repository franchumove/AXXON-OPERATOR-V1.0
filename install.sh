#!/usr/bin/env bash

# Installer para AXXON Core - Protocolo Simbólico v2.0
# Autor: AXXON DevCore

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SYMBOL_LOADING="⏳"
SYMBOL_SUCCESS="✅"
SYMBOL_ERROR="❌"
SYMBOL_INFO="ℹ️"

error_exit() {
    echo -e "${RED}${SYMBOL_ERROR} $1${NC}" >&2
    exit 1
}

check_command() {
    command -v "$1" >/dev/null 2>&1 || error_exit "Requiere $1 pero no está instalado."
}

echo -e "${BLUE}🌀 Iniciando Protocolo de Instalación Simbólica AXXON...${NC}\n"

# ========================
# 🔍 Verificación de entorno
# ========================
echo -e "${YELLOW}${SYMBOL_LOADING} Verificando entorno simbólico...${NC}"
check_command python3
check_command pip

# ========================
# 🔄 Actualización de Pip
# ========================
echo -e "\n${YELLOW}${SYMBOL_LOADING} Actualizando Núcleo Pip...${NC}"
python3 -m pip install --upgrade pip || error_exit "Fallo al actualizar pip."

# ========================
# 📚 Instalación de dependencias
# ========================
REQUIREMENTS_FILE="requirements.txt"

echo -e "\n${YELLOW}${SYMBOL_LOADING} Buscando Matriz de Dependencias...${NC}"
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    error_exit "Archivo $REQUIREMENTS_FILE no encontrado."
fi

echo -e "${YELLOW}${SYMBOL_LOADING} Instalando Componentes Simbólicos...${NC}"
pip install --upgrade -r "$REQUIREMENTS_FILE" || error_exit "Error al instalar dependencias."

# ========================
# 🧠 Resultado Final
# ========================
echo -e "\n${GREEN}${SYMBOL_SUCCESS} Instalación Completa. Bienvenido al Núcleo AXXON.${NC}"
echo -e "${BLUE}🔮 Ejecuta 'python3 main_orquestador.py' para iniciar el orquestador simbólico.${NC}"
