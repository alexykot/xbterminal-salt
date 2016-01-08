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
    return result['jid']


def run():
    '''
    Run the reactor
    '''
    if data['fun'] == 'state.highstate':
        _save_jid_to_pillar(data['id'], data['jid'])
        log.debug('saved {jid} for {mid} '.format(jid=data['jid'], mid=data['id']))
    elif data['fun'] == 'state.sls' and 'xbterminal-firmware.check' in data['fun_args']:
        hjid = _get_hjid(data['id'])
        cjid = data['jid']
        log.debug('check jid {cjid} called by  highstate {hjid} for minion {mid} '.format(cjid=cjid, hjid=hjid,
                                                                                         mid=data['id']))
        from salt.utils.http import query as httpclient

        url = '{host}/api/v2/devices/{device_key}/confirm_activation'.format(host='http://stage.xbterminal.com',
                                                                             device_key=data['id'])
        payload = {"highstate_jid": hjid, "checkstate_jid": cjid, "data": data}
        result = httpclient(url=url, method='POST', data=json.dumps(payload),
                            headers=['content-type: application/json'])

        log.debug('check state status confirmation for {mid} sended, got result: {result}'.format(result=result,
                                                                                                 mid=data['id']))
    else:
        pass
    return {}
