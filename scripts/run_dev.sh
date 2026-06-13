#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "================================================"
echo "  CAG Lab - Verificacion del entorno"
echo "================================================"

echo ""
echo "[1/3] Verificando Python..."
python3 --version || { echo "ERROR: Python3 no encontrado"; exit 1; }

echo ""
echo "[2/3] Verificando Redis..."
redis-cli ping || { echo "ERROR: Redis no esta corriendo. Inicia Redis primero."; exit 1; }

echo ""
echo "[3/3] Verificando dependencias Python..."
python3 -c "import redis; print('redis-py OK')" || { echo "ERROR: Instala redis con: pip install redis>=4.0,<5.0"; exit 1; }

echo ""
echo "================================================"
echo "  Entorno verificado. Iniciando backend..."
echo "  Frontend: abre frontend/index.html en el navegador"
echo "================================================"
echo ""

PYTHONPATH=. python3 -m backend.server