"""Utilities shared by the author database tooling.

This module must stay free of heavyweight imports so that both the
author database model layer and the command line tools can use it.
"""

from __future__ import annotations

import functools
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pylatexenc.latex2text import LatexNodes2Text

__all__ = ["check_orcid", "latex2text"]


@functools.cache
def _latex_converter() -> LatexNodes2Text:
    """Return a shared LaTeX-to-text converter.

    Conversion is stateless and construction is relatively expensive, so a
    single converter is reused. The import is deferred so that tools that
    never convert LaTeX do not require pylatexenc.
    """
    from pylatexenc.latex2text import LatexNodes2Text

    return LatexNodes2Text()


@functools.cache
def latex2text(latex: str) -> str:
    """Convert a LaTeX string into a plain text string.

    Parameters
    ----------
    latex : `str`
        Latex string to convert.

    Returns
    -------
    plain : `str`
        The plain text version.
    """
    return _latex_converter().latex_to_text(latex)


def check_orcid(orcid: str | None) -> str | None:
    """Validate and normalize an ORCID identifier.

    Parameters
    ----------
    orcid : `str` or `None`
        A bare dashed or 16-character ORCID identifier.

    Returns
    -------
    normalized : `str` or `None`
        The dashed identifier, or `None`.

    Raises
    ------
    ValueError
        Raised if the identifier is not in a recognized bare form.
    """
    if orcid is None:
        return None
    if re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[0-9X]", orcid):
        return orcid
    if re.fullmatch(r"\d{15}[0-9X]", orcid):
        return "-".join(orcid[i : i + 4] for i in range(0, len(orcid), 4))
    raise ValueError(f"Given ORCiD does not match standard form: {orcid}")
