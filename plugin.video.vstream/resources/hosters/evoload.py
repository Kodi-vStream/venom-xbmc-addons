#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://evoload.io/e/xxxxxx

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import requests
import re
import string
import random

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Evoload'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'evoload'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''
        sUrlSecurePlayer = "https://evoload.io/SecurePlayer"

        code = self.__sUrl.split('/')[-1]

        headers = {'User-Agent': UA,
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://evoload.io',
            'Referer': 'https://evoload.io/'}

        headers1 = {'user-agent':UA,
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                    }

        headers2 = {'user-agent':UA,
                   'Accept':'Accept: application/json, text/plain, */*',
                   'Content-Type':'application/json;charset=utf-8',
                   'Referer':self.__sUrl
                    }

        s = requests.session()
        
        crsv = requests.get('https://csrv.evosrv.com/captcha?m412548', headers=headers).text

        html = s.get(self.__sUrl, headers=headers1).text
        passe = re.search('<div id="captcha_pass" value="(.+?)"></div>',html).group(1)

        post = '{"code":"' + code + '","csrv_token":"'+crsv+'","pass":"' + passe + '","token":"ok"}'

        req = s.post(sUrlSecurePlayer, data=post, headers=headers2)
        response = str(req.content)

        sPattern = 'stream.+?src.+?"(https.+?)"'
        aResult = re.findall(sPattern, response)
        if aResult:
            api_call = aResult[0]

        if (api_call):
            return True, api_call + '|User-Agent=' + UA

        return False, False
