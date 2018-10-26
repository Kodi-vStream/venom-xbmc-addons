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
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showAZRadio', addons.VSlang(30203) +' (A-Z)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30203), 'music.png', oOutputParameterHandler)

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
    liste.append( ['Iptvurls (m3u8 playlist)', 'http://www.iptvurls.com/iptv-daily-m3u-playlist/'])
    liste.append( ['My Free Tivi', 'https://www.myfree-tivi.com/livetv/pp67'])
    liste.append( ['FirstOneTv', 'https://www.firstonetv.net/Live/France'])

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
    elif 'iptvurls' in sUrl:
        sPattern = '<strong><span style=" font-size:10px; color:#06C">(.+?)</span.+?[|](.+?)-(.+?)-(.+?)</strong><br'
    elif 'myfree-tivi' in sUrl:
        sPattern = '<img.+?src="(.+?)">\s*</a>\s*</div>\s*<div class="list-item-detals">\s*<a href="(.+?)" title="(.+?)">\s*<.+?\s*<hr>\s*<p class="list-item-text">(.+?)</p>'

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

            if 'iptvurls' in sUrl:
                sTitle = "Playlist du : " + aEntry[3] +  '-' + aEntry[2] + '-' + aEntry[1]
            elif not 'myfree-tivi' in sUrl and not 'firstonetv' in sUrl:
                sTitle = aEntry[1]

            if 'myfree-tivi' in sUrl and not 'firstonetv' in sUrl:
                sThumb = "https:" + aEntry[0]
                sUrl2 = 'https://www.myfree-tivi.com'+ aEntry[1]
                sTitle = aEntry[2]
                sDesc = aEntry[3]
            elif not 'myfree-tivi' in sUrl and not 'firstonetv' in sUrl:
                sUrl2 = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if 'firstonetv' in sUrl:
                oOutputParameterHandler.addParameter('sDescription', sDesc)
                oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            if 'myfree-tivi' in sUrl or 'firstonetv' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'iptvurls' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'parseWebM3U', sTitle, 'tv.png', oOutputParameterHandler)
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
        url = 'https://www.firstonetv.net/Register-Login'
        data = {'usrmail':ADDON.getSetting('hoster_firstonetv_username'),
                'password':ADDON.getSetting('hoster_firstonetv_password'),
                'login':'Login+Now'}

        headers = {'user-agent':UA,
                    'Content-Type':'application/x-www-form-urlencoded',
                    'Referer':'https://www.firstonetv.net/Index',
                    'Content-Length': str(len(data))}

        session.post(url, data=data, headers=headers)
        cookiesDict = requests.utils.dict_from_cookiejar(session.cookies)
        getUser = re.match("{'(.+?)': '(.+?)',",str(cookiesDict))
        VSlog(cookiesDict)
        cookies = str(getUser.group(1)) + '=' + str(getUser.group(2))
        GestionCookie().SaveCookie('firstonetv', cookies)
        dialog().VSinfo('Authentification reussie merci de recharger la page', "FirstOneTv", 15)
        return

    sHtmlContent = getHtml(sUrl)

    if 'myfree-tivi' in sUrl:
        aResult = re.findall('<meta name="csrf-token" content="(.+?)">',sHtmlContent)
        if aResult:
            token = aResult[0]
            VSlog(token)
            sHtmlContent = getHtml(sUrl,token)

    if 'firstonetv' in sUrl:
        sPattern = '(?:"surl":"{\".+?|,.+?)"([^"]+)\".+?"http([^"]+).m3u8'
    elif 'myfree-tivi' in sUrl:
        sPattern = "thumb'.+?'(.+?)'.+?title.+?'(.+?)'.+?url'.+?'(.+?)'"
    elif 'iptvgratuit.com' in sUrl:
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

            if 'firstonetv' in sUrl:
                sTitle = sTitle + aEntry[0]
                sDesc = sDesc
                sThumb = sThumb
                sUrl2 = 'http' + aEntry[1].replace('\\\/','/').replace("\/","/") + '.m3u8|Referer='+sUrl+'&User-Agent='+UA+'&X-Requested-With=ShockwaveFlash/28.0.0.137&Origin=https://www.firstonetv.net'
            elif 'myfree-tivi' in sUrl:
                sTitle = str(aEntry[1])
                sUrl2 = str(aEntry[2])
                sThumb = 'https:' + str(aEntry[0])
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
            elif 'firstonetv' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'play__', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif not 'firstonetv' or not 'myfree-tivi' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'parseWebM3U', sTitle, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'play__', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

        oGui.addDir(SITE_IDENTIFIER, 'parseWebM3U', sTitle, 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getHtml(sUrl, data=None):#S'occupe des requetes
    if 'firstonetv' in sUrl:
        cookies = GestionCookie().Readcookie('firstonetv')
    if 'myfree-tivi' and 'watch' in sUrl:
        VSlog(data)
        cookies = GestionCookie().Readcookie('myfree_tivi')
        headers = {'Host': 'www.myfree-tivi.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': sUrl,
            'X-CSRF-Token': data,
            'Connection': 'keep-alive',
            'Cookie':cookies,
            'Content-Length':'0',
            'TE': 'Trailers'}

        r = requests.post('https://www.myfree-tivi.com/getdata', headers=headers)

    elif 'firstonetv'and '/France/' in sUrl:#On passe les redirection
        aResult = re.findall('Live/.+?/*[^<>]+(?:-)([^"]+)',sUrl)
        idChannel = aResult[0]

        apiNumber = random.uniform(0.0000000000000000,0.9999999999999999)
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
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
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
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
        url = 'https://www.firstonetv.net/api/?cacheFucker=' + str(apiNumber)
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
        data = oRequestHandler.request()

        return data
    elif 'firstonetv' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Host','www.firstonetv.net')
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

    if not data == None and 'watch' in sUrl:
        data = r.json()
        VSlog(data)
    else:
        data = oRequestHandler.request()
    #VSlog(data)
    return data

def parseWebM3U():#Traite les m3u
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    line = re.compile('EXTINF:.+?,(.+?)\n(.+?)\n').findall(sHtmlContent)

    if line:
        total = len(line)

    progress_ = progress().VScreate(SITE_NAME)

    for sTitle, sUrl2 in line:
        progress_.VSupdate(progress_, total)
        if progress_.iscanceled():
            break
        sUrl2 = sUrl2.replace('\r', '')

        #with open('D:\\playlist.m3u', 'r+b') as f:
        #    f.seek(0,2)
        #    f.write('\n'+'#EXTINF:-1, '+sTitle)
        #    f.write('\n'+sUrl2)

        #testtt

        if '.ts' in sUrl2:
            sUrl2 = 'plugin://plugin.video.f4mTester/?url=' + urllib.quote_plus(sUrl2) + '&amp;streamtype=TSDOWNLOADER&name=' + urllib.quote(sTitle)
        else :
            sUrl2 = urllib.quote_plus(sUrl2)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumbnail', "tv.png")

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('play__')
        oGuiElement.setTitle(sTitle)
        oGuiElement.setFileName(sTitle)
        oGuiElement.setIcon('tv.png')
        oGuiElement.setMeta(0)
        oGuiElement.setThumbnail("tv.png")
        oGuiElement.setCat(6)

        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
        #oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'recording', 'Recording')
        oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

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
        oGui.addText(SITE_IDENTIFIER, "[COLOR red] Problème de lecture avec la playlist[/COLOR] ")

    else:
        for track in playlist:
            sThumb = track.icon
            if not sThumb:
                sThumb = 'tv.png'

            #les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')
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
            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

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

def recording():#Code qui gerent l'epg
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

    tr = Threading()

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
            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def parseWebM3URegex(infile):#Ancien fonction pour traiter les m3u
    site= infile
    user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(site, headers=headers)
    inf = urllib2.urlopen(req)

    line = inf.readline()

    #cConfig().log(str(line))
    #if not line.startswith('#EXTM3U'):
        #return

    playlist=[]
    song=track(None, None, None, None)
    ValidEntry = False

    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            length,title=line.split('#EXTINF:')[1].split(',', 1)
            try:
                licon = line.split('#EXTINF:')[1].partition('tvg-logo=')[2]
                icon = licon.split('"')[1]
            except:
                icon = "tv.png"
            ValidEntry = True

            song=track(length, title, None, icon)
        elif (len(line) != 0):
            if (ValidEntry) and (not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path=line
                playlist.append(song)
                song=track(None, None, None, None)

    inf.close()

    return playlist

def play__():#Lancer les liens
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    if 'f4mTester' in sUrl:
        xbmc.executebuiltin('XBMC.RunPlugin(' + sUrl + ')')
        return
    if 'firstonetv' or 'bouygtel' in sUrl:
        sHosterUrl = sUrl
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        oGui.setEndOfDirectory()
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

class JSUnfuck(object):#Utile pour decoder Hiro (parametre utiliser par firstOneTv)

    numbers = None
    words = {
        "(![]+[])": "false",
        "([]+{})": "[object Object]",
        "(!![]+[])": "true",
        "([][[]]+[])": "undefined",
        "(+{}+[])": "NaN",
        "([![]]+[][[]])": "falseundefined",
        "([][f+i+l+t+e+r]+[])": "function filter() { [native code] }",
        "(!![]+[][f+i+l+t+e+r])": "truefunction filter() { [native code] }",
        "(+![]+([]+[])[c+o+n+s+t+r+u+c+t+o+r])": "0function String() { [native code] }",
        "(+![]+[![]]+([]+[])[c+o+n+s+t+r+u+c+t+o+r])": "0falsefunction String() { [native code] }",
        "([]+[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +l+o+c+a+t+i+o+n)())": "https://123movies.to",
        "([]+[])[f+o+n+t+c+o+l+o+r]()": '<font color="undefined"></font>',
        "(+(+!![]+e+1+0+0+0)+[])": "Infinity",
        "(+[![]]+[][f+i+l+t+e+r])": 'NaNfunction filter() { [native code] }',
        '(+[![]]+[+(+!+[]+(!+[]+[])[3]+[1]+[0]+[0]+[0])])': 'NaNInfinity',
        '([]+[])[i+t+a+l+i+c+s]()': '<i></i>',
        '[[]][c+o+n+c+a+t]([[]])+[]': ',',
        '([][f+i+l+l]+[])': 'function fill() {    [native code]}',
        '(!![]+[][f+i+l+l])': 'truefunction fill() {    [native code]}',
        '((+[])[c+o+n+s+t+r+u+c+t+o+r]+[])': 'function Number() {[native code]}  _display:45:1',
        '(+(+!+[]+[1]+e+[2]+[0])+[])': '1.1e+21',
        '([]+[])[c+o+n+s+t+r+u+c+t+o+r][n+a+m+e]': 'S+t+r+i+n+g',
        '([][e+n+t+r+i+e+s]()+[])': '[object Array Iterator]',
        '([]+[])[l+i+n+k](")': '<a href="&quot;"></a>',
        '(![]+[0])[i+t+a+l+i+c+s]()': '<i>false0</i>',
        # dummy to force array dereference
        'DUMMY1': '6p',
        'DUMMY2': '2x',
        'DUMMY3': '%3C',
        'DUMMY4': '%5B',
        'DUMMY5': '6q',
        'DUMMY6': '4h',
    }

    uniqs = {
        '[t+o+S+t+r+i+n+g]': 1,
        '[][f+i+l+t+e+r][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +e+s+c+a+p+e)()': 2,
        '[][f+i+l+t+e+r][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +u+n+e+s+c+a+p+e)()': 3,
        '[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +e+s+c+a+p+e)()': 2,
        '[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +u+n+e+s+c+a+p+e)()': 3,
    }

    def __init__(self, js):
        self.js = js

    def decode(self, replace_plus=True):
        while True:
            start_js = self.js
            self.repl_words(self.words)
            self.repl_numbers()
            self.repl_arrays(self.words)
            self.repl_uniqs(self.uniqs)
            if start_js == self.js:
                break

        if replace_plus:
            self.js = self.js.replace('+', '')
        self.js = re.sub('\[[A-Za-z]*\]', '', self.js)
        self.js = re.sub('\[(\d+)\]', '\\1', self.js)
        return self.js

    def repl_words(self, words):
        while True:
            start_js = self.js
            for key, value in sorted(words.items(), key=lambda x: len(x[0]), reverse=True):
                self.js = self.js.replace(key, value)

            if self.js == start_js:
                break

    def repl_arrays(self, words):
        for word in sorted(words.values(), key=lambda x: len(x), reverse=True):
            for index in xrange(0, 100):
                try:
                    repl = word[index]
                    self.js = self.js.replace('%s[%d]' % (word, index), repl)
                except:
                    pass

    def repl_numbers(self):
        if self.numbers is None:
            self.numbers = self.__gen_numbers()

        while True:
            start_js = self.js
            for key, value in sorted(self.numbers.items(), key=lambda x: len(x[0]), reverse=True):
                self.js = self.js.replace(key, value)

            if self.js == start_js:
                break

    def repl_uniqs(self, uniqs):
        for key, value in uniqs.iteritems():
            if key in self.js:
                if value == 1:
                    self.__handle_tostring()
                elif value == 2:
                    self.__handle_escape(key)
                elif value == 3:
                    self.__handle_unescape(key)

    def __handle_tostring(self):
        for match in re.finditer('(\d+)\[t\+o\+S\+t\+r\+i\+n\+g\](\d+)', self.js):
            repl = to_base(match.group(1), match.group(2))
            self.js = self.js.replace(match.group(0), repl)

    def __handle_escape(self, key):
        while True:
            start_js = self.js
            offset = self.js.find(key) + len(key)
            if self.js[offset] == '(' and self.js[offset + 2] == ')':
                c = self.js[offset + 1]
                self.js = self.js.replace('%s(%s)' % (key, c), urllib.quote(c))

            if start_js == self.js:
                break

    def __handle_unescape(self, key):
        start = 0
        while True:
            start_js = self.js
            offset = self.js.find(key, start)
            if offset == -1: break

            offset += len(key)
            expr = ''
            extra = ''
            last_c = self.js[offset - 1]
            abort = False
            for i, c in enumerate(self.js[offset:]):
                extra += c
                if c == ')':
                    break
                elif (i > 0 and c == '(') or (c == '[' and last_c != '+'):
                    abort = True
                    break
                elif c == '%' or c in string.hexdigits:
                    expr += c
                last_c = c

            if not abort:
                self.js = self.js.replace(key + extra, urllib.unquote(expr))

                if start_js == self.js:
                    break
            else:
                start = offset

    def __gen_numbers(self):
        n = {'!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]': '9',
             '!+[]+!![]+!![]+!![]+!![]': '5', '!+[]+!![]+!![]+!![]': '4',
             '!+[]+!![]+!![]+!![]+!![]+!![]': '6', '!+[]+!![]': '2',
             '!+[]+!![]+!![]': '3', '(+![]+([]+[]))': '0', '(+[]+[])': '0',
             '(+!![]+[])': '1', '!+[]+!![]+!![]+!![]+!![]+!![]+!![]': '7',
             '!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]': '8', '+!![]': '1',
             '[+[]]': '[0]', '!+[]+!+[]': '2', '[+!+[]]': '[1]', '(+20)': '20',
             '[+!![]]': '[1]', '[+!+[]+[+[]]]': '[10]', '+(1+1)': '11'}

        for i in xrange(2, 20):
            key = '+!![]' * (i - 1)
            key = '!+[]' + key
            n['(' + key + ')'] = str(i)
            key += '+[]'
            n['(' + key + ')'] = str(i)
            n['[' + key + ']'] = '[' + str(i) + ']'

        for i in xrange(2, 10):
            key = '!+[]+' * (i - 1) + '!+[]'
            n['(' + key + ')'] = str(i)
            n['[' + key + ']'] = '[' + str(i) + ']'

            key = '!+[]' + '+!![]' * (i - 1)
            n['[' + key + ']'] = '[' + str(i) + ']'

        for i in xrange(0, 10):
            key = '(+(+!+[]+[%d]))' % (i)
            n[key] = str(i + 10)
            key = '[+!+[]+[%s]]' % (i)
            n[key] = '[' + str(i + 10) + ']'

        for tens in xrange(2, 10):
            for ones in xrange(0, 10):
                key = '!+[]+' * (tens) + '[%d]' % (ones)
                n['(' + key + ')'] = str(tens * 10 + ones)
                n['[' + key + ']'] = '[' + str(tens * 10 + ones) + ']'

        for hundreds in xrange(1, 10):
            for tens in xrange(0, 10):
                for ones in xrange(0, 10):
                    key = '+!+[]' * hundreds + '+[%d]+[%d]))' % (tens, ones)
                    if hundreds > 1: key = key[1:]
                    key = '(+(' + key
                    n[key] = str(hundreds * 100 + tens * 10 + ones)
        return n

    def to_base(n, base, digits="0123456789abcdefghijklmnopqrstuvwxyz"):
        n, base = int(n), int(base)
        if n < base:
            return digits[n]
        else:
            return to_base(n // base, base, digits).lstrip(digits[0]) + digits[n % base]

def unFuckFirst(data):
    try:
        #lib.common.log("JairoDemyst: " + data)
        p = 186
        hiro = re.findall(r'"hiro":"(.*?)"', data)[0]
        parts = re.findall('([^;]+)', hiro)
        for part in parts:
            if '(' in part:
                f = re.findall('(.*?)\((.+)\)',part)[0]
                exec(f[0] + JSUnfuck(f[1]).decode())
            else:
                exec(part)
        if isinstance(n, long):
            data = re.sub(r'"hiro":"(.*?)"', '"hiro":%s'%str(n), data, count=1)

        return data
    except:
        return data
