# Build the book PDF inside a TeX Live container (no local TeX install needed).
#
#   make pdf    LuaLaTeX build -> outlined text + invisible Unicode text layer
#   make clean  remove build leftovers
#
# The PDF is post-processed (tools/make_searchable.py) so that copy/paste and
# search give correct Gurmukhi in every viewer. Needs the project's Python
# venv:  ../.venv  (see requirements.txt)
IMAGE = nanak-niwas-latex
JOB   = raw
PY    = ../.venv/bin/python
FONT  = fonts/NotoSerifGurmukhi-Regular.ttf
TITLE = Nanak Niwas book template
AUTHOR =
DOCKER = docker run --rm -u $$(id -u):$$(id -g) -v "$(CURDIR)":/book -w /book $(IMAGE)

.PHONY: image pdf clean
image:
	docker build -t $(IMAGE) .

pdf: image
	$(DOCKER) lualatex -interaction=nonstopmode -jobname=$(JOB) main.tex
	$(DOCKER) lualatex -interaction=nonstopmode -jobname=$(JOB) main.tex
	$(DOCKER) lualatex -interaction=nonstopmode -jobname=$(JOB) main.tex
	$(DOCKER) gs -q -o $(JOB)_outlined.pdf -sDEVICE=pdfwrite -dNoOutputFonts -dCompatibilityLevel=1.7 -dPDFSETTINGS=/prepress $(JOB).pdf
	$(PY) ../tools/make_searchable.py $(JOB).pdf $(JOB)_outlined.pdf $(FONT) main.pdf "$(TITLE)" "$(AUTHOR)"
	$(PY) ../tools/verify_pdf.py main.pdf
	$(MAKE) clean

clean:
	$(RM) $(JOB).aux $(JOB).log $(JOB).out $(JOB).toc $(JOB).pdf $(JOB)_outlined.pdf
