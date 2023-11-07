#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import urllib

try: # Python 2
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import urlEncode
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import xbmc


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'exashare', 'Exashare')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()

        #methode1
        #lien indirect
        if 'You have requested the file:' in sHtmlContent:
            POST_Url               = re.findall('form method="POST" action=\'([^<>"]*)\'',sHtmlContent)[0]
            POST_Selected          = re.findall('form method="POST" action=(.*)</Form>',sHtmlContent,re.DOTALL)[0]
            POST_Data              = {}
            POST_Data['op']        = re.findall('input type="hidden" name="op" value="([^<>"]*)"',POST_Selected)[0]
            #POST_Data['usr_login'] = re.findall('input type="hidden" name="usr_login" value="([^<>"]*)"',
            #                           POST_Selected)[0]
            POST_Data['id']        = re.findall('input type="hidden" name="id" value="([^<>"]*)"',POST_Selected)[0]
            POST_Data['fname']     = re.findall('input type="hidden" name="fname" value="([^<>"]*)"',POST_Selected)[0]
            #POST_Data['referer']   = re.findall('input type="hidden" name="referer" value="([^<>"]*)"',
            #                           POST_Selected)[0]
            POST_Data['hash']      = re.findall('input type="hidden" name="hash" value="([^<>"]*)"',POST_Selected)[0]
            POST_Data['imhuman']   = 'Proceed to video'

            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            headers = {'User-Agent': UA ,
                       'Host' : 'www.exashare.com',
                       'Referer' : self._url ,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Content-Type': 'application/x-www-form-urlencoded'}

            postdata = urlEncode(POST_Data)

            req = urllib2.Request(POST_Url,postdata,headers)

            xbmc.sleep(10*1000)

            response = urllib2.urlopen(req)
            sHtmlContent = response.read()
            response.close()

            #fh = open('c:\\test.txt', "w")
            #fh.write(sHtmlContent)
            #fh.close()

        sPattern = 'file: "([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]

        #methode2
        sPattern = '<iframe[^<>]+?src="(.+?)"[^<>]+?><\/iframe>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            url = aResult[1][0]
            oRequest = cRequestHandler(url)
            oRequest.addHeaderEntry('Referer',url)
            #oRequest.addHeaderEntry('Host','dowed.info')
            sHtmlContent = oRequest.request()

            sPattern = 'file: *"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                api_call = aResult[1][0]

            #methode2-3
            sPattern = '<iframe.+?src="([^"]+)".+?<\/iframe>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                vurl = aResult[1][0]
                oRequest = cRequestHandler(vurl)
                sHtmlContent = oRequest.request()
                sPattern = 'file: *"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
