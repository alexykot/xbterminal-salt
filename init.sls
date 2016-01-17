xbterminal-firmware:
  pkg:
    - installed
    - refresh: True
    - allow_updates: False
    - version: {{ pillar['xbt']['version'] }}
