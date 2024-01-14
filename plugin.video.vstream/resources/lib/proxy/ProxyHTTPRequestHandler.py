# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import base64
import requests

from resources.lib.comaddon import isMatrix

if isMatrix():
    from http.server import BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qsl
else:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from urlparse import urlparse, parse_qsl


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'
    headers = None

    def parseUrl(self):
        if "@" in self.path:
            url, h = self.path.split('@')
            ProxyHTTPRequestHandler.headers = dict(parse_qsl(h))
        else:
            url = self.path

        p = urlparse(url)
        q = dict(parse_qsl(p.query))
        url = q['u']
        return url

    def do_HEAD(self):
        self.send_response_only(200)

    def do_GET(self):
        url = self.parseUrl()

        res = requests.get(url, headers=ProxyHTTPRequestHandler.headers)

        if '?msKey=' in url:
            ret = res.content[8:]
        else:
            if isMatrix():
                res = res.content.decode()
            res = res.replace('http', 'http://127.0.0.1:2424?u=http')

            if res.endswith("=="):
                ret = base64.b64decode(res)
            else:
                if isMatrix():
                    ret = res.encode()

        self.send_response_only(200)
        self.send_header('Content-Length', len(ret))
        self.send_header('Content-Type', 'application/vnd.apple.mpegurl')
        self.end_headers()
        self.wfile.write(ret)
