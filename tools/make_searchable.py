#!/usr/bin/env python3
"""Make a LaTeX-built Gurmukhi PDF copy/paste- and search-friendly in every viewer.

Why: a shaped Gurmukhi PDF stores glyphs in *visual* order (the vowel sign
ਿ is drawn before its letter), so viewers that only look at the glyph stream
(pdf.js, pdfminer, many web viewers) copy "ਿਕਹਾ" instead of "ਕਿਹਾ".

What this script does:
  1. reads the *logical* text + positions from the source PDF (PyMuPDF
     understands the /ActualText spans LuaLaTeX writes),
  2. takes an "outlined" copy of the PDF (all text converted to vector
     shapes by Ghostscript, so no visual-order glyph stream remains),
  3. lays an invisible text layer (render mode 3) in logical order on top.

Usage: make_searchable.py SOURCE.pdf OUTLINED.pdf FONT.ttf OUTPUT.pdf [TITLE] [AUTHOR]
"""
import os
import sys
import pymupdf

src_path, outlined_path, font_path, out_path = sys.argv[1:5]
title = sys.argv[5] if len(sys.argv) > 5 else ""
author = sys.argv[6] if len(sys.argv) > 6 else ""

src = pymupdf.open(src_path)
dst = pymupdf.open(outlined_path)
assert len(src) == len(dst), "page count differs between source and outlined PDF"

gur = pymupdf.Font(fontfile=font_path)
latin = pymupdf.Font("helv")        # ASCII fallback (base-14, no embedding)
# Symbols the fonts above lack are written in plain ASCII instead.
ASCII_FALLBACK = {"\u2192": "->", "\u2190": "<-"}


def pick(ch):
    """Return (font key, Font) able to show this character."""
    if gur.has_glyph(ord(ch)):
        return "gur", gur
    if ord(ch) < 256 and latin.has_glyph(ord(ch)):
        return "latin", latin
    return "skip", None


def runs(text):
    out = []
    for ch in "".join(ASCII_FALLBACK.get(c, c) for c in text):
        key, font = pick(ch)
        if key == "skip":
            continue
        if out and out[-1][0] == key:
            out[-1][2].append(ch)
        else:
            out.append([key, font, [ch]])
    return [(k, f, "".join(c)) for k, f, c in out]


n_chars = 0
for page_no, (sp, dp) in enumerate(zip(src, dst)):
    dp.insert_font(fontname="gur", fontfile=font_path)
    for block in sp.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                text = span["text"]
                if not text.strip():
                    continue
                size = span["size"]
                x0, _, x1, _ = span["bbox"]
                ox, oy = span["origin"]
                pieces = runs(text)
                natural = sum(f.text_length(t, fontsize=size) for _, f, t in pieces)
                if natural <= 0:
                    continue
                sx = (x1 - x0) / natural   # stretch to the visible width
                x = ox
                for key, font, t in pieces:
                    w = font.text_length(t, fontsize=size) * sx
                    name = {"gur": "gur", "latin": "helv"}[key]
                    dp.insert_text(
                        pymupdf.Point(x, oy), t,
                        fontname=name,
                        fontfile=None,
                        fontsize=size, render_mode=3,
                        morph=(pymupdf.Point(x, oy), pymupdf.Matrix(sx, 0, 0, 1, 0, 0)),
                    )
                    x += w
                n_chars += len(text)

meta = dst.metadata or {}
if title:
    meta["title"] = title
if author:
    meta["author"] = author
meta["producer"] = "LuaLaTeX + Ghostscript + PyMuPDF"
dst.set_metadata(meta)
dst.save(out_path, garbage=4, deflate=True)
print(f"{out_path}: {len(dst)} pages, {n_chars} characters in the invisible text layer")
