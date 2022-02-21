#-*- coding: utf8 -*-
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'youwatch', 'Youwatch')

    def __getIdFromUrl(self, url):
        sPattern = "http://youwatch.org/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(url, sPattern)
        if aResult[0] is True:
            return aResult[1][0]

        return ''

    def setUrl(self, url):
        if 'embed' not in url:
            self._url = str(self.__getIdFromUrl(url))
            self._url = 'http://youwatch.org/embed-'+str(self._url)+'.html'
            if not re.match('[0-9]+x[0-9]+.html',self._url,re.IGNORECASE):
                self._url =  self._url.replace('.html','-640x360.html')
        else:
            self._url = url

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()

        sPattern ='<iframe[^<>]+?src="(.+?)" [^<>]+?> *<\/iframe>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
            oRequestHandler = cRequestHandler(aResult[1][0])
            oRequestHandler.addHeaderEntry('User-Agent',UA)
            oRequestHandler.addHeaderEntry('Referer',aResult[1][0])
            sHtmlContent = oRequestHandler.request()


        sPattern ='\[{file:"(.+?)",label:"(.+?)"}\]'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            return True , aResult[1][0][0] + '|Referer=' + self._url

        return False, False
