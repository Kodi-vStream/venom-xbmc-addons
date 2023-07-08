# -*- coding: utf-8 -*-
import json

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'tune', 'Tune')

    def __getIdFromUrl(self, sUrl):  # correction ancienne url >> embed depreciated
        sPattern = '(?:play/|video/|embed\?videoid=|vid=)([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0] is True:
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = ''
        url = []
        qua = []
        sId = self.__getIdFromUrl(self._url)

        sUrl = 'https://api.tune.pk/v3/videos/' + sId

        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('X-KEY', '777750fea4d3bd585bf47dc1873619fc')
        oRequest.addHeaderEntry('X-REQ-APP', 'web')  # pour les mp4
        oRequest.addHeaderEntry('Referer', self._url)  # au cas ou
        sHtmlContent1 = oRequest.request()

        if sHtmlContent1:
            sHtmlContent1 = cUtil().removeHtmlTags(sHtmlContent1)
            sHtmlContent = cUtil().unescape(sHtmlContent1)

            content = json.loads(sHtmlContent)

            content = content["data"]["videos"]["files"]

            if content:
                for x in content:
                    if 'Auto' in str(content[x]['label']):
                        continue
                    url2 = str(content[x]['file']).replace('index', str(content[x]['label']))

                    url.append(url2)
                    qua.append(repr(content[x]['label']))

                api_call = dialog().VSselectqual(qua,url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA

            return False, False
