{{ "#" * cookiecutter.title|length }}
{{ cookiecutter.title }}
{{ "#" * cookiecutter.title|length }}

Presentation by {{ cookiecutter.presenter }} at {{ cookiecutter.venue }} on {{ cookiecutter.date }}.

How to compile
==============

This presentation is built with the ``LSST-beamer`` package that comes with `lsst-texmf <https://lsst-texmf.lsst.io>`_.
To compile:

1. Ensure the ``TEXMFHOME`` environment variable is set to ``lsst-texmf``.
   See `Installing lsst-texmf <https://lsst-texmf.lsst.io/install.html>`_ for details.
2. Run ``make``.

For more information about LSST-beamer:

- Documentation: https://lsst-texmf.lsst.io/beamer.html
- Examples: https://lsst-texmf.lsst.io/examples/index.html#presentations

****

Copyright {{ cookiecutter.copyright_year }} {{ cookiecutter.copyright_holder }}

{% if cookiecutter.license_cc_by %}
This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.
{% endif %}
