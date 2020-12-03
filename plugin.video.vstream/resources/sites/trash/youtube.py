# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import ssl
import re, sys, requests, random, json, string
import xbmcplugin, xbmcvfs, xbmc

return False

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import urlEncode, Unquote, Quote, QuotePlus
from resources.lib.player import cPlayer
from resources.lib.config import GestionCookie
from resources.lib.gui.hoster import cHosterGui
from resources.lib.jsunfuck import unFuckFirst

from resources.lib.enregistrement import cEnregistremement
from resources.lib.epg import cePg
from resources.lib.comaddon import progress, addon, VSlog, dialog


SITE_IDENTIFIER = 'youtube'
SITE_NAME = '[COLOR orange]Youtube[/COLOR]'
SITE_DESC = 'Youtube'

URL_MAIN = 'https://www.googleapis.com/youtube/v3/'
API_KEY = ''
URL_VIEW = 'https://youtube.com/watch?v=%s'

icon = 'tv.png'
# /home/lordvenom/.kodi/
# sRootArt = cConfig().getRootArt()

# https://developers.google.com/youtube/v3/guides/implementation/pagination

ADDON = addon()

class youtube:
    def __init__(self, ctype='videos', params=''):
        self.result = ''
        self.next = ''

        params = urlEncode(params)

        req = urllib2.Request(URL_MAIN + ctype + '?' + params)
        try:
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            response = urllib2.urlopen(req, context=gcontext)
        except:
            response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        sHtmlContent = sHtmlContent.decode('utf-8')
        self.result = json.loads(sHtmlContent)
        response.close()
        if self.result:
            self.load_result()
        return

    def load_result(self):
        if self.result.has_key('nextPageToken'):
            self.next = self.result.get('nextPageToken', [])

        videos, channels, playlists = [], [], []
        for search_result in self.result.get('items', []):
            if search_result['kind'] == 'youtube#video':
                videos.append({'title': search_result['snippet']['title'], 'id': search_result['id'], 'channelId': search_result['snippet']['channelId'], 'channelTitle': search_result['snippet']['channelTitle'], 'thumbnails': search_result['snippet']['thumbnails']['high']['url'], 'description': search_result['snippet']['description']})
            elif search_result['kind'] == 'youtube#channel':
                channels.append({'title': search_result['snippet']['title'], 'id': search_result['id']})
            elif search_result['kind'] == 'youtube#playlist':
                playlists.append({ 'title': search_result['snippet']['title'], 'id': search_result['id']})

        self.videos = videos
        self.channels = channels
        self.playlists = playlists
        return

    def getVideos(self):
        return self.videos

    def getNext(self):
        return self.next

    def getChannels(self):
        return self.channels

    def getPlaylists(self):
        return self.playlists

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30332), 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Catégorie', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('radio', 'showAZ', addons.VSlang(30203) + ' (A-Z)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('radio', 'showWeb', addons.VSlang(30203), 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('lsdb', 'load', 'Liveset Database', 'music.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():

    oGui = cGui()

    liste = []
    liste.append( ['1', 'Film & Animation'] )
    liste.append( ['2', 'Autos & Vehicles'] )
    liste.append( ['10', 'Music'])
    liste.append( ['15', 'Pets & Animals'])
    liste.append( ['17', 'Sports'])
    liste.append( ['18', 'Short Movies'])
    liste.append( ['19', 'Travel & Events'] )
    liste.append( ['20', 'Gaming'] )
    liste.append( ['21', 'Videoblogging'])
    liste.append( ['22', 'People & Blogs'])
    liste.append( ['23', 'Comedy'])
    liste.append( ['24', 'Entertainment'])
    liste.append( ['25', 'News & Politics'] )
    liste.append( ['26', 'Howto & Style'] )
    liste.append( ['27', 'Education'])
    liste.append( ['28', 'Science & Technology'])
    liste.append( ['29', 'Nonprofits & Activism'])
    liste.append( ['30', 'Movies'])
    liste.append( ['31', 'Anime/Animation'])
    liste.append( ['32', 'Action/Adventure'])
    liste.append( ['33', 'Classics'] )
    liste.append( ['34', 'Comedy'] )
    liste.append( ['35', 'Documentary'])
    liste.append( ['36', 'Drama'])
    liste.append( ['37', 'Family'])
    liste.append( ['38', 'Foreign'])
    liste.append( ['39', 'Horror'])
    liste.append( ['40', 'Sci-Fi/Fantasy'])
    liste.append( ['41', 'Thriller'] )
    liste.append( ['42', 'Shorts'] )
    liste.append( ['43', 'Shows'])
    liste.append( ['44', 'Trailers'])

    for sCatID, sTitle in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('videoCategoryId', sCatID)
        oGui.addDir(SITE_IDENTIFIER, 'showLinks', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sCatID = oInputParameterHandler.getValue('videoCategoryId')
    sNext = oInputParameterHandler.getValue('pageToken')

    params = {
                'part': 'snippet',
                'maxResults': 20,
                'key': API_KEY,
                'chart': 'mostPopular',
                'regionCode': 'FR',
                'videoCategoryId': sCatID
            }

    if sNext:
        params['pageToken'] = sNext

    ytb = youtube('videos', params)
    videos = ytb.getVideos()
    # channel = result.getChannels()

    if (videos):
        total = len(videos)

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in videos:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry['thumbnails']
            sID = aEntry['id']
            sTitle = aEntry['title'].encode('utf-8')
            sDesc = aEntry['description'].encode('utf-8')
            sUrl = URL_VIEW % sID

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sID', sID)

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'ytb.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        _next = ytb.getNext()
        if _next:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('videoCategoryId', sCatID)
            oOutputParameterHandler.addParameter('pageToken', _next)
            oGui.addNext(SITE_IDENTIFIER, 'showLinks', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):  # Affiche les page suivant si il y en a
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'myfree-tivi' in sUrl:
        sPattern = '<li class="page-item"><a class="page-link waves-effect" href="(.+?)" data-page=".+.?">.+?<div class="clearfix"></div></nav></div>'
    elif 'https://www.iptvsource.com/' in sUrl:
        sPattern = 'class="last" title=".+?">.+?</a><a href="(.+?)"><i class="td-icon-menu-right"></i>'
    else:
        sPattern = '<a class="next page-numbers" href="(.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        if 'myfree-tivi' in sUrl:
            return 'https://www.myfree-tivi.com' + aResult[1][0]
        else:
            return  aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)

    oGui.setEndOfDirectory()

def showAllPlaylist():  # On recupere les differentes playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')
    sDesc = oInputParameterHandler.getValue('sDescription')
    # VSlog(str(sUrl))
    if 'firstonetv' and 'Register-Login' in sUrl:

        session = requests.Session()
        url = 'https://www.firstonetv.net/Register-Login'
        data = {'usrmail': ADDON.getSetting('hoster_firstonetv_username'),
                'password': ADDON.getSetting('hoster_firstonetv_password'),
                'login': 'Login+Now'}

        headers = {'user-agent': UA,
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': 'https://www.firstonetv.net/Index',
                   'Content-Length': str(len(data))}

        session.post(url, data=data, headers=headers)
        cookiesDict = requests.utils.dict_from_cookiejar(session.cookies)
        getUser = re.match("{'(.+?)': '(.+?)',", str(cookiesDict))
        # VSlog(cookiesDict)
        cookies = str(getUser.group(1)) + '=' + str(getUser.group(2))
        GestionCookie().SaveCookie('firstonetv', cookies)
        dialog().VSinfo('Authentification réussie merci de recharger la page', 'FirstOneTv', 15)
        return

    sHtmlContent = getHtml(sUrl)

    if 'myfree-tivi' in sUrl:
        aResult = re.findall('<meta name="csrf-token" content="(.+?)">', sHtmlContent)
        if aResult:
            token = aResult[0]
            # VSlog(token)
            sHtmlContent = getHtml(sUrl,token)

    if 'firstonetv' in sUrl:
        sPattern = '(?:"surl":"{\".+?|,.+?)"([^"]+)\".+?"http([^"]+).m3u8'
    elif 'myfree-tivi' in sUrl:
        sPattern = 'url".+?"(.+?)".+?title.+?"(.+?)".+?thumb".+?"(.+?)"'
    elif 'iptvgratuit.com' in sUrl:
        sPattern = '<h4><a class="more-link" title="(.+?)" href="(.+?)" target="_blank" rel="noopener"><button>.+?</button></a></h4>'
    elif 'dailyiptvlist.com' in sUrl:
        sPattern = '<p></br><br /><strong>2. Click on link to download .+? iptv channels list</strong></p>\s*.+?<a href="(.+?)">Download (.+?)</a>'
    elif 'iptvsource.com':
        sPattern = '<a href="([^"]+)">Download as([^"]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'firstonetv' in sUrl:
                sTitle = sTitle + aEntry[0]
                sDesc = sDesc
                sThumb = sThumb
                sUrl2 = 'http' + aEntry[1].replace('\\\/', '/').replace('\/', '/') + '.m3u8|Referer=' + sUrl + '&User-Agent=' + UA + '&X-Requested-With=ShockwaveFlash/28.0.0.137&Origin=https://www.firstonetv.net'
            elif 'myfree-tivi' in sUrl:
                sTitle = str(aEntry[1])
                sUrl2 = aEntry[0].replace('\\\/','/').replace("\/","/")
                sThumb = 'https:' + str(aEntry[2]).replace('\\\/', '/').replace('\/','/')
                sDesc = ''
            elif 'iptvgratuit.com' in sUrl:
                sTitle = aEntry[0]
                sUrl2 = aEntry[1]
                sThumb = ''
                sDesc = ''
            else:
                sTitle = aEntry[1]
                sUrl2 = aEntry[0]
                sThumb = ''
                sDesc = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if 'myfree-tivi'  or 'firstonetv' in sUrl:
                oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            if 'iptvgratuit' and 'world-iptv-links' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showWorldIptvGratuit', sTitle, '', oOutputParameterHandler)
            elif 'firstonetv' in sUrl or 'myfree-tivi' in sUrl:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('play__')
                oGuiElement.setTitle(sTitle)
                oGuiElement.setFileName(sTitle)
                oGuiElement.setIcon(sThumb)
                oGuiElement.setMeta(0)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setDirectTvFanart()
                oGuiElement.setCat(6)

                oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
                oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
                oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
                oGui.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showWorldIptvGratuit():  # On recupere les liens qui sont dans les playlist 'World' de IptvGratuit
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    line = re.compile('http(.+?)\n').findall(sHtmlContent)

    for sUrl2 in line:
        sUrl2 = 'http' + sUrl2
        sTitle = 'Lien: ' + sUrl2
        # cConfig().log(str(sHtmlContent))

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getHtml(sUrl, data=None):  # S'occupe des requetes
    if 'firstonetv' in sUrl:
        cookies = GestionCookie().Readcookie('firstonetv')
    if 'myfree-tivi' and 'watch' in sUrl and not data is None:
        # VSlog(data)
        cookies = GestionCookie().Readcookie('myfree_tivi')
        headers = {'Host': 'www.myfree-tivi.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': sUrl,
            'X-CSRF-Token': data.replace('\n', '').replace('\r', ''),
            'Connection': 'keep-alive',
            'Cookie': cookies,
            'Content-Length': '0',
            'TE': 'Trailers'}

        r = requests.post('https://www.myfree-tivi.com/getdata', headers=headers)

    elif 'firstonetv'and '/France/' in sUrl:  # On passe les redirection
        aResult = re.findall('Live/.+?/*[^<>]+(?:-)([^"]+)', sUrl)
        idChannel = aResult[0]

        apiNumber = random.uniform(0.0000000000000000,0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParameters('action', 'hiro')
        oRequestHandler.addParameters('result', 'get')
        data = oRequestHandler.request()
        hiro = unFuckFirst(data)  # On decode Hiro

        sPattern = '"hiro":(.+?),"hash":"(.+?)","time":(.+?),'

        oParser = cParser()
        aResult = oParser.parse(hiro, sPattern)

        for aEntry in aResult[1]:
            hiro = aEntry[0]
            Hash = aEntry[1]
            time = aEntry[2]

        apiNumber = random.uniform(0.0000000000000000,0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParameters('action', 'hiro')
        oRequestHandler.addParameters('result', hiro)
        oRequestHandler.addParameters('time', time)
        oRequestHandler.addParameters('hash', Hash)
        data = oRequestHandler.request()

        aResult = re.findall('"ctoken":"(.+?)"}', data)
        cToken = aResult[0]

        apiNumber = random.uniform(0.0000000000000000,0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParameters('action', 'channel')
        oRequestHandler.addParameters('ctoken', cToken)
        oRequestHandler.addParameters('c', 'fr')
        oRequestHandler.addParameters('id', idChannel)
        oRequestHandler.addParameters('native_hls', '0')
        oRequestHandler.addParameters('unsecure_hls', '0')
        data = oRequestHandler.request()
        return data
    elif 'firstonetv' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Host', 'www.firstonetv.net')
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        data = oRequestHandler.request()
        return data

    if data == None and 'watch' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        data = oRequestHandler.request()
        cookies = oRequestHandler.GetCookies()
        GestionCookie().SaveCookie('myfree_tivi', cookies)
        return data

    else:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)

    if not data is None and 'watch' in sUrl:
        data = r.text
        VSlog(data)
    else:
        data = oRequestHandler.request()
    # VSlog(data)
    return data

def parseM3U(infile):  # Traite les m3u local
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'iptv4sat' in sUrl or '.zip' in sUrl:
        sHtmlContent = getHtml(sUrl)
        from zipfile import ZipFile
        import io
        zip_file = ZipFile(io.BytesIO(sHtmlContent))
        files = zip_file.namelist()
        with zip_file.open(files[0]) as f:
            sHtmlContent = []
            for line in f:
                sHtmlContent.append(line)
            inf = sHtmlContent

    elif not '#EXTM3U' in sUrl:
        site = infile
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(site, headers=headers)
        inf = urllib2.urlopen(req)
    else:
        inf = infile

    try:
        line = inf.readline()
    except:
        pass

    # cConfig().log(str(line))
    # if not line.startswith('#EXTM3U'):
        # return

    playlist = []
    song = track(None, None, None, None)
    ValidEntry = False

    for line in inf:

        line = line.strip()
        if line.startswith('#EXTINF:'):
            length, title = line.split('#EXTINF:')[1].split(',', 1)
            try:
                licon = line.split('#EXTINF:')[1].partition('tvg-logo=')[2]
                icon = licon.split('"')[1]
            except:
                icon = 'tv.png'
            ValidEntry = True

            song = track(length, title, None, icon)
        elif (len(line) != 0):
            if (ValidEntry) and (not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path = line
                playlist.append(song)
                # VSlog(playlist)
                song = track(None, None, None, None)

    try:
        inf.close()
    except:
        pass

    return playlist

def showWeb():  # Code qui s'occupe de liens TV du Web
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseM3U(sUrl)

    if (oInputParameterHandler.exist('AZ')):
        sAZ = oInputParameterHandler.getValue('AZ')
        string = filter(lambda t: t.title.strip().capitalize().startswith(sAZ), playlist)
        playlist = sorted(string, key=lambda t: t.title.strip().capitalize())
    else :
        playlist = sorted(playlist, key=lambda t: t.title.strip().capitalize())

    if not playlist:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addText(SITE_IDENTIFIER, "[COLOR red] Problème de lecture avec la playlist[/COLOR]")

    else:
        total = len(playlist)
        progress_ = progress().VScreate(SITE_NAME)
        for track in playlist:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sThumb = track.icon
            if not sThumb:
                sThumb = 'tv.png'

            # les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')
            if not '[' in url2 and not ']' in url2 and not '.m3u8' in url2:
                url2 = 'plugin://plugin.video.f4mTester/?url=' + QuotePlus(url2) + '&amp;streamtype=TSDOWNLOADER&name=' + Quote(track.title)

            thumb = '/'.join([sRootArt, sThumb])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url2)
            oOutputParameterHandler.addParameter('sMovieTitle', track.title)
            oOutputParameterHandler.addParameter('sThumbnail', thumb)

            # oGui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt + '/tv/' + sThumb, oOutputParameterHandler)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setTitle(track.title)
            oGuiElement.setFileName(track.title)
            oGuiElement.setIcon('tv.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(thumb)
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
            oGui.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        progress_.VSclose(progress_)
    oGui.setEndOfDirectory()

def direct_epg():  # Code qui gere l'epg
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    # aParams = oInputParameterHandler.getAllParameter()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sCom = cePg().view_epg(sTitle, 'direct')

def soir_epg():  # Code qui gere l'epg
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()

    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sCom = cePg().view_epg(sTitle, 'soir')

def enregistrement():  # Code qui gere l'epg
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')

    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        oDialog = dialog().VSok('Merci d\'activer l\'enregistrement dans les options')
        return

    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    if 'plugin' in sUrl:
        url = re.findall('url=(.+?)&amp', ''.join(sUrl))
        sUrl = Unquote(url[0])
    shebdule = cEnregistremement().programmation_enregistrement(sUrl)

def showAZ():

    import string
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    for i in string.digits:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showTV', i, 'az.png', oOutputParameterHandler)

    for i in string.ascii_uppercase:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showTV', i, 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAZRadio():

    import string
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    for i in string.digits:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showWeb', i, 'az.png', oOutputParameterHandler)

    for i in string.ascii_uppercase:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showWeb', i, 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showTV():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    # sPattern = '<url>([^<>]+?)</url><title>([^<>]+?)</title><order>' + sOrder + '</order><icon>(.+?)</icon>'
    sPattern = '<title>(.+?)</title><link>(.+?)</link>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        progress_ = progress().VScreate(SITE_NAME)

        # affiche par
        if (oInputParameterHandler.exist('AZ')):
            sAZ = oInputParameterHandler.getValue('AZ')
            string = filter(lambda t: t[0].strip().capitalize().startswith(sAZ), aResult[1])
            string = sorted(string, key=lambda t: t[0].strip().capitalize())
        else :
            string = sorted(aResult[1], key=lambda t: t[0].strip().capitalize())

        total = len(string)
        for aEntry in string:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[0])
            oOutputParameterHandler.addParameter('sThumbnail', 'tv.png')

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setTitle(aEntry[0])
            oGuiElement.setFileName(aEntry[0])
            oGuiElement.setIcon('tv.png')
            oGuiElement.setMeta(0)
            # oGuiElement.setThumbnail('tv.png')
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
            oGui.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def play__():  # Lancer les liens
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    # Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    playmode = ''

    if playmode == 0:
        stype = ''
        if '.ts' in sUrl:
            stype = 'TSDOWNLOADER'
        elif '.m3u' in sUrl:
            stype = 'HLS'
        if stype:
            from F4mProxy import f4mProxyHelper
            f4mp=f4mProxyHelper()
            xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
            f4mp.playF4mLink(sUrl, sTitle, proxy=None, use_proxy_for_chunks=False, maxbitrate=0, simpleDownloader=False, auth=None, streamtype=stype, setResolved=False, swf=None, callbackpath="", callbackparam="", iconImage=sThumbnail)
            return

    if 'f4mTester' in sUrl:
        xbmc.executebuiltin('XBMC.RunPlugin(' + sUrl + ')')
        return
    else:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sTitle)
        sUrl = sUrl.replace(' ','%20')
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        # tout repetter
        # xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")

        oPlayer.startPlayer()
        return

def openwindows():
    xbmc.executebuiltin("ActivateWindow(%d, return)" % (10601))
    return
