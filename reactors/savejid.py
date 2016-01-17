#!py


import json
import logging
# requires mongodb 3.0+

log = logging.getLogger('reactor.event_handler')

# data and __opts_ provided by salt



def _save_jid_to_pillar(mid, jid):
    """
    :param mid:
    :param jid:
    :return: True
    """
    import pymongo

    conn = pymongo.MongoClient()
    mdb = conn[__opts__['mongo.db']]
    mdb.xbt_pillars.update({"_id": mid}, {"$set": {"_id": mid, "jid": jid}}, upsert=True)
    conn.close()
    return True


def _get_hjid(mid):
    import pymongo
    conn = pymongo.MongoClient()
    mdb = conn[__opts__['mongo.db']]
    result = mdb.xbt_pillars.find_one({"_id": mid})
    conn.close()
    if result == None or 'jid' not in result:
        return {}
    else:
        return result['jid']

def _get_pillars(mid):
    import pymongo
    conn = pymongo.MongoClient()
    mdb = conn[__opts__['mongo.db']]
    result = mdb.xbt_pillars.find_one({"_id": mid})
    conn.close()
    if result == None or 'xbt' not in result:
        return {}
    else:
        return result['xbt']

def run():
    '''
    Run the reactor
    '''
    mid = data['id']
    cjid = data['jid']
    if data['fun'] == 'state.highstate':
        _save_jid_to_pillar(data['id'], data['jid'])
        log.debug('saved {jid} for {mid} '.format(jid=data['jid'], mid=mid))
    elif data['fun'] == 'state.sls' and 'xbterminal-firmware.check' in data['fun_args']:
        hjid = _get_hjid(mid)
        pillars = _get_pillars(mid)
        log.debug('check jid {cjid} called by  highstate {hjid} for minion {mid} '.format(cjid=cjid, hjid=hjid,
                                                                                         mid=mid))
        from salt.utils.http import query as httpclient

        try:
            env = pillars['env']
        except KeyError:
            log.error('cannot retrieve env for {mid}: {e}'.format(mid=mid))
            return {}


        if pillars['env'] in ['None', 'base', 'prod']:
            xbtapihost ='https://xbterminal.io'
        elif pillars['env'] in [ 'dev', 'stage']:
            xbtapihost = 'http://stage.xbterminal.com'

        url = '{host}/api/v2/devices/{device_key}/confirm_activation/'.format(host=xbtapihost,
                                                                             device_key=mid)
        payload = {"highstate_jid": hjid, "checkstate_jid": cjid, "data": data}
        result = httpclient(url=url, method='POST', data=json.dumps(payload),
                            headers=['content-type: application/json'])

        log.debug('check state status confirmation for {mid} sended, got result: {result}'.format(result=result,
                                                                                                 mid=mid))
    else:
        pass
    return {}
