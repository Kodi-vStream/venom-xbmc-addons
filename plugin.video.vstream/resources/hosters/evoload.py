#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://evoload.io/e/xxxxxx
# référence https://github.com/addon-lab/addon-lab_resolver_Project

import requests
import re
# from resources.lib.handler.requestHandler import cRequestHandler
# from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

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
        url = self.__sUrl
        key = "6Ldv2fYUAAAAALstHex35R1aDDYakYO85jt0ot-c"
        co = "aHR0cHM6Ly9ldm9sb2FkLmlvOjQ0Mw.."
        loc = "https://evoload.io"
        sUrlSecurePlayer = "https://evoload.io/SecurePlayer"

        code = url.split('/')[-1]

        headers1 = {'user-agent':UA,
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                    }

        headers2 = {'user-agent':UA,
                   'Accept':'Accept: application/json, text/plain, */*',
                   'Content-Type':'application/json;charset=utf-8',
                   'Referer':url
                    }

        s = requests.session()
        s.get(url, headers=headers1)

        bvalid, token = get_token(key, co, loc)
        if bvalid:
            post = '{"code":"' + code + '","token":"' + token + '"}'
            req = s.post(sUrlSecurePlayer, data=post, headers=headers2)
            response = str(req.content)
            sPattern = 'stream.+?src.+?"(https.+?)"'
            aResult = re.findall(sPattern, response)
            if aResult:
                api_call = aResult[0]

        if (api_call):
            return True, api_call

        return False, False


def get_token(site_key, co, loc):

    sa = ''
    cb = '123456789'
    headers1 = {'user-agent':UA,
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Content-Type':'application/x-www-form-urlencoded;charset=utf-8',
               'Referer':loc
                }

    url1 = 'https://www.google.com/recaptcha/api.js'
    s = requests.session()
    req = s.get(url1, headers=headers1)
    data = req.text

    aresult = re.findall("releases\/(.*?)\/", data)
    if aresult:
        v = aresult[0]
    else:
        return False, False

    url2 = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=" + site_key + "&co=" + co + "&hl=ro&v=" + v + "&size=invisible&cb=" + cb

    req = s.get(url2)
    data = req.text
    data = data.replace('\x22', '')

    aresult = re.findall("recaptcha-token.*?=(.*?)>", data)
    if aresult:
        c = aresult[0]
    else:
        return False, False

    url3 = "https://www.google.com/recaptcha/api2/reload?k=" + site_key

    post_data = {'v':v,
       'reason':'q',
       'k':site_key,
       'c':c,
       'sa':sa,
       'co':co}

    headers2 = {'user-agent':UA,
               'Accept':'*/*',
               'Content-Type':'application/x-www-form-urlencoded;charset=utf-8',
               'Referer':url2
                }

    req_url3 = s.post(url3, data=post_data, headers=headers2)
    data = req_url3.text
    aresult = re.findall("resp\",\"(.*?)\"", data)
    if aresult:
        token  = aresult[0]
        return True, token
    return False, False
