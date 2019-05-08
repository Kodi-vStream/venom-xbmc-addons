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

from resources.lib.enregistrement import cEnregistremement
from resources.lib.epg import cePg
from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog, dialog

import re, urllib2, urllib, sys, random, string
import xbmcplugin, xbmcvfs
import json, requests

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

def decodeEmail(e):
    head , e = e.split('a href=')
    e , rest = e.split('</a>')
    e = re.search('data-cfemail="(.+?)"',e).group(1)
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return head + str(de) + rest

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
    liste.append( ['Extinf','https://extinf.tk/'])

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

    if 'iptvsource.com' in sUrl:
        sPattern = '<h3 class="entry-title td-module-title"><a href="(.+?)" rel="bookmark" title="(.+?)"'
    elif 'iptvgratuit.com' in sUrl:
        sPattern = '<a href="([^"]+)" rel="bookmark".+?title="([^"]+)".+?</a></h3>'
    elif 'dailyiptvlist.com' in sUrl:
        sPattern = '</a><h2 class="post-title"><a href="(.+?)">(.+?)</a></h2><div class="excerpt"><p>.+?</p>'
    elif 'extinf' in sUrl:
        sPattern = '<div class="news-thumb col-md-6">\s*<a href=([^"]+) title="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if not 'extinf' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, 'tv.png', oOutputParameterHandler)
            else:
                if 'extinf' and 'daily-premium-m3u' in sUrl2:
                    oGui.addDir(SITE_IDENTIFIER, 'showDailyIptvList', sTitle, '', oOutputParameterHandler)
                else:
                    oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'tv.png', oOutputParameterHandler)

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

    if 'extinf' in sUrl:
        sPattern = '<a class="next page-numbers" href=([^"]+)>Next</a>'
    elif 'https://www.iptvsource.com/' in sUrl:
        sPattern = ' class="last" title=".+?">.+?</a><a href="(.+?)"><i class="td-icon-menu-right"></i>'
    elif 'iptvgratuit.com' in sUrl:
        sPattern = '<span class="current">.+?</span><a href="([^"]+)"'
    else:
        sPattern = '<a class="next page-numbers" href="(.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showAllPlaylist():#On recupere les differentes playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')
    sDesc = oInputParameterHandler.getValue('sDescription')

    sHtmlContent = getHtml(sUrl)

    if 'iptvgratuit.com' in sUrl:
        sPattern = 'Cliquez sur le lien.+?</strong></p>.+?<h4><a class="more-link" title="([^"]+)" href="([^"]+)".+?<button>'
    elif 'dailyiptvlist.com' in sUrl:
        sPattern = '<p></br><br /><strong>2. Click on link to download .+? iptv channels list</strong></p>.+?<a href="(.+?)">Download (.+?)</a>'
    elif 'iptvsource.com':
        sPattern = '<a href="([^"]+)">Download ([^"]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'iptvgratuit.com' in sUrl:
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

            oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showDailyIptvList():#On recupere les liens qui sont dans les playlist "World" de IptvGratuit
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    clearHtml = re.search('null>([\s*\S*]+)</pre><p>',sHtmlContent).group(1)
    line = re.compile('http(.+?)\n').findall(clearHtml)

    for sUrl2 in line:
        if '/cdn-cgi/l/email-protection' in str(sUrl2):
            sUrl2 = 'http' + decodeEmail(sUrl2).replace('<','')
        else:
            sUrl2 = 'http' + sUrl2

        sTitle = 'Lien: ' + sUrl2

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getHtml(sUrl, data=None):#S'occupe des requetes
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent',UA)

    if not data is None and 'watch' in sUrl:
        data = r.text
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
            if not '[' in url2 and not ']' in url2 and not '.m3u8' in url2 and not 'dailymotion' in url2:
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

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    if 'dailymotion' in sUrl:
        oGui = cGui()
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        metadata = json.loads(sHtmlContent)
        if metadata['qualities']:
            sUrl = str(metadata['qualities']['auto'][0]['url'])
        headers={'User-Agent':'Android'}
        mb = requests.get(sUrl,headers=headers).text
        mb = re.findall('NAME="([^"]+)"\n(.+)',mb)
        mb = sorted(mb,reverse=True)
        for quality, url1 in mb:

            sHosterUrl = url1
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle + ' ' +quality)
                oHoster.setFileName(sTitle + ' ' +quality)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        oGui.setEndOfDirectory()
        return

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
