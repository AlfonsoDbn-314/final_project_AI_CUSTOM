#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "================================================"
echo "  CAG Lab - Suite completa de pruebas"
echo "================================================"

echo ""
echo "[1/3] Pruebas base..."
PYTHONPATH=. python3 -m unittest discover -s tests/base -p 'test_*.py' -v

echo ""
echo "[2/3] Pruebas de validacion CAG..."
PYTHONPATH=. python3 -m unittest discover -s tests/validation -p 'test_*.py' -v

echo ""
echo "[3/3] Pruebas propias BDD/TDD..."
PYTHONPATH=. python3 -m unittest tests/test_cag_own.py -v

echo ""
echo "================================================"
echo "  Todas las pruebas completadas."
echo "================================================"