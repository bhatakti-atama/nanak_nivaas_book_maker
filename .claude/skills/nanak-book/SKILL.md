---
name: nanak-book
description: Create, edit or build a Nanak Niwas Gurmukhi book (LaTeX, A5) from base_template, and produce a searchable, copy-paste-safe PDF. Use when asked to start a new book, add chapters/photos, convert source text (PDF/doc) into the template, or build/fix the PDF.
---

# Nanak Niwas book workflow

Project layout (repo root = `nanak_nivaas_book_maker/`):

```
base_template/      the clean base book: cover, Bhumika, Nanak Niwas page, photo gallery
<book_folder>/      one folder per book (e.g. havan_maryada/), created from base_template
tools/new_book.sh   start a new book from base_template
tools/setup_env.sh  one-time: create .venv + install requirements.txt
tools/make_searchable.py  post-process step (called by `make pdf`)
tools/verify_pdf.py       checks copy/search order with pypdf (also called by `make pdf`)
.venv/              Python env (PyMuPDF) - git-ignored
```

## Start a new book
1. `tools/setup_env.sh` (once; also needs Docker).
2. `tools/new_book.sh <folder> "<title>" "<subtitle>" "<author>"`
3. Put the new text in `<folder>/main.tex` where it says `ADD NEW CHAPTERS HERE`.
   Replace the Bhumika placeholder, the sevadar list and the cover image
   (`images/cover.jpg`); edit the `\galleryphoto{file}{caption}` lines (photos in `images/gallery/`).
4. `cd <folder> && make pdf` -> `main.pdf`.

Extracting text from a source PDF: use PyMuPDF from the venv
(`.venv/bin/python -I`, `pymupdf.open(f)[i].get_text()`), then READ THE RENDERED PAGES
(Read tool with `pages=`) to catch what extraction misses (tables, equations, broken glyphs).

## LaTeX rules for this template (do not break these)
- Build engine is **LuaLaTeX** (HarfBuzz renderer). Not XeLaTeX.
- Headings: use **`\chapter*{...}`** + `\addcontentsline{toc}{chapter}{...}`. Only the starred
  form is supported (custom `\chapter` in the preamble). Use `\section*`, `\subsection*` below it.
  Do not load `titlesec` (incompatible with the tagged-PDF setup).
- `\DocumentMetadata{...}` must stay the first thing in `main.tex`.
- The Gurmukhi font has no Latin letters and renders ASCII digits oddly: wrap Latin text
  and numbers in `\eng{...}` (e.g. `\eng{betula utilis}`, `\eng{94\%}`). Chapter numbers too:
  `\chapter*{\eng{3.} ਨਾਮ}`.
- Escape `%`, `&`, `_`, `#`. Use curly quotes “ ” in text, not `"`.
- Tables: `longtable` with `\rowcolors`; avoid `\hline` and vertical rules (they stick out under `\rowcolors`).
- Every `\includegraphics` needs `alt={...}` (tagged PDF); `\galleryphoto` already adds it.
- Don't wrap `\bfseries` around Gurmukhi in macros that reset the font: heading styles already
  select `\punjabifont`.

## Searchable / copyable PDF (why `make pdf` is more than LuaLaTeX)
Shaped Gurmukhi is stored in visual order (ਿ before its letter), so pdf.js/pdfminer/browser
viewers copy "ਿਕਹਾ". `make pdf` therefore: LuaLaTeX x3 (job name `raw`) -> Ghostscript
`-dNoOutputFonts` (text to outlines) -> `tools/make_searchable.py` adds an invisible
(render mode 3) logical-order Unicode text layer, sets title/author, writes `main.pdf`,
then `make clean` removes `raw.*`.
- Set the PDF title/author in the book's `Makefile` (`TITLE`, `AUTHOR`).
- `make pdf` runs `tools/verify_pdf.py` (pypdf, NOT PyMuPDF - PyMuPDF hides the problem); run it by hand with phrases: `.venv/bin/python tools/verify_pdf.py main.pdf "ਹਵਨ ਕੀ ਹੈ"`: page text must read
  `ਕਿਹਾ`, and no word may start with a stray `ਿ`.
- Symbols missing from the Gurmukhi font (e.g. `→`) are copied as ASCII (`->`).

## Checks before saying "done"
- Open/render several pages (Ghostscript PNG via the Docker image) and look at cover, headings,
  tables, gallery - don't trust the log alone.
- Log: no `Missing character`, no `! ` errors; overfull boxes under ~10pt are acceptable.
- Text spot-check against the source (Gurmukhi was transcribed from extracted text).
