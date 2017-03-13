
EXAMPLES = \
Example_presentation.tex \
LDM-nnn.tex

.SUFFIXES:
.SUFFIXES: .tex .pdf
PDF = $(EXAMPLES:.tex=.pdf)

all: $(PDF)

$(PDF): %.pdf: examples/%.tex
	latexmk -pdf -f $<

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
