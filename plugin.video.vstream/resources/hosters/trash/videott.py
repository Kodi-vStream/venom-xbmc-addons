#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

try: # Python 2
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

try:    import json
except: import simplejson as json

from resources.lib.handler.requestHandler import cRequestHandler
#from t0mm0.common.net import Net
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'videott', 'VideoTT')

    def __getIdFromUrl(self, sUrl):
        sPattern = 'http:..(?:www.)*video.tt\/e(?:mbed)*\/([^<]+)'
        aResult = re.findall(sPattern,sUrl)
        if (aResult):
            return aResult[0]

        return ''

    def _getMediaLinkForGuest(self):
        sId = self.__getIdFromUrl(self._url)

        json_url = 'http://www.video.tt/player_control/settings.php?v=%s' % sId

        vUrl = False

        try:

            reponse = urllib2.urlopen(json_url)

            data = json.loads(reponse.read().decode(reponse.info().getparam('charset') or 'utf-8'))

            vids = data['settings']['res']

            if vids:

                vUrlsCount = len(vids)

                if (vUrlsCount > 0):
                    if vUrlsCount == 1:
                        vUrl = vids[0][u'u'].decode('base-64')
                    else:
                        vid_list = []
                        url_list = []

                        for index in vids:
                            quality = index[u'l']
                            vid_list.extend(['Video TT - %sp' % quality])
                            url_list.extend([index[u'u']])

                        result = dialog().VSselectqual(vid_list, url_list)
                        if result:
                            vUrl = url_list[result].decode('base-64')

        except urllib2.URLError as e:
            print(e.read())
            print(e.reason)
        except Exception as e:
            print(e.read())
            print(e.reason)


        if (vUrl):
            api_call = vUrl
            return True, api_call

        return False, False
