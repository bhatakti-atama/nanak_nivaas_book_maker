#!/usr/bin/env bash
# Regenerate the PDF of a book.   Usage: ./build_pdf.sh [book_folder]   (default: havan_maryada)
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
book="${1:-havan_maryada}"
book="${book%/}"
[ -f "$root/$book/Makefile" ] || { echo "No Makefile in $root/$book" >&2; exit 1; }
[ -x "$root/.venv/bin/python" ] || { echo "Missing .venv - run tools/setup_env.sh first" >&2; exit 1; }
cd "$root/$book"
make pdf
echo "Done: $root/$book/main.pdf"
