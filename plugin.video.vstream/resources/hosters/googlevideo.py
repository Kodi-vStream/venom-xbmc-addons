# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

import re
import xbmcgui

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'GoogleVideo'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def get_host_and_id(self, url):
        sPattern = 'http[s]*:\/\/(.*?(?:\.googlevideo|picasaweb\.google)\.com)\/(.*?(?:videoplayback\?|\?authkey|#|\/).+)'
        r = re.search(sPattern, url)
        if r:
            return r.groups()
        else:
            return False

    def __modifyUrl(self, sUrl):
        return

    def getPluginIdentifier(self):
        return 'googlevideo'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def checkUrl(self, sUrl):
        return True

    def getUrl(self, host, media_id):
        return 'https://%s/%s' % (host, media_id)

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        r = self.get_host_and_id(self.__sUrl)

        # si lien deja decode
        if (r == False):
            if '//lh3.googleusercontent.com' in self.__sUrl:
                # Nouveaute, avec cookie now

                VSlog(self.__sUrl)

                import requests
                h = {'User-Agent': UA}
                r = requests.get(self.__sUrl, headers=h, allow_redirects=False)
                url = r.headers['Location']
                # VSlog(url)

                url = url + '|User-Agent=' + UA

                if 'set-cookie' in r.headers:
                    cookies = r.headers['set-cookie']
                    url = url + '&Cookie=' + cookies
                    # VSlog(cookies)

                # Impossible a faire fonctionner, si quelqu'un y arrive .....
                # class NoRedirect(urllib2.HTTPRedirectHandler):
                    # def redirect_request(self, req, fp, code, msg, hdrs, newurl):
                        # return newurl
                # opener = urllib2.build_opener(NoRedirect)
                # HttpReponse = opener.open(self.__sUrl)
                # htmlcontent = HttpReponse.read()
                # head = HttpReponse.headers

                return True, url
            # Peut etre un peu brutal, peut provoquer des bugs
            if 'lh3.googleusercontent.com' in self.__sUrl:
                VSlog('Attention: lien sans cookies')
                return True, self.__sUrl

        web_url = self.getUrl(r[0], r[1])

        headers = {'Referer': web_url}

        stream_url = ''
        vid_sel = web_url

        try:
            if 'picasaweb.' in r[0]:

                request = urllib2.Request(web_url, None, headers)

                try:
                    reponse = urllib2.urlopen(request)
                except UrlError as e:
                    print(e.read())
                    print(e.reason)

                resp = reponse.read()

                # fh = open('c:\\test.txt', "w")
                # fh.write(resp)
                # fh.close()

                vid_sel = ''
                vid_id = re.search('.*?#(.+?)$', web_url)

                if vid_id:
                    vid_id = vid_id.group(1)
                    html = re.search('\["shared_group_' + re.escape(vid_id) + '"\](.+?),"ccOverride":"false"}', resp, re.DOTALL)
                else:
                    # Methode brute en test
                    html = re.search('(?:,|\[)"shared_group_[0-9]+"\](.+?),"ccOverride":"false"}', resp, re.DOTALL)

                if html:
                    vid_list = []
                    url_list = []
                    best = 0
                    quality = 0

                    videos = re.compile(',{"url":"(https:\/\/redirector\.googlevideo\.com\/[^<>"]+?)","height":([0-9]+?),"width":([0-9]+?),"type":"video\/.+?"}').findall(html.group(1))
                    if not videos:
                        videos = re.compile(',{"url":"(https:\/\/lh3\.googleusercontent\.com\/[^<>"]+?)","height":([0-9]+?),"width":([0-9]+?),"type":"video\/.+?"}').findall(html.group(1))

                    if videos:
                        if len(videos) > 1:
                            for index, video in enumerate(videos):
                                if int(video[1]) > quality:
                                    best = index
                                quality = int(video[2])
                                vid_list.extend(['GoogleVideo - %sp' % quality])
                                url_list.extend([video[0]])
                        if len(videos) == 1:
                            vid_sel = videos[0][0]
                        else:
                            result = xbmcgui.Dialog().select('Choose a link', vid_list)
                            if result != -1:
                                vid_sel = url_list[result]
                            else:
                                return self.unresolvable(0, 'No link selected')

            if vid_sel:
                if 'googleusercontent' in vid_sel:
                    stream_url = urllib2.urlopen(vid_sel).geturl()
                elif 'redirector.' in vid_sel:
                    stream_url = urllib2.urlopen(vid_sel).geturl()
                elif 'google' in vid_sel:
                    stream_url = vid_sel

        except UrlError:
            stream_url = ''

        api_call = stream_url

        if api_call:
            return True, api_call

        return False, False
