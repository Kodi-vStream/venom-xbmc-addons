# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom
import re
import string
import xbmc
import xbmcvfs

from resources.lib.comaddon import addon
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.player import cPlayer

SITE_IDENTIFIER = 'radio'
SITE_NAME = 'Radio'
SITE_DESC = 'Radio'

UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
headers = {'User-Agent': USER_AGENT, 'Accept': '*/*', 'Connection': 'keep-alive'}

icon = 'tv.png'
# sRootArt = cConfig().getRootArt()
sRootArt = 'special://home/addons/plugin.video.vstream/resources/art/tv'


class track:
    def __init__(self, location, title, image, ident):
        self.location = location
        self.title = title
        self.image = image
        self.ident = ident


def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30203), 'radio.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', addons.VSlang(30105), 'music.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showAZ', addons.VSlang(30111), 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = [['70', '70'], ['80', '80'], ['90', '90'], ['Clubbing', 'Clubbing'],
             ['Dance', 'Dance'], ['Electronic', 'Electronic'], ['Funk', 'Funk'], ['Hip-Hop', 'Hip-hop'],
             ['Hits', 'Hits'], ['Jazz', 'Jazz'], ['Lounge', 'Lounge'], ['Metal', 'Metal'],
             ['News', 'News'], ['Pop', 'Pop'], ['Rock', 'Rock'], ['Slow', 'Slow'], ['Trance', 'Trance']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sIdent in liste:
        oOutputParameterHandler.addParameter('siteUrl', '')
        oOutputParameterHandler.addParameter('ident', sIdent)
        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'music.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def parseWebM3U():  # Traite les m3u
    playlist = []
    # song = track(None, None, None, None)
    sFile = 'special://home/addons/plugin.video.vstream/resources/extra/radio.xspf'

    if not xbmcvfs.exists(sFile):
        return

    f = xbmcvfs.File(sFile, 'rb')
    sHtmlContent = f.read()
    f.close()

    line = re.compile('<location>([^<]+).+?title>([^<]+).+?image>([^<]+).+?identifier>([^<]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(sHtmlContent)

    if line:
        # total = len(line)

        for result in line:
            # sUrl2 = result[0].replace('\r', '')
            song = track(result[0], result[1], result[2], result[3])
            playlist.append(song)

    return playlist


def showWeb():  # Code qui s'occupe de liens TV du Web
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    playlist = parseWebM3U()

    if oInputParameterHandler.exist('AZ'):
        sAZ = oInputParameterHandler.getValue('AZ')
        string = filter(lambda t: t.title.strip().capitalize().startswith(sAZ), playlist)
        playlist = sorted(string, key=lambda t: t.title.strip().capitalize())
    elif oInputParameterHandler.exist('ident'):
        sIdent = oInputParameterHandler.getValue('ident')
        string = filter(lambda t: t.ident.strip().capitalize().startswith(sIdent), playlist)
        playlist = sorted(string, key=lambda t: t.ident.strip().capitalize())
    else:
        playlist = sorted(playlist, key=lambda t: t.title.strip().capitalize())

    if not playlist:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun résultat[/COLOR] ')
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for track in playlist:
            sThumb = track.image
            if not sThumb:
                sThumb = 'music.png'

            oOutputParameterHandler.addParameter('siteUrl', track.location)
            oOutputParameterHandler.addParameter('sMovieTitle', track.title)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setTitle(track.title)
            oGuiElement.setFileName(track.title)
            oGuiElement.setIcon('music.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            oGui.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAZ():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for i in string.digits:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showWeb', i, 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    for i in string.ascii_uppercase:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showWeb', i, 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def play__():  # Lancer les liens
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    # Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    if 'f4mTester' in sUrl:
        xbmc.executebuiltin('XBMC.RunPlugin(' + sUrl + ')')
        return
    else:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sTitle)
        sUrl = sUrl.replace(' ', '%20')
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        # tout répéter
        xbmc.executebuiltin('xbmc.playercontrol(RepeatAll)')

        oPlayer.startPlayer()
        return


def GetRealUrl(chain):  # Récupère les liens des regex

    UA2 = UA
    url = chain
    regex = ''
    sHtmlContent = ''

    r = re.search('\[[REGEX]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        regex = r.group(1)

    r = re.search('\[[UA]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        UA2 = r.group(1)

    r = re.search('\[[URL]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = r.group(1)

    # post methode ?
    r = re.search('\[[POSTFORM]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        param = r.group(1)
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'identity')
        oRequestHandler.addParametersLine(param)
        sHtmlContent = oRequestHandler.request()

    else:
        if url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

    if regex:
        oParser = cParser()
        aResult2 = oParser.parse(sHtmlContent, regex)
        if aResult2:
            url = aResult2[1][0]

    url = url + '|User-Agent=' + UA2

    return url
