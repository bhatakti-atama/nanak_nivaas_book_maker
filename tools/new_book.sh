#!/usr/bin/env bash
# Start a new book from base_template.
#
#   tools/new_book.sh <folder_name> "<Gurmukhi title>" ["<subtitle>"] ["<author>"]
#
# Example:
#   tools/new_book.sh sarbloh_maryada "ਸਰਬਲੋਹ" "ਇੱਕ ਪੁਰਾਤਨ ਮਰਿਯਾਦਾ" "ਭਾਈ ਮਨਪ੍ਰੀਤ ਸਿੰਘ"
#
# Creates ./<folder_name>/ next to base_template/ with fonts, images, Makefile,
# Dockerfile and a main.tex whose book details are already filled in.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ $# -ge 2 ] || { sed -n '2,10p' "$0"; exit 1; }
NAME="$1"; TITLE="$2"; SUBTITLE="${3:-}"; AUTHOR="${4:-}"
DEST="$ROOT/$NAME"
[ ! -e "$DEST" ] || { echo "$DEST already exists" >&2; exit 1; }

mkdir "$DEST"
cp -r "$ROOT/base_template/fonts" "$ROOT/base_template/images" \
      "$ROOT/base_template/main.tex" "$ROOT/base_template/Makefile" \
      "$ROOT/base_template/Dockerfile" "$DEST/"

python3 - "$DEST" "$TITLE" "$SUBTITLE" "$AUTHOR" <<'PY'
import re, sys
dest, title, sub, author = sys.argv[1:5]
tex = open(f"{dest}/main.tex", encoding="utf-8").read()
tex = tex.replace("\\newcommand{\\booktitle}{ਕਿਤਾਬ ਦਾ ਨਾਮ}", f"\\newcommand{{\\booktitle}}{{{title}}}")
subline = sub
if author:
    subline = (sub + " \\\\[0.6em] " if sub else "") + "{\\Large " + author + "}"
tex = re.sub(r"\\newcommand\{\\booksubtitle\}\{[^\n]*\}", lambda m: "\\newcommand{\\booksubtitle}{" + subline + "}", tex, count=1)
open(f"{dest}/main.tex", "w", encoding="utf-8").write(tex)
mk = open(f"{dest}/Makefile", encoding="utf-8").read()
mk = re.sub(r"^TITLE = .*$", lambda m: f"TITLE = {title} {('- ' + sub) if sub else ''}".rstrip(), mk, flags=re.M)
mk = re.sub(r"^AUTHOR =.*$", lambda m: f"AUTHOR = {author}", mk, flags=re.M)
open(f"{dest}/Makefile", "w", encoding="utf-8").write(mk)
PY

echo "created $DEST"
echo "next: edit $NAME/main.tex (Bhumika, chapters, gallery), then: cd $NAME && make pdf"
