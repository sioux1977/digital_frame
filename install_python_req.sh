#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "[1/4] Updating apt package index..."
sudo apt-get update

echo "[2/4] Installing system packages..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    pkg-config \
    git

echo "[3/4] Upgrading pip tooling..."
python3 -m pip install --upgrade pip setuptools wheel

echo "[4/4] Installing Python dependencies..."
python3 -m pip install "kivy[base]"

echo
echo "Done."
echo "Installed Python packages:"
python3 -m pip show kivy || true
