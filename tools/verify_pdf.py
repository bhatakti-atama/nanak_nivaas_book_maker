#!/usr/bin/env python3
"""Check that a book PDF copies/searches correctly in strict viewers.

Usage: verify_pdf.py book/main.pdf ["phrase to find" ...]

Uses pypdf (reads the raw glyph stream like pdf.js does), not just PyMuPDF.
Fails (exit 1) if a word starts with a stray vowel sign ਿ (= visual-order bug)
or if a given phrase cannot be found.
"""
import re
import sys

import pypdf

path, phrases = sys.argv[1], sys.argv[2:]
pages = [p.extract_text() or "" for p in pypdf.PdfReader(path).pages]
text = "\n".join(pages)

stray = re.findall(r"(?:^|[\s(])ਿ\S*", text)
print(f"{path}: {len(pages)} pages, {len(text)} characters of text")
print(f"words starting with a stray ਿ: {len(stray)} {stray[:5]}")
ok = not stray
for ph in phrases:
    hits = [i + 1 for i, t in enumerate(pages) if ph in t]
    print(f"'{ph}': pages {hits[:8] or 'NOT FOUND'}")
    ok = ok and bool(hits)
sys.exit(0 if ok and text.strip() else 1)
