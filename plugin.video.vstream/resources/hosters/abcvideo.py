# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://abcvideo.cc/embed-xxxxx.html'
# https://abcvideo.cc/xxxxx.html'
# pour récuperer le token : https://github.com/addon-lab/addon-lab_resolver_Project adapté pour evoload
# mais meme principe

import re
import requests
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'abcvideo', 'Abcvideo')

    def _getMediaLinkForGuest(self):
        api_call = ''
        key = "6LcOeuUUAAAAANS5Gb3oKwWkBjOdMXxqbj_2cPCy"
        co = "aHR0cHM6Ly9hYmN2aWRlby5jYzo0NDM."
        loc = "https://abcvideo.cc"
        sUrlPlayer = "https://abcvideo.cc/dl"

        urlcode = self._url.replace('embed-', '')
        urlcode = urlcode.replace('.html', '')
        code = urlcode.split('/')[-1]

        headers1 = {'user-agent': UA,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                    }

        headers2 = {'user-agent': UA,
                    'Accept': '*/*',
                    'Content-Type': 'text/plain; charset=UTF-8',
                    'Referer': self._url
                    }

        s = requests.session()
        s.get(self._url, headers=headers1)

        bvalid, token = get_token(key, co, loc)
        if bvalid:
            url2 = sUrlPlayer + '?op=video_src&file_code=' + code + '&g-recaptcha-response=' + token
            req = s.get(url2, headers=headers2)
            response = str(req.content)

            sPattern = '"(https.+?)"'
            aResult = re.findall(sPattern, response)
            if aResult:
                api_call = aResult[0]  # fichier master valide pour la lecture
                req = s.get(api_call, headers=headers2)
                response = str(req.content)
                list_url = []
                list_q = []
                oParser = cParser()
                sPattern = 'PROGRAM.*?BANDWIDTH.*?RESOLUTION=(\d+x\d+).*?(https.*?m3u8)'
                aResult = oParser.parse(response, sPattern)
                if aResult[0] is True:
                    for aEntry in aResult[1]:
                        list_url.append(aEntry[1])
                        list_q.append(aEntry[0])
                    if list_url:
                        api_call = dialog().VSselectqual(list_q, list_url)

        if api_call:
            return True, api_call

        return False, False


def get_token(site_key, co, loc):

    sa = ''
    cb = '365ae0il5lwn'
    headers1 = {'user-agent': UA,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
                'Referer': loc
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
    url2 = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=" + site_key + "&co=" + co
    url2 += "&hl=ro&v=" + v + "&size=invisible&cb=" + cb

    req = s.get(url2)
    data = req.text
    data = data.replace('\x22', '')
    aresult = re.findall("recaptcha-token.*?=(.*?)>", data)

    if aresult:
        c = aresult[0]
    else:
        return False, False

    url3 = "https://www.google.com/recaptcha/api2/reload?k=" + site_key

    post_data = {'v': v, 'reason': 'q', 'k': site_key, 'c': c, 'sa': sa, 'co': co}

    headers2 = {'user-agent': UA,
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
                'Referer': url2
                }

    req_url3 = s.post(url3, data=post_data, headers=headers2)
    data = req_url3.text
    aresult = re.findall("resp\",\"(.*?)\"", data)
    if aresult:
        token = aresult[0]
        return True, token

    return False, False
