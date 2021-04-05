# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import io
import re
import string
import sys
from zipfile import ZipFile

import xbmc
import xbmcplugin
import xbmcvfs

from resources.lib.comaddon import progress, addon, dialog
from resources.lib.enregistrement import cEnregistremement
from resources.lib.epg import cePg
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Unquote, Quote, QuotePlus

SITE_IDENTIFIER = 'freebox'
SITE_NAME = '[COLOR orange]Télévision Direct/Stream[/COLOR]'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'http://mafreebox.freebox.fr/freeboxtv/playlist.m3u'
URL_WEB = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/Beta/repo/resources/webtv2.m3u'
URL_RADIO = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/repo/resources/radio.m3u'

MOVIE_IPTVSITE = (True, 'showIptvSite')

UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

headers = {'User-Agent': UA, 'Accept': '*/*', 'Connection': 'keep-alive'}

icon = 'tv.png'
# /home/lordvenom/.kodi/
# sRootArt = cConfig().getRootArt()
sRootArt = 'special://home/addons/plugin.video.vstream/resources/art/tv'
ADDON = addon()


class track:
    def __init__(self, length, title, path, icon, data=''):
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

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_IPTVSITE)
    oGui.addDir(SITE_IDENTIFIER, 'showIptvSite', 'TV (Sources)', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir('radio', 'showWeb', addons.VSlang(30203), 'music.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('radio', 'showGenres', addons.VSlang(30203) + ' (Genres)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir('radio', 'showAZ', addons.VSlang(30203) + ' (A-Z)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('lsdb', 'load', 'Liveset Database', 'music.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showIptvSite():
    oGui = cGui()

    # test f4mTester
    sPath = 'special://home/addons/plugin.video.f4mTester/default.py'

    if not xbmcvfs.exists(sPath) and not xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]plugin.video.f4mTester: L'addon n'est pas présent[/COLOR]")

    liste = []
    # liste.append(['IptvGratuit', 'iptv_gratuit'])
    # liste.append(['IptvSource', 'iptv_source'])
    # liste.append(['Iptv4Sat', 'iptv_four_sat'])
    # liste.append(['Daily Iptv List', 'daily_iptv_list'])
    # liste.append(['Extinf', 'iptv'])
    liste.append(['ChannelStream', 'channelstream'])
    liste.append(['Streamonsport', 'streamonsport'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, fName in liste:
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(fName, 'load', sTitle, 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getHtml(sUrl, data=None):  # S'occupe des requetes
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    data = oRequestHandler.request()
    return data


def parseM3U(sUrl=None, infile=None):  # Traite les m3u local
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if infile is None:
        if 'iptv4sat' in sUrl or '.zip' in sUrl:
            sHtmlContent = getHtml(sUrl)
            zip_files = ZipFile(io.BytesIO(sHtmlContent))
            files = zip_files.namelist()

            oOutputParameterHandler = cOutputParameterHandler()
            for Title in files:
                oOutputParameterHandler.addParameter('sMovieTitle', Title)
                oOutputParameterHandler.addParameter('siteUrl', sUrl)

                oGui.addDir(SITE_IDENTIFIER, 'unZip', Title, 'tv.png', oOutputParameterHandler)

            oGui.setEndOfDirectory()
            return

        elif '#EXTM3U' not in sUrl:

            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            inf = oRequestHandler.request()

            if 'drive.google' in inf:
                inf = unGoogleDrive(inf)

            inf = inf.split('\n')
        else:
            inf = infile

    else:
        inf = infile

    try:
        line = inf.readline()  # Local variable 'line' value is not used ??
    except:
        pass

    playlist = []
    song = track(None, None, None, None)
    ValidEntry = False

    for line in inf:
        if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
            try:
                line = line.decode('utf-8')
            except AttributeError:
                pass

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
            if ValidEntry and (not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path = line
                playlist.append(song)
                song = track(None, None, None, None)

    try:
        inf.close()
    except:
        pass

    return playlist


def showWeb(infile=None):  # Code qui s'occupe de liens TV du Web
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    if infile is None:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        playlist = parseM3U(sUrl=sUrl)
    else:
        playlist = parseM3U(infile=infile)

    if oInputParameterHandler.exist('AZ'):
        sAZ = oInputParameterHandler.getValue('AZ')
        string = filter(lambda t: t.title.strip().capitalize().startswith(sAZ), playlist)
        playlist = sorted(string, key=lambda t: t.title.strip().capitalize())
    else:
        playlist = sorted(playlist, key=lambda t: t.title.strip().capitalize())

    if not playlist:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Problème de lecture avec la playlist[/COLOR]')

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
            if not xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                if '[' not in url2 and ']' not in url2 and '.m3u8' not in url2 and 'dailymotion' not in url2:
                    url2 = 'plugin://plugin.video.f4mTester/?url=' + QuotePlus(url2)
                    url2 += '&amp;streamtype=TSDOWNLOADER&name=' + Quote(track.title)

            thumb = '/'.join([sRootArt, sThumb])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url2)
            oOutputParameterHandler.addParameter('sMovieTitle', track.title)
            oOutputParameterHandler.addParameter('sThumbnail', thumb)

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


def direct_epg():  # Code qui gerent l'epg
    # oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    # aParams = oInputParameterHandler.getAllParameter()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    cePg().view_epg(sTitle, 'direct')


def soir_epg():  # Code qui gerent l'epg
    # oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    cePg().view_epg(sTitle, 'soir')


def enregistrement():  # Code qui gerent l'epg
    # oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')

    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        dialog().VSok('Merci d\'activer l\'enregistrement dans les options')
        return

    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    if 'plugin' in sUrl:
        url = re.findall('url=(.+?)&amp', ''.join(sUrl))
        sUrl = Unquote(url[0])
    cEnregistremement().programmation_enregistrement(sUrl)


def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for i in string.digits:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showTV', i, 'az.png', oOutputParameterHandler)

    for i in string.ascii_uppercase:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showTV', i, 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAZRadio():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for i in string.digits:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showWeb', i, 'az.png', oOutputParameterHandler)

    for i in string.ascii_uppercase:
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
    sPattern = '<title>(.+?)</title><link>(.+?)</link>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        progress_ = progress().VScreate(SITE_NAME)

        # affiche par
        if oInputParameterHandler.exist('AZ'):
            sAZ = oInputParameterHandler.getValue('AZ')
            string = filter(lambda t: t[0].strip().capitalize().startswith(sAZ), aResult[1])
            string = sorted(string, key=lambda t: t[0].strip().capitalize())
        else:
            string = sorted(aResult[1], key=lambda t: t[0].strip().capitalize())

        total = len(string)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in string:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

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

            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
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
    sDesc = oInputParameterHandler.getValue('sDesc')

    # Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)
    elif not xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
        stype = ''
        if '.ts' in sUrl:
            stype = 'TSDOWNLOADER'
        elif '.m3u' in sUrl:
            pass
        if stype:
            from F4mProxy import f4mProxyHelper
            f4mp = f4mProxyHelper()
            xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
            f4mp.playF4mLink(sUrl, sTitle, proxy=None, use_proxy_for_chunks=False, maxbitrate=0, simpleDownloader=True
                                 , auth=None, streamtype=stype, setResolved=True, swf=None, callbackpath=''
                                 , callbackparam='', iconImage=sThumbnail)
            return

    if 'f4mTester' in sUrl:
        xbmc.executebuiltin('XBMC.RunPlugin(' + sUrl + ')')
        return

    # Bug specifique au flux france TV
    # eof detectedL
    elif 'ftven.fr' in sUrl:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sTitle)
        sUrl = sUrl.replace(' ', '%20')
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)

        from resources.lib.player import cPlayer
        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()

    else:
        oHoster = cHosterGui().checkHoster(sUrl)

        if (oHoster != False):
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sUrl, sThumbnail)

        oGui.setEndOfDirectory()


"""
Fonction diverse:
#   - GetRealUrl = Regex pour Iptv(Officiel)
#   - DecodeEmail = Decode les email coder par Cloudflare pour extinf
#   - unZip = Extrait les un fichier specific dans une archive zip
#   - unGoogleDrive = Recupere le fichier video quand il est heberger sur GoogleDrive
#   - showDailymotionStream = Lis les liens de streaming de Daylimotion qui sont speciaux
#   - getBrightcoveKey = Recupere le token pour les liens proteger par Brightcove (RMC Decouvert par exemple)
"""


def GetRealUrl(chain):
    oParser = cParser()

    UA2 = UA
    url = chain
    regex = ''

    r = re.search('\[[DECODENRJ]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = decodeNrj(r.group(1))

    r = re.search('\[[BRIGHTCOVEKEY]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = getBrightcoveKey(r.group(1))

    r = re.search('\[[REGEX]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        regex = r.group(1)

    r = re.search('\[[UA]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        UA2 = r.group(1)

    r = re.search('\[[URL]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = r.group(1)

    # post metehod ?
    r = re.search('\[[POSTFORM]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        param = r.group(1)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'identity')
        oRequestHandler.addParametersLine(param)
        sHtmlContent = oRequestHandler.request()

    else:
        oRequestHandler = cRequestHandler(url)
        sHtmlContent = oRequestHandler.request()

    if regex:
        aResult2 = oParser.parse(sHtmlContent, regex)
        if aResult2:
            url = aResult2[1][0]

    url = url + '|User-Agent=' + UA2

    return url


def openwindows():
    xbmc.executebuiltin('ActivateWindow(%d, return)' % 10601)
    return


def decodeNrj(d):
    oRequestHandler = cRequestHandler(d)
    sHtmlContent = oRequestHandler.request()

    title = re.search('<div data-title="([^"]+)"', sHtmlContent).group(1)
    ids = re.search('data-ref="([^"]+)"', sHtmlContent).group(1)

    url = 'https://www.nrj-play.fr/compte/live?channel=' + d.split('/')[3] + '&title=' + title + '&channel='
    url += d.split('/')[3] + '&ref=' + ids + '&formId=formDirect'

    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    dataUrl = re.search('"contentUrl" content="([^"]+)"', sHtmlContent).group(1)

    return dataUrl


def decodeEmail(e):
    head, e = e.split('a href=')
    e, rest = e.split('</a>')
    e = re.search('data-cfemail="(.+?)"', e).group(1)
    de = ''
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16) ^ k)

    return head + str(de) + rest


def unZip():
    oInputParameterHandler = cInputParameterHandler()
    Title = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    zip_files = ZipFile(io.BytesIO(sHtmlContent))
    files = zip_files.namelist()
    pos = files.index(Title)
    with zip_files.open(files[pos]) as f:
        sHtmlContent = []
        for line in f:
            sHtmlContent.append(line)
        inf = sHtmlContent

    showWeb(inf)


def unGoogleDrive (infile):
    ids = re.findall('<a href="https://drive.google.com/file/d/([^"]+)/view', infile)[0]
    url = 'https://drive.google.com/uc?id=' + ids + '&export=download'
    inf = getHtml(url)

    return inf


def getBrightcoveKey(sUrl):
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "rmcdecouverte" in sUrl:
        result = re.search('data-account="(.+?)" data-player="(.+?)".+?data-video-id="(.+?)"', sHtmlContent)
    else:
        result = re.search('<div class="video_block" id="video_player_.+?" accountid="([^"]+)" playerid="([^"]+)" videoid="([^"]+)"', sHtmlContent)

    account = result.group(1)
    player = result.group(2)
    video = result.group(3)

    url = 'http://players.brightcove.net/%s/%s_default/index.min.js' % (account, player)

    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    policyKey = re.search('policyKey:"(.+?)"', sHtmlContent).group(1)

    url = "https://edge.api.brightcove.com/playback/v1/accounts/" + account + "/videos/" + video
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Accept', "application/json;pk=" + policyKey)
    sHtmlContent = oRequestHandler.request()
    url = re.search('"sources":.+?src":"([^"]+)"', sHtmlContent).group(1)

    return url
