# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import json
import binascii
import requests
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'veev', 'Veev')

    def _getMediaLinkForGuest(self):
        sUrl = self._url
        sReferer = ''
        
        if '|Referer=' in sUrl:
            sUrl, sReferer = sUrl.split('|Referer=')

        match = re.search(r'/(?:v|embed|e|d)/([0-9a-zA-Z]+)', sUrl)
        if not match:
            return False, False

        media_id = match.group(1)
        
        parsed_url = re.match(r'(https?://[^/]+)', sUrl)
        base_url = parsed_url.group(1) if parsed_url else 'https://veev.to'
        if not sReferer:
            sReferer = base_url + '/'

        headers = {
            'User-Agent': UA,
            'Referer': sReferer,
            'Origin': base_url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

        try:
            response = requests.get(sUrl, headers=headers, verify=False, timeout=15)
            web_url = response.url
            page_content = response.text

            if response.history:
                match_redir = re.search(r'/(?:v|embed|e|d)/([0-9a-zA-Z]+)', web_url)
                if match_redir:
                    media_id = match_redir.group(1)

            items = re.findall(r'''[\.\s'](?:fc|_vvto\[[^\]]*)(?:['\]]*)?\s*[:=]\s*['"]([^'"]+)''', page_content)
            if not items:
                return False, False

            for f in items[::-1]:
                ch = veev_decode(f)
                if ch != f:
                    params = {
                        'op': 'player_api',
                        'cmd': 'gi',
                        'file_code': media_id,
                        'ch': ch,
                        'ie': 1
                    }
                    
                    api_url = base_url + '/dl'
                    api_resp = requests.get(api_url, params=params, headers=headers, verify=False, timeout=15)
                    
                    try:
                        jdata = api_resp.json()
                        file_dict = jdata.get('file', {})
                        
                        if file_dict.get('file_status') == 'OK':
                            dv_list = file_dict.get('dv', [])
                            if dv_list:
                                encoded_s = dv_list[0].get('s')
                                decoded_s = veev_decode(encoded_s)
                                tarray = build_array(ch)[0]
                                str_url = decode_url(decoded_s, tarray)
                                
                                final_link = str_url + '|User-Agent=' + UA + '&Referer=' + base_url + '/'
                                return True, final_link
                    except Exception:
                        pass

            return False, False

        except Exception:
            return False, False


def veev_decode(etext):
    result = []
    lut = {}
    n = 256
    if not etext:
        return ''
    c = etext[0]
    result.append(c)
    for char in etext[1:]:
        code = ord(char)
        nc = char if code < 256 else lut.get(code, c + c[0])
        result.append(nc)
        lut[n] = c + nc[0]
        n += 1
        c = nc
    return ''.join(result)

def js_int(x):
    return int(x) if str(x).isdigit() else 0

def build_array(encoded_string):
    d = []
    c = list(encoded_string)
    if not c:
        return d
    count = js_int(c.pop(0))
    while count:
        current_array = []
        for _ in range(count):
            if c:
                current_array.insert(0, js_int(c.pop(0)))
        d.append(current_array)
        if c:
            count = js_int(c.pop(0))
        else:
            break
    return d

def decode_url(etext, tarray):
    ds = etext
    for t in tarray:
        if t == 1:
            ds = ds[::-1]
        try:
            ds = binascii.unhexlify(ds).decode('utf8')
        except Exception:
            pass
        ds = ds.replace('dXRmOA==', '')
    return ds