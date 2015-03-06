#!/usr/bin/python
import httplib
import json

class StaticFlowPusher(object):

    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowentrypusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret

pusher = StaticFlowPusher('10.123.123.1')

to_h2_rdirc_h3 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"flow-to-server01",
    "priority":"32768",
    "ether-type":"0x0800",
    "protocol":"0x06",
    "ingress-port":"1",
    "dst-ip":"10.0.0.2",
    "active":"true",
    "actions":"output=NORMAL,set-dst-mac=00:00:00:00:00:03,set-dst-ip=10.0.0.3,output=NORMAL"
    }


pusher.set(to_h2_rdirc_h3)
