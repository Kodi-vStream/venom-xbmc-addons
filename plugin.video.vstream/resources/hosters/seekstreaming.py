# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# SeekStreaming / Embed4me family player (p2pstream, ezplayer, embed4me,
# embedseek, seekplayer, seekplays, uns.bio ...). Used by 1jour1film.
#
# Flow: embed URL carries the video id in the #fragment
#   https://marcus.p2pstream.vip/#hdxxgm  ->  id = hdxxgm
# The API returns an AES-CBC (static key/iv) hex blob:
#   GET https://{domain}/api/v1/video?id={id}&w=1920&h=1080&r=
# Decrypted JSON exposes two HLS playlists:
#   source   -> raw-IP origin (geo/IP locked, cert won't match -> verifypeer=false)
#   cfNative -> CDN route via the embed domain (.m3u8, proper cert) = "normale"
#   cf       -> CDN .txt playlist (fallback for "normale")
from urllib.parse import urlparse

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import dialog, VSlog

import binascii
import json

from Cryptodome.Cipher import AES

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Static AES-CBC key/iv baked into the seekstreaming player bundle.
AES_KEY = b'kiemtienmua911ca'
AES_IV = b'1234567890oiuytr'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'seekstreaming', 'SeekStreaming')

    def setUrl(self, url):
        # Keep the #fragment (it carries the video id) - iHoster.setUrl drops nothing,
        # but the generic http-prefixer is fine here.
        super(cHoster, self).setUrl(url)

    def _decrypt(self, hexStr):
        try:
            data = binascii.unhexlify(hexStr.strip().replace('"', ''))
            dec = AES.new(AES_KEY, AES.MODE_CBC, AES_IV).decrypt(data)
            dec = dec[:-dec[-1]]  # strip PKCS7 padding
            return dec.decode('utf-8', 'replace')
        except Exception as e:
            VSlog('[SEEKSTREAMING] decrypt error: %s' % str(e))
            return None

    def _getMediaLinkForGuest(self):
        sUrl = self._url

        # video id: after #fragment, else /embed/<id>, else last path segment
        videoId = ''
        if '#' in sUrl:
            videoId = sUrl.split('#')[-1].strip()
        else:
            parsed = urlparse(sUrl)
            if parsed.fragment:
                videoId = parsed.fragment.strip()
            elif '/embed/' in sUrl.lower():
                videoId = sUrl.rstrip('/').split('/')[-1].strip()
            elif parsed.path and parsed.path != '/':
                videoId = parsed.path.rstrip('/').split('/')[-1].strip()
        if not videoId:
            return False, False

        domain = urlparse(sUrl).netloc
        if not domain:
            return False, False

        apiUrl = 'https://%s/api/v1/video?id=%s&w=1920&h=1080&r=' % (domain, videoId)
        oRequest = cRequestHandler(apiUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', '*/*')
        oRequest.addHeaderEntry('Referer', 'https://%s/' % domain)
        oRequest.addHeaderEntry('Origin', 'https://%s' % domain)
        sContent = oRequest.request(jsonDecode=False)
        if not sContent:
            return False, False

        raw = self._decrypt(sContent)
        if not raw:
            return False, False
        try:
            data = json.loads(raw)
        except ValueError:
            return False, False

        # "normale" (CDN) preferred as cfNative (.m3u8, proper cert), else cf (.txt)
        normale = data.get('cfNative') or data.get('cf')
        ipStream = data.get('source')

        # Headers carried to Kodi's player; verifypeer=false covers the raw-IP cert.
        suffix = '|User-Agent=%s&Referer=https://%s/&Origin=https://%s&verifypeer=false' % (UA, domain, domain)

        quals = []
        urls = []
        if normale:
            quals.append('Normale (CDN)')
            urls.append(normale + suffix)
        if ipStream:
            quals.append('IP direct')
            urls.append(ipStream + suffix)

        if not urls:
            return False, False

        api_call = dialog().VSselectqual(quals, urls)
        if api_call:
            return True, api_call

        return False, False
