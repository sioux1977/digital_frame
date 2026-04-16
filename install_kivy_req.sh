#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "[1/4] Updating package index..."
sudo apt-get update

echo "[2/4] Installing core Kivy / SDL / graphics dependencies..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    pkg-config \
    git \
    libgl1-mesa-glx \
    libgles2-mesa \
    libegl1-mesa \
    libjpeg-dev \
    libmtdev1 \
    libmtdev-dev \
    xclip \
    xsel

echo "[3/4] Installing GStreamer multimedia dependencies..."
sudo apt-get install -y \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-alsa \
    gstreamer1.0-tools

echo "[4/4] Done."
echo
echo "System dependencies for Kivy have been installed."
echo "You can now install Kivy with pip, for example:"
echo '  python3 -m pip install "kivy[base]"'
