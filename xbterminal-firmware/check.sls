{% from "xbterminal-firmware/map.jinja" import xbt with context %}

xbterminal-package:
  pkg:
    - installed
    - name: '{{ salt['grains.get']('xbt-package', 'xbterminal-rpc') }}'
    - refresh: True
    - allow_updates: False
    - version:  {{ xbt.version }}
    - hold: True

xbterminal-service:
  service:
    - running
    - name: '{{ salt['grains.get']('xbt-package', 'xbterminal-rpc') }}'
    - enable: True
    - provider: systemd


/etc/salt/minion.d/check.conf:
  file:
    - absent
    - require:
      - pkg: xbterminal-package
      - service: xbterminal-service
