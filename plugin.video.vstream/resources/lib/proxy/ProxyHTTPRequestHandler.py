# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import isMatrix, VSlog

if isMatrix():
    from http.server import BaseHTTPRequestHandler
    from socketserver import TCPServer
    from urllib.parse import parse_qs, urlparse, parse_qsl
else:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from SocketServer import TCPServer
    from urlparse import urlparse, parse_qs,parse_qsl

import requests

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'
    headers = None

    def do_GET(self):
        if "@" in self.path:
            url, h = self.path.split('@')
            VSlog(h)
            ProxyHTTPRequestHandler.headers = dict(parse_qsl(h))
        else:
            url = self.path

        p = urlparse(url)
        q = dict(parse_qsl(p.query))
        url = q['u']

        res = requests.get(url,headers=ProxyHTTPRequestHandler.headers)

        if '?msKey=' in url:
            ret = res.content[8:]
        else:
            if isMatrix(): res = res.content.decode()
            res = res.replace('http','http://127.0.0.1:2424?u=http')
            if isMatrix(): ret = res.encode()

        self.send_response_only(200)
        self.send_header('Content-Length', len(ret))
        self.send_header('Content-Type', 'application/vnd.apple.mpegurl')
        self.send_header('Referer', 'https://lb.toonanime.xyz')
        self.end_headers()
        self.wfile.write(ret)