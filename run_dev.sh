#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/Documenti/progetti/digital_frame"
VENV_PYTHON="${PROJECT_DIR}/.venv/bin/python"

export KIVY_NO_ARGS=1
export KIVY_LOG_LEVEL=debug
export KIVY_WINDOW=egl_rpi
export KIVY_GL_BACKEND=gl
export KIVY_BCM_DISPMANX_ID=2

cd "${PROJECT_DIR}"

exec "${VENV_PYTHON}" main.py
