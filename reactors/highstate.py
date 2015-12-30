#!py

import pprint
import os
import time
import salt.config as config
import json
import binascii
import pymongo
import logging
#requires mongodb 3.0+

log = logging.getLogger('reactor.event_handler')

__opts__ = {'mongo.db': 'salt',
            'mongo.host': '127.0.0.1',
            'mongo.password': '',
            'mongo.port': 27017,
            'mongo.user': ''}


def _save_pillar(id,data):
    host = __opts__['mongo.host']
    port = __opts__['mongo.port']
    log.info('connecting to {0}:{1} for mongo ext_pillar'.format(host, port))
    conn = pymongo.MongoClient(host, port)
    log.debug('using database \'{0}\''.format(__opts__['mongo.db']))
    mdb = conn[__opts__['mongo.db']]
    user = __opts__.get('mongo.user')
    password = __opts__.get('mongo.password')
    mdb.xbt_pillars.update({"_id": id},{ "$set": {"_id": id, "xbt": data }}, upsert=True )
    return True


def run():
      '''
      Run the reactor
      '''

      _save_pillar(data['id'], data['data']['pillar'])
      log.debug( 'saved {pillar} for {id} '.format(pillar=data['data']['pillar'], id=data['id'] ) )
      return {}
