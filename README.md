![lsst-texmf.lsst.io](https://img.shields.io/badge/lsst--texmf-lsst.io-blue.svg "Documentation") ![CI](https://github.com/lsst/lsst-texmf/workflows/CI/badge.svg)

# Rubin Observatory LSST LaTeX document class files

This repository contains LaTeX class and style files that can be used to create documents matching (reasonably closely) the LSST documentation standard.
This includes the `lsstdoc` class for documents (including LDM, DMTN, and SQR) and a `LSST-beamer` package for making Beamer slide decks.
lsst-texmf also includes DM's common BibTeX bibliographies.

**Documentation:** https://lsst-texmf.lsst.io.

## Quickstart

To use these class files clone this repository and set `$TEXMFHOME` to the location of the `texmf` subdirectory.
For example, with `bash` or `sh`:

```bash
git clone https://github.com/lsst/lsst-texmf
export TEXMFHOME=`pwd`/lsst-texmf/texmf
```

Additionally, add `lsst-texmf/bin` to you `PATH` so lsst-texmf's scripts such as `generateAcronyms.py` and `db2authors.py` are available.

Next, read the docs at https://lsst-texmf.lsst.io.

## Docker image

You can compile your document through an lsst-texmf Docker image to avoid installing LaTeX and lsst-texmf on your own computer:

```bash
docker run --rm -v `pwd`:/build -w /build lsstsqre/lsst-texmf:latest sh -c 'make'
```

[See the documentation for more information.](https://lsst-texmf.lsst.io/docker.html)

## Developers

Please refer to the [lsst-texmf Developer Guide](https://lsst-texmf.lsst.io/developer.html) for contribution information.

If adding or removing files from the `texmf` directory, please remember to run the `mktexlsr` command and commit the new version of `ls-R`.

```bash
mktexlsr --verbose texmf
```
