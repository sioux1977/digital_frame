#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/Documenti/progetti/digital_frame"
VENV_PYTHON="${PROJECT_DIR}/.venv/bin/python"

export KIVY_NO_ARGS=1
export KIVY_NO_CONSOLELOG=0
export KIVY_LOG_LEVEL=info
export KIVY_WINDOW=auto
export KIVY_GL_BACKEND=gl

cd "${PROJECT_DIR}"

exec "${VENV_PYTHON}" main.py
