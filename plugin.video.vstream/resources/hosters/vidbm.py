#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://www.vidbm.com/emb.html?xxx=img.vidbm.com/xxx
#https://www.vidbm.com/embed-xxx.html?auto=1
#https://www.vidbm.com/embed-xxx.html
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.aadecode import decodeAA
from resources.lib.packer import cPacker
#from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbm', 'VidBM')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = re.sub('=img.vidbm.com/.+?','',str(url))
        self._url = self._url.replace('https://www.vidbm.com/', '')
        self._url = self._url.replace('embed-', '')
        self._url = self._url.replace('emb.html?', '')
        self._url = self._url.replace('.html?auto=1','')
        self._url = self._url.replace('.html','')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'sources: *\[{file:"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        api_call = aResult[1][0] + '|User-Agent=' + UA

        if api_call:
            return True, api_call

        return False, False
