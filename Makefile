
EXAMPLES = \
presentation.tex \
beamer-desc.tex \
beamer-LSST2016.tex \
DMTN-nnn.tex \
MEMO-nnn.tex \
test-report.tex \
test-specification.tex \
LDM-nnn.tex

TESTFILES = \
test-bibtex.tex

# Bibliographies that are tested for pybtex compatibility
# Ignores the gaialink bibliography
BIBFILES = \
texmf/bibtex/bib/books.bib \
texmf/bibtex/bib/lsst.bib \
texmf/bibtex/bib/lsst-dm.bib \
texmf/bibtex/bib/refs.bib \
texmf/bibtex/bib/refs_ads.bib

.SUFFIXES:
.SUFFIXES: .tex .pdf
PDF = $(EXAMPLES:.tex=.pdf)

TESTS = $(TESTFILES:.tex=.pdf)

all: $(PDF) $(TESTS) glossary-table.pdf full-glossary.pdf

$(PDF): %.pdf: examples/%.tex
	latexmk -xelatex -f $<

$(TESTS): %.pdf: tests/%.tex
	latexmk -pdf -bibtex -f $<

test-acronyms: glossary-table.pdf

glossary-table.pdf: glstab.tex
	latexmk -xelatex -f examples/glossary-table.tex

full-glossary.pdf: glstab.tex
	bin/generateAcronyms.py -g --writeallacronyms --noadorn fullgls.tex
	latexmk -xelatex -f examples/full-glossary.tex
	makeglossaries full-glossary
	xelatex examples/full-glossary.tex

glstab.tex:
	@echo "Testing glossarydefs"
	@echo
	bin/generateAcronyms.py -c glstab.tex

.PHONY: test-pybtex
test-pybtex:
	@echo "Testing pybtex compatibility"
	@echo
	bin/validate_bib.py $(BIBFILES)

.PHONY: test-authors
test-authors:
	@echo "Testing authorsdb"
	@echo
	bin/validate_authors.py

authors.csv: etc/authordb.yaml
	bin/db2authors.py -m csvall

.PHONY: docs
docs: $(PDF) $(TESTS) glstab.tex authors.csv
	mkdir -p docs/_static/examples
	cp *.pdf docs/_static/examples/
	cp etc/glossary.html docs
	cp htmlglossary.csv docs
	cp af*.csv authors.csv docs
	make -C docs html

lsst.bib:
	bin/generateBibfile.py --external texmf/bibtex/bib/lsst.bib --external etc/static_entries.bib --dois etc/dois.yaml texmf/bibtex/bib/lsst.bib

processadbform:
	python3 $(TEXMFHOME)/../bin/makeAuthorListsFromGoogle.py -s `cat skip` --adb -p 1CGxjpPuyNJ_gXRHTvkEF0qeI0XedQ-GQgbmyzWFLSUE "A2:I1000"

# skip here is how far down the sheet we already processed - do not want to reprocess
processsignup:
	python3 $(TEXMFHOME)/../bin/makeAuthorListsFromGoogle.py --signup -p 1CGxjpPuyNJ_gXRHTvkEF0qeI0XedQ-GQgbmyzWFLSUE "GenPaper!A2:I1000"

merge_authors: new_authors.yaml
	python3 $(TEXMFHOME)/../bin/makeAuthorListsFromGoogle.py -m new_authors.yaml

merge_affil: new_affiliations.yaml
	python3 $(TEXMFHOME)/../bin/makeAuthorListsFromGoogle.py -a new_affiliations.yaml

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
	rm -f *.bbl
	rm -f *.bbg
	rm -f *.blg
	rm -f *.xdv
	rm -f testbibfile.bib
	make -C docs clean
	rm -f docs/_static/examples/*.pdf
