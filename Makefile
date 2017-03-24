
EXAMPLES = \
Example_presentation.tex \
Example-beamer-desc.tex \
Example-beamer-LSST2016.tex \
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
	rm -f -R _build
