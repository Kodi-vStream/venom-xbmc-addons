# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import string

from resources.lib.comaddon import progress, addon, dialog, siteManager
from resources.lib.enregistrement import cEnregistremement
from resources.lib.epg import cePg
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Unquote

SITE_IDENTIFIER = 'freebox'
SITE_NAME = 'Free Télévision/Radio'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_WEB = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/Beta/repo/resources/webtv2.m3u'
URL_RADIO = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/repo/resources/radio.m3u'

TV_TV = (True, 'showMenuTV')
CHAINE_TV = (URL_WEB, 'showWeb')


UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

icon = 'tv.png'
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
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', addons.VSlang(30115), 'tv.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMusic', addons.VSlang(30137), 'music.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMenuTV():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_WEB)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30332), 'tv.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMenuMusic():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir('radio', 'showWeb', addons.VSlang(30203), 'music.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('radio', 'showGenres', addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir('radio', 'showAZ', addons.VSlang(30111), 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def parseM3U(sUrl=None):  # Traite les m3u local
    
    if not sUrl:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    inf = oRequestHandler.request().split('\n')

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

        elif len(line) != 0:
            if ValidEntry and (not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path = line
                playlist.append(song)
                song = track(None, None, None, None)

    return playlist


def showWeb():  # Code qui s'occupe de liens TV du Web
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sUrl == 'TV':
        sUrl = URL_WEB
    elif sUrl == 'RADIO':
        sUrl = URL_RADIO

    playlist = parseM3U(sUrl=sUrl)

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
        cEpg = cePg()
        EPG = cEpg.getEpg('', 'direct',noTextBox=True)

        total = len(playlist)
        progress_ = progress().VScreate(SITE_NAME)
        for track in playlist:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sThumb = track.icon
            if not sThumb:
                sThumb = 'tv.png'

            channelName = track.title.replace('sport','sports').replace('(en clair)','')
            sDesc = cEpg.getChannelEpg(EPG, channelName)

            # les + ne peuvent pas passer
            url2 = track.path.replace('+', 'P_L_U_S')

            thumb = '/'.join([sRootArt, sThumb])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url2)
            oOutputParameterHandler.addParameter('sMovieTitle', track.title)
            oOutputParameterHandler.addParameter('sThumbnail', thumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('EpgData', EPG)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setDescription(sDesc)
            oGuiElement.setTitle(track.title)
            oGuiElement.setFileName(track.title)
            
            oGuiElement.setIcon('tv.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(thumb)
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
            # oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def direct_epg():  # Code qui gerent l'epg
    # oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    # aParams = oInputParameterHandler.getAllParameter()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    text = oInputParameterHandler.getValue('EpgData')
    cePg().view_epg(sTitle, 'direct', text=text)


def soir_epg():  # Code qui gerent l'epg
    # oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    cePg().view_epg(sTitle, 'soir')


def enregistrement():  # Code qui gerent l'enregistrement
    # oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')

    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        dialog().VSok('Merci d\'activer l\'enregistrement dans les options')
        return

    if '[' in sUrl and ']' in sUrl:
        sUrl = getRealUrl(sUrl)

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

    if aResult[0]:
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

            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
            # oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
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
        sUrl = getRealUrl(sUrl)

    # Bug specifique au flux france TV
    # eof detectedL
    if 'ftven.fr' in sUrl:
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

        if oHoster:
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sUrl, sThumbnail)

        oGui.setEndOfDirectory()


"""
Fonction diverse:
#   - getRealUrl = Regex pour Iptv(Officiel)
#   - showDailymotionStream = Lis les liens de streaming de Daylimotion qui sont speciaux
#   - getBrightcoveKey = Recupere le token pour les liens proteger par Brightcove (RMC Decouvert par exemple)
"""


def getRealUrl(chain):
    oParser = cParser()

    UA2 = UA
    url = chain
    regex = ''
    param = ""
    head = None

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

    r = re.search('\[[HEAD]+\](.+?)(?:(?:\[[A-Z]+\])|$)',chain)
    if r:
        head = r.group(1)

    # post metehod ?
    r = re.search('\[[POSTFORM]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        param = r.group(1)

    oRequestHandler = cRequestHandler(url)
    if param:
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'identity')
        oRequestHandler.addParametersLine(param)
    if head:
        import json
        head = json.loads(head)
        for a in head:
            oRequestHandler.addHeaderEntry(a,head[a])
    sHtmlContent = oRequestHandler.request()

    if regex:
        aResult2 = oParser.parse(sHtmlContent, regex)
        if aResult2:
            url = aResult2[1][0]

    url = url + '|User-Agent=' + UA2

    return url


def decodeNrj(d):
    oRequestHandler = cRequestHandler(d)
    sHtmlContent = oRequestHandler.request()

    title = re.search('data-program_title="([^"]+)"', sHtmlContent).group(1)
    ids = re.search('data-ref="([^"]+)"', sHtmlContent).group(1)

    url = 'https://www.nrj-play.fr/compte/live?channel=' + d.split('/')[3] + '&channel=' + d.split('/')[3] + '&title='
    url += title + '&channel=' + d.split('/')[3] + '&ref=' + ids + '&formId=formDirect'

    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    dataUrl = re.search('"contentUrl" content="([^"]+)"', sHtmlContent).group(1)

    return dataUrl


def getBrightcoveKey(sUrl):
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "rmcdecouverte" in sUrl:
        url = re.search('<script type="application/javascript" src="([^"]+)"></script>', sHtmlContent).group(1)

        oRequestHandler = cRequestHandler("https://" + sUrl.split('/')[2] + url)
        sHtmlContent = oRequestHandler.request()
        result = re.search('N="([^"]+)",y="([^"]+)"\)', sHtmlContent)
        player = result.group(1)
        video = result.group(2)

        oRequestHandler = cRequestHandler("https://static.bfmtv.com/ressources/next-player/cleo-player/playerBridge.js")
        sHtmlContent = oRequestHandler.request().lower()

        ID = sUrl.split('/')[2].split('.')[0]
        account = re.search("\n(.+?): '" + ID + "'", sHtmlContent).group(1).replace('            ', '')

    else:
        result = re.search('<div class="video_block" id="video_player_.+?" accountid="([^"]+)" playerid="([^"]+)" videoid="([^"]+)"', sHtmlContent)

        account = result.group(1)
        player = result.group(2)
        video = result.group(3)

    url = 'http://players.brightcove.net/%s/%s_default/index.min.js' % (account, player)
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    policyKey = re.search('policyKey:"(.+?)"', sHtmlContent).group(1)

    url = "https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s" % (account, video)
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Accept', "application/json;pk=" + policyKey)
    sHtmlContent = oRequestHandler.request()
    url = re.search('"sources":.+?src":"([^"]+)"', sHtmlContent).group(1)

    return url
