#!/bin/bash
set -e

SERVICE_NAME=$(basename "$(pwd)")
REPO_DIR="$(cd "$(dirname "$0")"; pwd)"
VENV_DIR="$REPO_DIR/venv"

echo "🛑 Menghentikan dan menghapus systemd service '$SERVICE_NAME'..."

if systemctl list-unit-files | grep -q "^$SERVICE_NAME.service"; then
    sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
    sudo rm -f "/etc/systemd/system/$SERVICE_NAME.service"
    sudo systemctl daemon-reload
    sudo systemctl reset-failed "$SERVICE_NAME" 2>/dev/null || true
    echo "✅ Service '$SERVICE_NAME' berhasil dihapus."
else
    echo "ℹ️ Service '$SERVICE_NAME' tidak ditemukan atau sudah dinonaktifkan."
fi

# Hapus log journal untuk service ini
echo "🗑️ Menghapus log journal untuk '$SERVICE_NAME'..."
sudo journalctl --rotate 2>/dev/null || true
sudo journalctl --vacuum-time=1s --unit="$SERVICE_NAME" 2>/dev/null || true
echo "✅ Log journal dibersihkan."

# Hapus virtual environment jika ada
if [ -d "$VENV_DIR" ]; then
    echo "🧹 Menghapus virtual environment..."
    rm -rf "$VENV_DIR"
    echo "✅ Virtual environment dihapus."
else
    echo "ℹ️ Virtual environment tidak ditemukan."
fi

echo ""
echo "🧼 Pembersihan selesai!"