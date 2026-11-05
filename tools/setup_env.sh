#!/usr/bin/env bash
# One-time setup of the project's Python virtual environment (.venv).
# Works even where `python3 -m venv` is unavailable (no python3-venv / ensurepip).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -x .venv/bin/python ]; then
  if python3 -m venv .venv 2>/dev/null; then
    echo "created .venv with python3 -m venv"
  else
    # ensurepip missing: create without pip, then bootstrap pip from a wheel
    rm -rf .venv
    python3 -m venv --without-pip .venv
    WHEEL="$(ls ~/.local/lib/python3*/site-packages/virtualenv/seed/wheels/embed/pip-*.whl 2>/dev/null | tail -1 || true)"
    if [ -z "$WHEEL" ]; then
      echo "Cannot bootstrap pip: install python3-venv (sudo apt install python3-venv) and re-run." >&2
      exit 1
    fi
    .venv/bin/python "$WHEEL/pip" install --no-index "$WHEEL"
  fi
fi

.venv/bin/pip install -q -r requirements.txt
echo "ready: $(.venv/bin/python -c 'import pymupdf; print("pymupdf", pymupdf.__version__)' 2>/dev/null)"
echo "check Docker too: $(docker --version 2>/dev/null || echo 'docker NOT found')"
