#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os


def _xbt_get_config_file_path():
    config_file_path = '/srv/xbterminal/xbterminal/runtime/local_config'
    return config_file_path

def _byteify(input):
    if isinstance(input, dict):
        return {_byteify(key):_byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [_byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def xbt_get_config():
    grains = {}
    grains['xbt'] = {}
    config_file_path=_xbt_get_config_file_path()
    with open(config_file_path) as local_config_file:
        local_config = json.loads(local_config_file.read())
    grains['xbt']['config']=_byteify(local_config)
    return grains
