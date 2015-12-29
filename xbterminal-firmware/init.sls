{% from "xbterminal-firmware/map.jinja" import xbt with context %}



xbterminal-firmware:
  pkg:
    - installed
    - refresh: True
    - allow_updates: False
    - version:  {{ xbt.version }}
    - hold: True
  service:
    - running
    - enable: True
    - provider: systemd
    - watch:
      - file: local_config


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

local_config:
  file:
    - managed
    - name:  /srv/xbterminal/xbterminal/runtime/local_config
    - source: salt://xbterminal-firmware/files/local_config
    - template: jinja
    - context:
      local_config: {{ grains['xbt']['config'] }}
      ext_config: {{ xbt.config }}
