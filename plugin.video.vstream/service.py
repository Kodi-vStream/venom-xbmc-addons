# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import subprocess
import xbmcvfs
from datetime import datetime
from resources.lib.comaddon import addon, xbmc, VSlog, VSPath, isMatrix
from resources.lib.util import Unquote, Quote, urlEncode

import requests
import sys

if isMatrix():
    from http.server import BaseHTTPRequestHandler
    from socketserver import TCPServer
    from urllib.parse import parse_qs, urlparse, parse_qsl
else:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from SocketServer import TCPServer
    from urlparse import urlparse, parse_qs,parse_qsl


def service():
    ADDON = addon()
    recordIsActivate = ADDON.getSetting('enregistrement_activer')
    if recordIsActivate == 'false':
        return

    pathRecording = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement'
    path = ''.join([pathRecording])
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdir(path)

    recordList = xbmcvfs.listdir(path)
    interval = ADDON.getSetting('heure_verification')
    ADDON.setSetting('path_enregistrement_programmation', path)
    recordInProgress = False
    monitor = xbmc.Monitor()

    del ADDON
    
    while not monitor.abortRequested() and not recordInProgress == True:
        if monitor.waitForAbort(int(interval)):
            break

        hour = datetime.now().strftime('%d-%H-%M') + '.py'
        if hour in str(recordList):
            hour = path + '/' + hour
            hour = VSPath(hour)
            recordInProgress = True
            VSlog('python ' + hour)
            command = 'python ' + hour
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            p_status = proc.wait()

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_GET(self):
        p = urlparse(self.path)
        q = dict(parse_qsl(p.query))
        url = q['u']
        
        if '?msKey=' in url: # Remove the PNG header
            res = requests.get(url).content[8:]
        else: # Redirect play list to proxy
            res = requests.get(url).content
            if isMatrix(): res = res.decode()
            res = res.replace('http','http://127.0.0.1:2424?u=http')
            if isMatrix(): res = res.encode()
        ret = res
        self.send_response_only(200)
        self.send_header('Content-Length', len(ret))
        self.send_header('Content-Type', 'application/vnd.apple.mpegurl')
        self.end_headers()
        self.wfile.write(ret)

if __name__ == '__main__':
    service()

    #Code by sviet2k
    if addon().getSetting('plugin_kepliz_com') == "true" or addon().getSetting('plugin_kaydo_ws') == "true":
        VSlog("Server Start")
        address = '127.0.0.1'  # Localhost
        port = 2424
        server_inst = TCPServer((address, port), ProxyHTTPRequestHandler)
        server_inst.serve_forever()
