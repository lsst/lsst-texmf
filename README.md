# LSST Latex document class files

This repository contains Latex class and style files that can be used to create documents matching (reasonably closely) the LSST documentation standard.
To use these class files check out this repository and set `$TEXMFLOCAL` to the location of the `texmf` subdirectory.
Template files with example usage can be found in the `examples` directory.

*Developer note:*

If adding or removing files from the `texmf` directory, please remember to run the `mktexlsr` command and commit the new version of `ls-R`.

```
% mktexlsr --verbose texmf
```
