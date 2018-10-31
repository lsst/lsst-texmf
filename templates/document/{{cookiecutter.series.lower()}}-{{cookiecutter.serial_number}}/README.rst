.. image:: https://img.shields.io/badge/{{ cookiecutter.series.lower() }}--{{ cookiecutter.serial_number }}-lsst.io-brightgreen.svg
   :target: https://{{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}.lsst.io
.. image:: https://travis-ci.org/{{ cookiecutter.github_org }}/{{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}.svg
   :target: https://travis-ci.org/{{ cookiecutter.github_org }}/{{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}

{{ "#" * cookiecutter.title|length }}
{{ cookiecutter.title }}
{{ "#" * cookiecutter.title|length }}

{{ cookiecutter.series.upper() }}-{{ cookiecutter.serial_number }}
{{ "-" * (cookiecutter.series|length + cookiecutter.serial_number|length + 1) }}

{{ cookiecutter.abstract }}

To compile this document you need to have set up https://github.com/lsst/lsst-texmf. The bin directory of texmf must be in your path for generateAcronyms.py to be found and  work. 
**Links**

{% if cookiecutter.docushare_url|length > 0 %}
- Accepted version on DocuShare: {{ cookiecutter.docushare_url }}
{% endif %}
- Live drafts: https://{{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}.lsst.io
- GitHub: https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}

****

Copyright {{ cookiecutter.copyright_year }} {{ cookiecutter.copyright_holder }}

{% if cookiecutter.license_cc_by %}
This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.
{% endif %}
