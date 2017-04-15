# LSST Latex document class files

## Users
This repository contains Latex class and style files that can be used to create documents matching (reasonably closely) the LSST documentation standard. To use these class files clone this repository and set `$TEXMFLOCAL` to the location of the `texmf` subdirectory. For example, using `bash` or `sh`:
```bash
export TEXMFHOME=`pwd`/lsst-texmf/texmf
```
(if run from the cloned directory).

For all other help on setting up, available Latex classes, and how to use them, see [the user guide](docs/index.rst).

## Developers

If adding or removing files from the `texmf` directory, please remember to run the `mktexlsr` command and commit the new version of `ls-R`.

```
% mktexlsr --verbose texmf
```
