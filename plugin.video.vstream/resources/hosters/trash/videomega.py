import xbmc
import re

try: # Python 2
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'videomega', 'VideoMega')

    def _getMediaLinkForGuest(self):
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
        headers = {'Host' : 'videomega.tv',
                   'User-Agent' : UA,
                   #'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                   #'Accept-Encoding' : 'gzip, deflate',
                   'Referer' : self._url
                   }

        request = urllib2.Request(self._url, None, headers)

        #print(url)

        try:
            reponse = urllib2.urlopen(request)
        except URLError as e:
            print(e.read())
            print(e.reason)

        sHtmlContent = reponse.read()

        api_call = False

        #si on passe pr le hash code
        if 'validatehash.php?hashkey=' in self._url:
            if 'ref=' in sHtmlContent:
                a = re.compile('.*?ref="(.+?)".*').findall(sHtmlContent)[0]
                url = 'http://videomega.tv/cdn.php?ref=' + a

                request = urllib2.Request(url, None, headers)

                try:
                    reponse = urllib2.urlopen(request)
                except URLError as e:
                    print(e.read())
                    print(e.reason)

                sHtmlContent = reponse.read()

        oParser = cParser()

        #Premier test, lien code unescape
        sPattern =  'unescape.+?"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            decoder = cUtil().urlDecode(aResult[1][0])

            sPattern =  'file: "(.+?)"'
            aResult = oParser.parse(decoder, sPattern)

            if aResult[0] is True:
                print('code unescape')
                api_call = aResult[1][0]

        #Dexieme test Dean Edwards Packer
        if not api_call:
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                print('code Dean Edwards Packer')
                sUnpacked = cPacker().unpack(aResult[1][0])

                sPattern =  '\("src", *"([^\)"<>]+?)"\)'
                aResult = oParser.parse(sUnpacked, sPattern)

                if aResult[0] is True:
                    api_call = aResult[1][0]

        #Troisieme test, lien non code
        if not api_call:
            sPattern =  '<source src="([^"]+)" type="video[^"]*"\/>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                print('non code')
                api_call = aResult[1][0]

        #print('url : ' + api_call)

        if api_call:
            api_call = api_call + '|User-Agent=' + UA + '&Referer=' + self._url
            xbmc.sleep(6000)
            return True, api_call

        return False, False
