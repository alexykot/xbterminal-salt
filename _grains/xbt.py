#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

CONFIGS = {
   'rpc_config': '/srv/xbterminal/xbterminal/runtime/rpc_config',
   'gui_config': '/srv/xbterminal/xbterminal/runtime/gui_config',
}


def _byteify(value):
    if isinstance(value, dict):
        return {_byteify(key): _byteify(value) for key, value in value.iteritems()}
    elif isinstance(value, list):
        return [_byteify(element) for element in value]
    elif isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value


def _xbt_get_batch_number():
    batch_number_path = '/srv/xbterminal/xbterminal/runtime/batch_number'
    with open(batch_number_path) as batch_number_file:
        batch_number = batch_number_file.read().strip()
    return batch_number


def xbt_get_config():
    grains = {}
    grains['xbt'] = {}
    for config_name, config_path in CONFIGS.items():
        with open(config_path) as config_file:
            config = json.loads(config_file.read())
        grains['xbt'][config_name] = _byteify(config)
    grains['xbt']['batch_number'] = _xbt_get_batch_number()
    return grains
