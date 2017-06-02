{{ cookiecutter.slug }}.pdf: *.tex
	latexmk -bibtex -pdf -f {{ cookiecutter.slug }}.tex

.PHONY: clean
clean:
	latexmk -c {{ cookiecutter.slug }}.tex
