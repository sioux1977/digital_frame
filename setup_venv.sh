#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/Documenti/progetti/digital_frame"
VENV_DIR="${PROJECT_DIR}/.venv"

cd "${PROJECT_DIR}"

python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install "kivy[base]"

echo
echo "Virtual environment ready:"
echo "  source ${VENV_DIR}/bin/activate"
echo "Run app with:"
echo "  ${VENV_DIR}/bin/python main.py"
