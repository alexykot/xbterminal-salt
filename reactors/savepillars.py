#!py

import logging
# requires mongodb 3.0+

log = logging.getLogger('reactor.event_handler')


def _save_pillar(mid, data):
    import pymongo

    conn = pymongo.MongoClient()
    mdb = conn[__opts__['mongo.db']]
    mdb.xbt_pillars.update({"_id": mid}, {"$set": {"_id": mid, "xbt": data}}, upsert=True)
    conn.close()
    return True


def run():
    '''
    Run the reactor
    '''
    pillars = data['data']['pillar']
    mid = data['id']
    _save_pillar(mid, pillars)
    log.debug('saved {pillar} for {mid} '.format(pillar=data['data']['pillar'], mid=data['id']))
    return {}
