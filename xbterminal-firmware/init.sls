{% from "xbterminal-firmware/map.jinja" import xbt with context %}

xbt/terminal/highstate:
  event.send:
    - data:
        pillar: {{ xbt }}



xbterminal-firmware:
  pkg:
    - installed
    - refresh: True
    - allow_updates: False
    - version:  '{{ xbt.version }}'
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
      - xbterminal-firmware-theme-{{ theme }}: '{{ version }}'
    {%- endfor %}

local_config:
  file:
    - managed
    - name:  /srv/xbterminal/xbterminal/runtime/local_config
    - source: salt://xbterminal-firmware/files/local_config
    - template: jinja
    - context:
      local_config: {{ grains['xbt']['config'] }}
      ext_config: {{ xbt.config }}


updated-system:
  pkg:
    - uptodate
    - refresh: True
    - require:
      - pkg: xbterminal-firmware
      - pkg: xbterminal-firmware-themes
      - file: local_config
      - event: xbt/terminal/highstate
      - file: /etc/salt/minion.d/check.conf

restart_terminal:
  module:
    - run
    - name: system.reboot
    - at_time: 1 #option requires 2015.8.3+ minion
    - require:
      - pkg: updated-system

/etc/salt/minion.d/check.conf:
  file:
    - managed
    - contents: |
       startup_states: 'sls'
       sls_list: xbterminal-firmware.check