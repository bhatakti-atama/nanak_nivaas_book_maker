# Nanak Niwas book maker

Gurmukhi books (A5, LaTeX) built from one clean template, with PDFs that are
searchable and copy/paste-safe in every viewer.

```
base_template/   base book: cover, Bhumika, Nanak Niwas page, photo gallery
havan_maryada/   example book built from the template
tools/           setup_env.sh, new_book.sh, make_searchable.py, verify_pdf.py
.claude/skills/nanak-book/   Claude Code project skill with the rules below
```

## Quick start

```bash
tools/setup_env.sh                       # once: .venv + PyMuPDF (needs Docker too)
tools/new_book.sh my_book "ਸਿਰਲੇਖ" "ਉਪ-ਸਿਰਲੇਖ" "ਲੇਖਕ"
cd my_book && make pdf                   # -> main.pdf
```

`make pdf` builds in a TeX Live Docker container (no local TeX needed):
LuaLaTeX x3 -> Ghostscript outlines the text -> `tools/make_searchable.py`
adds an invisible logical-order Unicode text layer -> `main.pdf`.
Gurmukhi stores ਿ before its letter in the drawing order, so without this step
pdf.js/browser viewers copy and search it wrongly.

## Writing a book

Edit `main.tex` in your book folder: replace the Bhumika placeholder, add chapters
at `ADD NEW CHAPTERS HERE`, swap `images/cover.jpg` and edit the `\galleryphoto`
lines. Rules (full list in the skill): use `\chapter*` only, wrap Latin text and
numbers in `\eng{...}`, give every image alt text, keep `\DocumentMetadata` first.
