{% from "xbterminal-firmware/map.jinja" import xbt with context %}

xbterminal-rpc:
  pkg:
    - installed
    - refresh: True
    - allow_updates: False
    - version:  {{ xbt.rpc_version }}
    - hold: True
  service:
    - running
    - enable: True
    - provider: systemd

xbterminal-gui:
  pkg:
    - installed
    - refresh: True
    - allow_updates: False
    - version:  {{ xbt.gui_version }}
    - hold: True
  service:
    - running
    - enable: True
    - provider: systemd

/etc/salt/minion.d/check.conf:
  file:
    - absent
    - require:
      - pkg: xbterminal-rpc
      - pkg: xbterminal-gui
      - service: xbterminal-rpc
      - service: xbterminal-gui
