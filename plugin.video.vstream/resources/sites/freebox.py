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

from resources.lib.epg import cePg
from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog

import re, urllib2, urllib, sys
import xbmcplugin, xbmcvfs

SITE_IDENTIFIER = 'freebox'
SITE_NAME = '[COLOR orange]Télévision Direct / Stream[/COLOR]'
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
    oGui.addDir(SITE_IDENTIFIER, 'showIptvSite', 'Liste site Iptv', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showAZRadio', addons.VSlang(30203)+' (A-Z)', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30203), 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showIptvSite():

    oGui = cGui()

    #test f4mTester
    sPath = "special://home/addons/plugin.video.f4mTester/default.py"

    if not xbmcvfs.exists(sPath):
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]plugin.video.f4mTester : L'addon n'est pas présent[/COLOR]")

    liste = []
    liste.append( ['IptvSource', 'https://www.iptvsource.com/'] )
    liste.append( ['Iptv Gratuit', 'http://iptvgratuit.com/'] )
    liste.append( ['Daily Iptv List', 'https://www.dailyiptvlist.com/'])

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
    #VSlog(str(sHtmlContent))

    if 'iptvsource.com' in sUrl:
        sPattern = '<h3 class="entry-title td-module-title"><a href="(.+?)" rel="bookmark" title="(.+?)"'
    elif 'iptvgratuit.com' in sUrl:
        sPattern = '<header class="entry-header">\s*<h2 class="entry-title">\s*<a href="(.+?)" rel="bookmark">(.+?)</a>'
    elif 'dailyiptvlist.com' in sUrl:
        sPattern = '</a><h2 class="post-title"><a href="(.+?)">(.+?)</a></h2><div class="excerpt"><p>.+?</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

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

    if 'https://www.iptvsource.com/' in sUrl:
        sPattern = ' class="last" title=".+?">.+?</a><a href="(.+?)"><i class="td-icon-menu-right"></i>'
    else:
        sPattern = '<a class="next page-numbers" href="(.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showAllPlaylist():#On recuepere les differente playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    #cConfig().log(str(sUrl))

    sHtmlContent = getHtml(sUrl)

    if 'iptvgratuit.com' in sUrl:
        sPattern = '<strong>2. Cliquez sur le lien pour télécharger la liste des chaînes .+?</strong></p><h4><a class="more-link" title="(.+?)" href="(.+?)" target="_blank"'
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

            if 'iptvgratuit.com' in sUrl:
                sTitle = str(aEntry[0])
                sUrl2 = str(aEntry[1])
            else:
                sTitle = str(aEntry[1])
                sUrl2 = str(aEntry[0])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if 'iptvgratuit' and 'world-iptv-links-m3u-playlist-' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showWorldIptvGratuit', sTitle, '', oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'parseWebM3U', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showWorldIptvGratuit():#On recupere les liens qui sont dans les playlist "World" de IptvGratuit
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    line = re.compile('http(.+?)\n').findall(sHtmlContent)

    for sUrl2 in line:
        sUrl2 = 'http'+sUrl2
        sTitle = 'Lien: '+sUrl2
        #cConfig().log(str(sHtmlContent))

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

        oGui.addDir(SITE_IDENTIFIER, 'parseWebM3U', sTitle, 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getHtml(sUrl, referer=None, hdr=None, data=None):#S'occupe des requete
    req = urllib2.Request(sUrl, data, headers)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    VSlog(data)
    return data

def parseWebM3U():#Traite les m3u
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    #cConfig().log(str(sUrl))

    line = re.compile('EXTINF:.+?,(.+?)\n(.+?)\n').findall(sHtmlContent)

    for sTitle, sUrl2 in line:
        sUrl2 = sUrl2.replace('\r','')

        #with open('D:\\playlist.m3u', 'r+b') as f:
        #    f.seek(0,2)
        #    f.write('\n'+'#EXTINF:-1,'+sTitle)
        #    f.write('\n'+sUrl2)

        icon = "tv.png"
        if '.ts' in sUrl2:
            sUrl2 = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(sUrl2)+'&amp;streamtype=TSDOWNLOADER&name='+urllib.quote(sTitle)

        ok = True
        liz = xbmcgui.ListItem(sTitle, iconImage="DefaultVideo.png", thumbnailImage=icon)
        commands = []
        direct_epg_url= "plugin://plugin.video.vstream/?site=freebox&function=direct_epg&sMovieTitle="+urllib.quote(sTitle)+"&siteUrl="+urllib.quote_plus(sUrl2)+"&sFav=play__&sThumbnail="+urllib.quote(icon)+"&sId=freebox&sCat=6"
        commands.append(( "Direct Epg" , 'RunPlugin('+ direct_epg_url +')'))
        soir_epg_url = "plugin://plugin.video.vstream/?site=freebox&function=soir_epg&sMovieTitle="+urllib.quote(sTitle)+"&siteUrl="+urllib.quote_plus(sUrl2)+"&sFav=play__&sThumbnail="+urllib.quote(icon)+"&sId=freebox&sCat=6"
        commands.append(( "Soir Epg" , 'RunPlugin('+ soir_epg_url +')'))
        liz.addContextMenuItems( commands )
        liz.setArt({'thumb': icon, 'icon': icon})
        liz.setInfo(type="Video", infoLabels={"Title": sTitle})
        video_streaminfo = {'codec': 'h264'}
        liz.addStreamInfo('video', video_streaminfo)
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sUrl2, listitem=liz, isFolder=False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def showWeb():#Code qui s'occupe de liens TV du Web
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseWebM3URegex(sUrl)

    if (oInputParameterHandler.exist('AZ')):
        sAZ = oInputParameterHandler.getValue('AZ')
        string = filter(lambda t: t.title.strip().capitalize().startswith(sAZ), playlist)
        playlist = sorted(string, key=lambda t: t.title.strip().capitalize())
    else :
        playlist = sorted(playlist, key=lambda t: t.title.strip().capitalize())

    if not playlist:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addText(SITE_IDENTIFIER, "[COLOR red] Probleme de lecture avec la playlist[/COLOR] ")

    else:
        for track in playlist:
            sThumb = track.icon
            if not sThumb:
                sThumb = 'tv.png'

            #les + ne peuvent pas passer
            url2 = str(track.path).replace('+','P_L_U_S')
            thumb = "/".join([sRootArt, sThumb])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url2)
            oOutputParameterHandler.addParameter('sMovieTitle', str(track.title))
            oOutputParameterHandler.addParameter('sThumbnail', thumb)

            #oGui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt+'/tv/'+sThumb, oOutputParameterHandler)

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

            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,SITE_IDENTIFIER,SITE_IDENTIFIER,'direct_epg','Guide tv Direct')
            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,SITE_IDENTIFIER,SITE_IDENTIFIER,'soir_epg','Guide tv Soir')
            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def direct_epg():#Code qui gerent l'epg
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    #aParams = oInputParameterHandler.getAllParameter()
    #print aParams
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sCom = cePg().get_epg(sTitle,'direct')

def soir_epg():#Code qui gerent l'epg
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()

    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sCom = cePg().get_epg(sTitle,'soir')

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
            oOutputParameterHandler.addParameter('sThumbnail', str('tv.png'))

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

            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,SITE_IDENTIFIER,SITE_IDENTIFIER,'direct_epg','Guide tv Direct')
            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,SITE_IDENTIFIER,SITE_IDENTIFIER,'soir_epg','Guide tv Soir')
            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def parseWebM3URegex(infile):#Ancien fonction pour traiter les m3u
    site= infile
    user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(site,headers=headers)
    inf = urllib2.urlopen(req)

    line = inf.readline()

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
                song=track(None,None,None,None)

    inf.close()

    return playlist

def parseM3U(infile):#Traite les m3u local
    inf = open(infile,'r')

    line = inf.readline()
    if not line.startswith('#EXTM3U'):
       return

    playlist=[]
    song=track(None,None,None,None)
    ValidEntry = False

    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            length,title=line.split('#EXTINF:')[1].split(',',1)
            song=track(length,title,None,None)
            ValidEntry = True
        elif (len(line) != 0):
            if (not line.startswith('!') and ValidEntry):
                ValidEntry = False
                song.path=line
                playlist.append(song)
                song=track(None,None,None,None)

    inf.close()

    return playlist

def play__():#Lancer les liens
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S','+')
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
            f4mp.playF4mLink(sUrl,sTitle,proxy=None,use_proxy_for_chunks=False, maxbitrate=0, simpleDownloader=False, auth=None, streamtype=stype,setResolved=False,swf=None , callbackpath="",callbackparam="", iconImage=sThumbnail)
            return

    listitem = xbmcgui.ListItem(sTitle, iconImage="DefaultVideo.png", thumbnailImage=sThumbnail)
    listitem.setInfo('video', {'Title': sTitle})
    listitem.setProperty("IsPlayable","true")
    #xbmc.Player().play(sUrl, listitem)

    if 'f4mTester' in sUrl:
        xbmc.executebuiltin('XBMC.RunPlugin('+sUrl+')')
    else:
        xbmc.Player().play(sUrl, listitem)
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
        oRequestHandler.addHeaderEntry('Accept-Encoding','identity')
        oRequestHandler.addParametersLine(param)
        sHtmlContent = oRequestHandler.request()
    else:
        if (url):
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

    #xbmc.log(sHtmlContent)

    if regex:
        aResult2 = oParser.parse(sHtmlContent, regex)
        if (aResult2):
            url = aResult2[1][0]

    #xbmc.log('Url recuperee : ' + url)

    url = url + '|User-Agent=' + UA2

    return url

def openwindows():
    xbmc.executebuiltin( "ActivateWindow(%d, return)" % ( 10601, ) )
    return
