# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import base64
import binascii
import json
import random
import string

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
MODE = 0


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'viewsb', 'Viewsb')

    def __getHost(self, url):
        parts = url.split('//', 1)
        host = parts[1].split('/', 1)[0]
        return 'https://{0}/'.format(host)

    def __getId(self, url):
        url = url.split('/')[-1]
        return url.split('.')[0]

    def _getMediaLinkForGuest(self):
        api_call = ''

        host = self.__getHost(self._url)
        videoId = self.__getId(self._url)
        url = host + 'd/' + videoId + '.html'

        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', host)
        sHtmlContent = oRequest.request()

        if MODE == 1:  # Non terminé encore
            sPattern = 'download_video([^"]+)[^\d]+\d+x(\d+)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                list_data = []
                list_q = []
                for aEntry in aResult[1]:
                    list_data.append(aEntry[0])
                    list_q.append(aEntry[1])
                if list_data:
                    data = dialog().VSselectqual(list_q, list_data)
                    code = list_data[0]
                    mode = list_data[1]
                    hash = list_data[2]
                    dl_url = host + 'dl?op=download_orig&id=' + code + '&mode=' + mode + '&hash=' + hash
                    VSlog(dl_url)

                    oRequest = cRequestHandler(dl_url)
                    sHtmlContent = oRequest.request()
                    domain = base64.b64encode((host[:-1] + ':443').encode('utf-8')).decode('utf-8').replace('=', '')
        else:
            eurl = get_embedurl(host, videoId)

            oRequest = cRequestHandler(eurl)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', host)
            oRequest.addHeaderEntry('watchsb', 'streamsb')
            sHtmlContent = oRequest.request()

            # fh = open('c:\\test.txt', "w")
            # fh.write(sHtmlContent)
            # fh.close

            page = json.loads(sHtmlContent)
            data = page['stream_data']
            if 'file' in data:
                api_call = data['file']
            elif 'backup' in data:
                api_call = data['backup']

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + host + '&Accept-Language=fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'

        return False, False


def get_embedurl(host, media_id):
    # Copyright (c) 2019 vb6rocod
    def makeid(length):
        t = string.ascii_letters + string.digits
        return ''.join([random.choice(t) for _ in range(length)])

    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), media_id, makeid(12))
    c1 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), makeid(12), makeid(12))
    c2 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), c2, makeid(12))
    c3 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    return '{0}sources43/{1}/{2}'.format(host, c1, c3)
