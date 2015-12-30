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


/etc/salt/minion.d/check.conf:
  file:
    - absent
    - require:
      - pkg: xbterminal-firmware
      - service: xbterminal-firmware
