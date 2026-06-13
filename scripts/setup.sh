#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "================================================"
echo "  CAG Lab - Setup inicial"
echo "================================================"

echo ""
echo "[1/2] Instalando dependencias Python..."
pip install "redis>=4.0,<5.0"

echo ""
echo "[2/2] Verificando Redis..."
redis-cli ping && echo "Redis OK" || echo "ADVERTENCIA: Redis no esta corriendo. Inicialo antes de levantar el backend."

echo ""
echo "================================================"
echo "  Setup completo."
echo "  Para iniciar: ./scripts/run_dev.sh"
echo "  Para probar:  ./scripts/run_all_tests.sh"
echo "================================================"