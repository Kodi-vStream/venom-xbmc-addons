# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

import re
import requests
import xbmcgui

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'googlevideo', 'GoogleVideo')


    def get_host_and_id(self, url):
        sPattern = 'http[s]*:\/\/(.*?(?:\.googlevideo|picasaweb\.google)\.com)' + \
            '\/(.*?(?:videoplayback\?|\?authkey|#|\/).+)'
        r = re.search(sPattern, url)
        if r:
            return r.groups()
        else:
            return False

    def getFormatedUrl(self, host, media_id):
        return 'https://%s/%s' % (host, media_id)

    def _getMediaLinkForGuest(self):
        r = self.get_host_and_id(self._url)

        # si lien deja decode
        if r is False:
            if '//lh3.googleusercontent.com' in self._url:
                # Nouveaute, avec cookie now

                VSlog(self._url)

                h = {'User-Agent': UA}
                r = requests.get(self._url, headers=h, allow_redirects=False)
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
                # HttpReponse = opener.open(self._url)
                # htmlcontent = HttpReponse.read()
                # head = HttpReponse.headers

                return True, url
            # Peut etre un peu brutal, peut provoquer des bugs
            if 'lh3.googleusercontent.com' in self._url:
                VSlog('Attention: lien sans cookies')
                return True, self._url

        web_url = self.getFormatedUrl(r[0], r[1])

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
                    html = re.search('\["shared_group_' + re.escape(vid_id) + '"\](.+?),"ccOverride":"false"}',
                        resp, re.DOTALL)
                else:
                    # Methode brute en test
                    html = re.search('(?:,|\[)"shared_group_[0-9]+"\](.+?),"ccOverride":"false"}', resp, re.DOTALL)

                if html:
                    vid_list = []
                    url_list = []
                    best = 0
                    quality = 0

                    videos = re.compile(',{"url":"(https:\/\/redirector\.googlevideo\.com\/[^<>"]+?)",' + \
                        '"height":([0-9]+?),"width":([0-9]+?),"type":"video\/.+?"}').findall(html.group(1))
                    if not videos:
                        videos = re.compile(',{"url":"(https:\/\/lh3\.googleusercontent\.com\/[^<>"]+?)",' + \
                            '"height":([0-9]+?),"width":([0-9]+?),"type":"video\/.+?"}').findall(html.group(1))

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
                                return False, False

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
