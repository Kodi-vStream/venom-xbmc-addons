#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.player import cPlayer
from resources.lib.config import GestionCookie
from resources.lib.gui.hoster import cHosterGui
from resources.lib.jsunfuck import unFuckFirst

from resources.lib.enregistrement import cEnregistremement
from resources.lib.epg import cePg
from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog, dialog

import re, urllib2, urllib, sys, requests, random, json, string
import xbmcplugin, xbmcvfs

SITE_IDENTIFIER = 'freebox'
SITE_NAME = '[COLOR orange]Télévision Direct/Stream[/COLOR]'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'http://mafreebox.freebox.fr/freeboxtv/playlist.m3u'
URL_WEB = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/Beta/repo/resources/webtv2.m3u'
URL_RADIO = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/repo/resources/radio.m3u'

MOVIE_IPTVSITE = (True, 'showIptvSite')

UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}

icon = 'tv.png'
#/home/lordvenom/.kodi/
#sRootArt = cConfig().getRootArt()
sRootArt = "special://home/addons/plugin.video.vstream/resources/art/tv"
ADDON = addon()

class track():
    def __init__(self, length, title, path, icon,data=''):
        self.length = length
        self.title = title
        self.path = path
        self.icon = icon
        self.data = data

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_WEB)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30332), 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_IPTVSITE)
    oGui.addDir(SITE_IDENTIFIER, 'showIptvSite', 'Iptv (Sites)', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('radio', 'showGenres', addons.VSlang(30203) +' (Genres)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir('radio', 'showAZ', addons.VSlang(30203) +' (A-Z)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir('radio', 'showWeb', addons.VSlang(30203), 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('lsdb', 'load', 'Liveset Database', 'music.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showIptvSite():

    oGui = cGui()

    #test f4mTester
    sPath = "special://home/addons/plugin.video.f4mTester/default.py"

    if not xbmcvfs.exists(sPath):
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]plugin.video.f4mTester: L'addon n'est pas présent[/COLOR]")

    liste = []
    liste.append( ['IptvSource', 'https://www.iptvsource.com/'] )
    liste.append( ['Iptv Gratuit', 'http://iptvgratuit.com/'] )
    liste.append( ['Daily Iptv List', 'https://www.dailyiptvlist.com/'])
    liste.append( ['pavandayal (m3u8 playlist)', 'https://pavandayal.com/iptv/links.php'])
    liste.append( ['My Free Tivi (Connection au compte impossible a cause de Recaptcha)', 'https://www.myfree-tivi.com/livetv/pp67'])
    liste.append( ['FirstOneTv', 'https://www.firstonetv.live/Live/France'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showDailyList', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showDailyList(): #On recupere les dernier playlist ajouter au site
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)#On recupere le contenue de la page
    #VSlog(sHtmlContent)
    #VSlog(sUrl)

    if 'firstonetv' in sUrl:
        sPattern = '<div class="post-thumb">\s*<img src="(.+?)" alt="(.+?)">\s*<a href="(.+?)".+?>(?:\s*<img.+?\s*<.+?<b>(.+?)<.+?>(.+?)<.+?>.+?>(.+?)</text>.+?</b><br><br>(.+?)</span>|)'
    elif 'iptvsource.com' in sUrl:
        sPattern = '<h3 class="entry-title td-module-title"><a href="(.+?)" rel="bookmark" title="(.+?)"'
    elif 'iptvgratuit.com' in sUrl:
        sPattern = '<header class="entry-header">\s*<h2 class="entry-title">\s*<a href="(.+?)" rel="bookmark">(.+?)</a>'
    elif 'dailyiptvlist.com' in sUrl:
        sPattern = '</a><h2 class="post-title"><a href="(.+?)">(.+?)</a></h2><div class="excerpt"><p>.+?</p>'
    elif 'pavandayal' in sUrl:
        sPattern = '<p class="link" data-clipboard-text="(.+?)">(.+?)<'
    elif 'myfree-tivi' in sUrl:
        sPattern = '<a title="([^"]+)" href="([^"]+)" class=".+?">\s*<.+?>\s*<.+?style="background-image.+?url.+?[^\;](.+?)[^\&].+?[^\;](?:.|\s)+?<span class="teaser-lineB"([^"]+)</span>'

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
                sThumb = 'https://www.firstonetv.net' + aEntry[0]
                sTitle = aEntry[1]
                sUrl2 = 'https://www.firstonetv.net' + aEntry[2]
                sDesc = ('[COLOR skyblue]%s de %s a %s[/COLOR] \n [COLOR coral]Synopsis :[/COLOR] %s') % (aEntry[3], aEntry[4], aEntry[5], aEntry[6])

            if 'pavandayal' in sUrl:
                sTitle = aEntry[1]
            elif not 'myfree-tivi' in sUrl and not 'firstonetv' in sUrl:
                sTitle = aEntry[1]

            if 'myfree-tivi' in sUrl and not 'firstonetv' in sUrl:
                sThumb = "https:" + aEntry[2]
                sUrl2 = 'https://www.myfree-tivi.com'+ aEntry[1]
                sTitle = aEntry[0]
                sDesc = aEntry[3]
            elif not 'myfree-tivi' in sUrl and not 'firstonetv' in sUrl:
                sUrl2 = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if 'firstonetv' in sUrl or 'myfree-tivi' in sUrl:
                oOutputParameterHandler.addParameter('sDescription', sDesc)
                oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            if 'myfree-tivi' in sUrl or 'firstonetv' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'pavandayal' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'tv.png', oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, 'tv.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showDailyList', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent): #Affiche les page suivant si il y en a
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'myfree-tivi' in sUrl:
        sPattern = '<li class="page-item"><a class="page-link waves-effect" href="(.+?)" data-page=".+.?">.+?<div class="clearfix"></div></nav></div>'
    elif 'https://www.iptvsource.com/' in sUrl:
        sPattern = ' class="last" title=".+?">.+?</a><a href="(.+?)"><i class="td-icon-menu-right"></i>'
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

def showAllPlaylist():#On recupere les differentes playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')
    sDesc = oInputParameterHandler.getValue('sDescription')
    #VSlog(str(sUrl))
    if 'firstonetv' and 'Register-Login' in sUrl:

        session = requests.Session()
        url = 'https://www.firstonetv.live/Register-Login'
        data = {'usrmail':ADDON.getSetting('hoster_firstonetv_username'),
                'password':ADDON.getSetting('hoster_firstonetv_password'),
                'login':'Login+Now'}

        headers = {'user-agent':UA,
                    'Content-Type':'application/x-www-form-urlencoded',
                    'Referer':'https://www.firstonetv.live/Index',
                    'Content-Length': str(len(data))}

        session.post(url, data=data, headers=headers)
        cookiesDict = requests.utils.dict_from_cookiejar(session.cookies)
        getUser = re.match("{'(.+?)': '(.+?)',",str(cookiesDict))
        #VSlog(cookiesDict)
        cookies = str(getUser.group(1)) + '=' + str(getUser.group(2))
        GestionCookie().SaveCookie('firstonetv', cookies)
        dialog().VSinfo('Authentification reussie merci de recharger la page', "FirstOneTv", 15)
        return

    sHtmlContent = getHtml(sUrl)

    if 'myfree-tivi' in sUrl:
        aResult = re.findall('<meta name="csrf-token" content="(.+?)">',sHtmlContent)
        if aResult:
            token = aResult[0]
            #VSlog(token)
            sHtmlContent = getHtml(sUrl,token)

    if 'firstonetv' in sUrl:
        sPattern = '"([^"]+).m3u8'
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
                sTitle = sTitle
                sDesc = sDesc
                sThumb = sThumb
                if aEntry.startswith('/hls/'):
                    sUrl2 = 'https://rtm-1.firstonetv.live:4433'+aEntry.replace('\\\/','/').replace("\/","/") + '.m3u8|Referer='+sUrl+'&User-Agent='+UA+'&X-Requested-With=ShockwaveFlash/28.0.0.137&Origin=https://www.firstonetv.live'
                else:
                    sUrl2 = aEntry.replace('\\\/','/').replace("\/","/") + '.m3u8|Referer='+sUrl+'&User-Agent='+UA+'&X-Requested-With=ShockwaveFlash/28.0.0.137&Origin=https://www.firstonetv.live'
            elif 'myfree-tivi' in sUrl:
                sTitle = str(aEntry[1])
                sUrl2 = aEntry[0].replace('\\\/','/').replace("\/","/")
                sThumb = 'https:' + str(aEntry[2]).replace('\\\/','/').replace("\/","/")
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
                oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showWorldIptvGratuit():#On recupere les liens qui sont dans les playlist "World" de IptvGratuit
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    line = re.compile('http(.+?)\n').findall(sHtmlContent)

    for sUrl2 in line:
        sUrl2 = 'http' + sUrl2
        sTitle = 'Lien: ' + sUrl2
        #cConfig().log(str(sHtmlContent))

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getHtml(sUrl, data=None):#S'occupe des requetes
    if 'firstonetv' in sUrl:
        cookies = GestionCookie().Readcookie('firstonetv')
    if 'myfree-tivi' and 'watch' in sUrl and not data is None:
        #VSlog(data)
        cookies = GestionCookie().Readcookie('myfree_tivi')
        headers = {'Host': 'www.myfree-tivi.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': sUrl,
            'X-CSRF-Token': data.replace('\n','').replace('\r',''),
            'Connection': 'keep-alive',
            'Cookie':cookies,
            'Content-Length':'0',
            'TE': 'Trailers'}

        r = requests.post('https://www.myfree-tivi.com/getdata', headers=headers)

    elif 'firstonetv'and '/France/' in sUrl:#On passe les redirection
        aResult = re.findall('Live/.+?/*[^<>]+(?:-)([^"]+)',sUrl)
        idChannel = aResult[0]

        apiNumber = random.uniform(0.0000000000000000,0.9999999999999999)
        url = 'https://www.firstonetv.live/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Cookie',cookies)
        oRequestHandler.addParameters('action','hiro')
        oRequestHandler.addParameters('result','get')
        data = oRequestHandler.request()
        hiro = unFuckFirst(data)#On decode Hiro

        sPattern = '"hiro":(.+?),"hash":"(.+?)","time":(.+?),'

        oParser = cParser()
        aResult = oParser.parse(hiro, sPattern)

        for aEntry in aResult[1]:
            hiro = aEntry[0]
            Hash = aEntry[1]
            time = aEntry[2]

        apiNumber = random.uniform(0.0000000000000000,0.9999999999999999)
        url = 'https://www.firstonetv.live/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Cookie',cookies)
        oRequestHandler.addParameters('action','hiro')
        oRequestHandler.addParameters('result',hiro)
        oRequestHandler.addParameters('time',time)
        oRequestHandler.addParameters('hash',Hash)
        data = oRequestHandler.request()

        aResult = re.findall('"ctoken":"(.+?)"}',data)
        cToken = aResult[0]

        apiNumber = random.uniform(0.0000000000000000,0.9999999999999999)
        url = 'https://www.firstonetv.live/api/?cacheFucker=' + str(apiNumber)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Cookie',cookies)
        oRequestHandler.addParameters('action','channel')
        oRequestHandler.addParameters('ctoken',cToken)
        oRequestHandler.addParameters('c','fr')
        oRequestHandler.addParameters('id',idChannel)
        oRequestHandler.addParameters('native_hls','0')
        oRequestHandler.addParameters('unsecure_hls','0')
        oRequestHandler.addParameters('worldstream','{"RTM":16387,"AMS":999999,"DUB":10280,"IAD":11158}')
        data = oRequestHandler.request()
        return data
    elif 'firstonetv' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Host','www.firstonetv.live')
        oRequestHandler.addHeaderEntry('Cookie',cookies)
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
        oRequestHandler.addHeaderEntry('User-Agent',UA)

    if not data is None and 'watch' in sUrl:
        data = r.text
        VSlog(data)
    else:
        data = oRequestHandler.request()
    #VSlog(data)
    return data

def parseM3U(infile):#Traite les m3u local
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
        site= infile
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'
        headers = {'User-Agent': user_agent}
        #req = urllib2.Request(site,headers=headers)
        #inf = urllib2.urlopen(req)
        
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent',user_agent)
        inf = oRequestHandler.request()

        inf = inf.split('\n')
           
    else:
        inf = infile

    try:
        line = inf.readline()
    except:
        pass

    #cConfig().log(str(line))
    #if not line.startswith('#EXTM3U'):
        #return

    playlist=[]
    song=track(None,None,None,None)
    ValidEntry = False

    for line in inf:

        line=line.strip()
        if line.startswith('#EXTINF:'):
            length,title=line.split('#EXTINF:')[1].split(',',1)
            try:
                licon = line.split('#EXTINF:')[1].partition('tvg-logo=')[2]
                icon = licon.split('"')[1]
            except:
                icon = "tv.png"
            ValidEntry = True

            song=track(length,title,None,icon)
        elif (len(line) != 0):
            if (ValidEntry) and (not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path=line
                playlist.append(song)
                #VSlog(playlist)
                song=track(None,None,None,None)

    try:
        inf.close()
    except:
        pass

    return playlist

def showWeb():#Code qui s'occupe de liens TV du Web
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
        oGui.addText(SITE_IDENTIFIER, "[COLOR red] Problème de lecture avec la playlist[/COLOR] ")

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

            #les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')
            if not '[' in url2 and not ']' in url2 and not '.m3u8' in url2:
                url2 = 'plugin://plugin.video.f4mTester/?url=' + urllib.quote_plus(url2) + '&amp;streamtype=TSDOWNLOADER&name=' + urllib.quote(track.title)

            thumb = "/".join([sRootArt, sThumb])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url2)
            oOutputParameterHandler.addParameter('sMovieTitle', track.title)
            oOutputParameterHandler.addParameter('sThumbnail', thumb)

            #oGui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt + '/tv/' + sThumb, oOutputParameterHandler)

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
            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        progress_.VSclose(progress_)
    oGui.setEndOfDirectory()

def direct_epg():#Code qui gerent l'epg
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    #aParams = oInputParameterHandler.getAllParameter()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sCom = cePg().get_epg(sTitle, 'direct')

def soir_epg():#Code qui gerent l'epg
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()

    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sCom = cePg().get_epg(sTitle, 'soir')

def enregistrement():#Code qui gerent l'epg
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')

    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        oDialog = dialog().VSok('Merci d\'activer l\'enregistrement dans les option')
        return

    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    if 'plugin' in sUrl:
        url = re.findall('url=(.+?)&amp',''.join(sUrl))
        sUrl = urllib2.unquote(url[0])
    shebdule = cEnregistremement().programmation_enregistrement(sUrl)

def showAZ():

    import string
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
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
    #sPattern = '<url>([^<>]+?)</url><title>([^<>]+?)</title><order>' + sOrder + '</order><icon>(.+?)</icon>'
    sPattern = '<title>(.+?)</title><link>(.+?)</link>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        progress_ = progress().VScreate(SITE_NAME)

        #affiche par
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
            #oGuiElement.setThumbnail('tv.png')
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def play__():#Lancer les liens
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #Special url with tag
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
        #tout repetter
        xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")

        oPlayer.startPlayer()
        return

def GetRealUrl(chain):#Recupere les liens des regex

    oParser = cParser()

    UA2 = UA
    url = chain
    regex = ''
    sHtmlContent = ''

    r = re.search('\[[REGEX]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if (r):
        regex = r.group(1)

    r = re.search('\[[UA]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if (r):
        UA2 = r.group(1)

    r = re.search('\[[URL]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if (r):
        url = r.group(1)

    #post metehod ?
    r = re.search('\[[POSTFORM]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if (r):
        param = r.group(1)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'identity')
        oRequestHandler.addParametersLine(param)
        sHtmlContent = oRequestHandler.request()
    else:
        if (url):
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

    #VSlog(sHtmlContent)

    if regex:
        aResult2 = oParser.parse(sHtmlContent, regex)
        if (aResult2):
            url = aResult2[1][0]

    #VSlog('Url recuperee : ' + url)

    url = url + '|User-Agent=' + UA2

    return url

def openwindows():
    xbmc.executebuiltin( "ActivateWindow(%d, return)" % ( 10601, ) )
    return
