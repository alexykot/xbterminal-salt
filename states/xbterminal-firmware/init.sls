{% from "xbterminal-firmware/map.jinja" import xbt with context %}

xbt/terminal/highstate:
  event.send:
    - data:
        pillar: {{ xbt }}

xbterminal-rpc:
  pkg:
    - installed
    - refresh: True
    - allow_updates: False
    - version:  '{{ xbt.rpc_version }}'
    - hold: True
  service:
    - running
    - enable: True
    - provider: systemd
    - watch:
      - file: rpc_config

xbterminal-gui:
  pkg:
    - installed
    - refresh: True
    - allow_updates: False
    - version:  '{{ xbt.gui_version }}'
    - hold: True
  service:
    - running
    - enable: True
    - provider: systemd
    - watch:
      - file: gui_config

{% if 'themes' in xbt %}
xbterminal-gui-themes:
  pkg:
    - installed
    - hold: True
    - require_in:
      - pkg: updated-system
    - pkgs:
    {%- for theme, version in xbt.themes.iteritems() %}
      - xbterminal-gui-theme-{{ theme }}: '{{ version }}'
    {%- endfor %}
{% endif %}

rpc_config:
  file:
    - managed
    - name:  /srv/xbterminal/xbterminal/runtime/rpc_config
    - source: salt://xbterminal-firmware/files/local_config
    - template: jinja
    - context:
      local_config: {{ grains['xbt']['rpc_config'] }}
      ext_config: {{ xbt.rpc_config }}

gui_config:
  file:
    - managed
    - name:  /srv/xbterminal/xbterminal/runtime/gui_config
    - source: salt://xbterminal-firmware/files/local_config
    - template: jinja
    - context:
      local_config: {{ grains['xbt']['gui_config'] }}
      ext_config: {{ xbt.gui_config }}

updated-system:
  pkg:
    - uptodate
    - refresh: True
    - require:
      - pkg: xbterminal-rpc
      - pkg: xbterminal-gui
      - file: rpc_config
      - file: gui_config
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
