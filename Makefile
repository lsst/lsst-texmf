
EXAMPLES = \
presentation.tex \
beamer-desc.tex \
beamer-LSST2016.tex \
DMTN-nnn.tex \
LDM-nnn.tex

TESTFILES = \
test-bibtex.tex

.SUFFIXES:
.SUFFIXES: .tex .pdf
PDF = $(EXAMPLES:.tex=.pdf)

TESTS = $(TESTFILES:.tex=.pdf)

all: $(PDF) $(TESTS)

$(PDF): %.pdf: examples/%.tex
	latexmk -xelatex -f $<

$(TESTS): %.pdf: tests/%.tex
	latexmk -pdf -bibtex -f $<

.PHONY: docs
docs: $(PDF) $(TESTS)
	mkdir -p docs/_static/examples
	cp *.pdf docs/_static/examples/
	make -C docs html

.PHONY: lsstthedocs
lsstthedocs:
	ltd-mason-travis --html-dir docs/_build/html

.PHONY: clean
clean:
	rm -f *.aux
	rm -f *.fdb_latexmk
	rm -f *.fls
	rm -f *.log
	rm -f *.out
	rm -f *.pdf
	rm -f *.toc
	rm -f *.nav
	rm -f *.snm
	make -C docs clean
	rm -f docs/_static/examples/*.pdf
