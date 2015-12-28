{% from "xbterminal-firmware/map.jinja" import xbt with context %}

xbterminal-firmware:
  pkg:
    - installed
    - refresh: True
    - allow_updates: False
    - version:  {{ xbt.version }}
    - hold: True

xbterminal-firmware-themes:
  pkg:
    - installed
    - hold: True
    - pkgs:
	{%- for theme, version in xbt.themes.iteritems() %}
      - xbterminal-firmware-theme-{{ theme }}: {{ version }}
  {%- endfor %}

updated-system:
  pkg:
    - uptodate
    - refresh: True
    - require:
      - pkg: xbterminal-firmware
      - pkg: xbterminal-firmware-themes
