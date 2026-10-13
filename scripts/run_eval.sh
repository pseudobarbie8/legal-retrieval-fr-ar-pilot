#!/usr/bin/env bash
set -euo pipefail

python scripts/validate_data.py

RUN_DIR="results/$(date +%Y%m%d_%H%M%S)"
python eval/evaluate.py "$RUN_DIR"
echo "Raw run saved to $RUN_DIR"
