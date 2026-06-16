#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from urllib.parse import urlencode

import json
import base64
import urllib

from Cryptodome.Cipher import AES as PyCryptoAES

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'

#Function from https://github.com/Gujal00/ResolveUR


def ft(e, o = False):
    t = e.replace('-', '+').replace('_', '/')
    if len(t) % 4 != 0:
        t += '=' * (-len(t) % 4)
    r = base64.b64decode(t)
    return r

def xn(e, v):
    if v:
        v = int(v)
        e = [e[v - 1], e[len(e) - v]]
    t = list(map(ft, e))
    return b''.join(t)

def fp(x, y, z):
    from binascii import hexlify
    from hashlib import sha256
    from os import urandom
    from time import time
    from random import uniform
    import base64

    v_id = hexlify(urandom(x)).decode()
    d_id = hexlify(urandom(x)).decode()
    ctime = int(time())
    t_data = {
        'viewer_id': v_id,
        'device_id': d_id,
        'confidence': round(uniform(y, z), 2),
        'iat': ctime,
        'exp': ctime + 600
    }
    t_bdata = str(base64.b64encode(json.dumps(t_data).encode())).rstrip('=')
    t_sig = str(base64.b64encode(sha256(t_bdata.encode()).digest())).rstrip('=')
    token = '{0}.{1}'.format(t_bdata, t_sig)
    t_data.update({'token': token})
    t_data.pop('iat')
    t_data.pop('exp')
    return {'fingerprint': t_data}

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filemoon', 'FileMoon')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        url2 = self._url.replace('/e/', '/api/videos/') + '/embed/playback'
        _json = fp(16, 0.6, 0.9)
        _data = json.dumps(_json)

        oRequest = cRequestHandler(url2)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Origin', self._url[:-1])
        oRequest.addHeaderEntry('Content-Type', 'application/json')
        oRequest.addParametersLine(_data)
        oRequest.setRequestType(1)
        sHtmlContent2 = oRequest.request()

        _json = json.loads(sHtmlContent2)['playback']
        
        iv = ft(_json['iv'], True)
        key = xn(_json['key_parts'],_json['version'])
        payload = ft(_json['payload'])

        tag = payload[-16:]
        ciphertext = payload[:-16]
        cipher = PyCryptoAES.new(key, PyCryptoAES.MODE_GCM, nonce=iv)
        pt = cipher.decrypt_and_verify(ciphertext, tag)
        ct = json.loads(pt.decode('latin-1'))

        #flemme de detailler
        for i in ct['sources']:
            api_call = i['url']
        
        if api_call:
            return True, api_call # + '|User-Agent=' + UA
  

        return False, False
