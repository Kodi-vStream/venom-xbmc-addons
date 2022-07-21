# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://evoload.io/e/xxxxxx

import re
import requests

from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'evoload', 'Evoload')

    def _getMediaLinkForGuest(self):
        api_call = ''
        sUrlSecurePlayer = "https://evoload.io/SecurePlayer"

        code = self._url.split('/')[-1]

        headers = {'User-Agent': UA,
                   'Accept': 'application/json, text/plain, */*',
                   'Origin': 'https://evoload.io',
                   'Referer': 'https://evoload.io/'
                   }

        headers1 = {'user-agent': UA,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                    }

        headers2 = {'user-agent': UA,
                    'Accept': 'Accept: application/json, text/plain, */*',
                    'Content-Type': 'application/json;charset=utf-8',
                    'Referer': self._url
                    }

        s = requests.session()

        crsv = requests.get('https://csrv.evosrv.com/captcha?m412548', headers=headers).text

        html = s.get(self._url, headers=headers1).text
        passe = re.search('<div id="captcha_pass" value="(.+?)"></div>', html).group(1)

        post = '{"code":"' + code + '","csrv_token":"'+crsv+'","pass":"' + passe + '","token":"ok"}'

        req = s.post(sUrlSecurePlayer, data=post, headers=headers2)
        response = str(req.content)

        sPattern = 'stream.+?src.+?"(https.+?)"'
        aResult = re.findall(sPattern, response)
        if aResult:
            api_call = aResult[0]

        if api_call:
            return True, api_call + '|User-Agent=' + UA

        return False, False
