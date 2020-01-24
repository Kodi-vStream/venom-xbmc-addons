#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom 
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.player import cPlayer
from resources.lib.gui.hoster import cHosterGui


from resources.lib.comaddon import progress, addon, xbmc

import re, random, string
import xbmcplugin, xbmcvfs

SITE_IDENTIFIER = 'radio'
SITE_NAME = '[COLOR orange]Radio[/COLOR]'
SITE_DESC = 'Radio'

UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}

icon = 'tv.png'
#/home/lordvenom/.kodi/
#sRootArt = cConfig().getRootArt()
sRootArt = "special://home/addons/plugin.video.vstream.dev/resources/art/tv"
ADDON = addon()

class track():
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
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', addons.VSlang(30203) +' (Genres)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showAZ', addons.VSlang(30203) +' (A-Z)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30203), 'music.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['70', '70'] )
    liste.append( ['80', '80'] )
    liste.append( ['90', '90'] )
    liste.append( ['Classic', 'Classic'] )
    liste.append( ['Clubbing', 'Clubbing'] )
    liste.append( ['Dance', 'Dance'] )
    liste.append( ['Electronic', 'Electronic'] )
    liste.append( ['Funk', 'Funk'] )
    liste.append( ['Hip-Hop', 'Hip-Hop'] )
    liste.append( ['Hits', 'Hits'] )
    liste.append( ['Jazz', 'Jazz'] )
    liste.append( ['Lounge', 'Lounge'] )
    liste.append( ['Love', 'Love'] )
    liste.append( ['Metal', 'Metal'] )
    liste.append( ['News', 'News'] )
    liste.append( ['Pop', 'Pop'] )
    liste.append( ['Rock', 'Rock'] )
    liste.append( ['Slow', 'Slow'] )
    liste.append( ['Trance', 'Trance'] )

    for sTitle, sIdent in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', '')
        oOutputParameterHandler.addParameter('ident', sIdent)
        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def parseWebM3U():#Traite les m3u
    playlist=[]
    song=track(None, None, None, None)

    file = "special://home/addons/plugin.video.vstream.dev/resources/extra/radio.xspf"

    if not xbmcvfs.exists(file):
        return

    f = xbmcvfs.File(file, 'rb')
    sHtmlContent = f.read()
    f.close()


    line = re.compile('<location>(.+?)<.+?<title>(.+?)<.+?<image>(.+?)<.+?<identifier>(.+?)<', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(sHtmlContent)

    if line:
        total = len(line)

        for result in line:
            #sUrl2 = result[0].replace('\r', '')
            song=track(result[0], result[1], result[2], result[3])
            playlist.append(song)

    return playlist

def showWeb():#Code qui s'occupe de liens TV du Web
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseWebM3U()

    if (oInputParameterHandler.exist('AZ')):
        sAZ = oInputParameterHandler.getValue('AZ')
        string = filter(lambda t: t.title.strip().capitalize().startswith(sAZ), playlist)
        playlist = sorted(string, key=lambda t: t.title.strip().capitalize())
    elif (oInputParameterHandler.exist('ident')):
        sIdent = oInputParameterHandler.getValue('ident')
        string = filter(lambda t: t.ident.strip().capitalize().startswith(sIdent), playlist)
        playlist = sorted(string, key=lambda t: t.ident.strip().capitalize())
    else :
        playlist = sorted(playlist, key=lambda t: t.title.strip().capitalize())

    if not playlist:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]Aucun résultat[/COLOR] ")

    else:
        for track in playlist:
            sThumb = track.image
            if not sThumb:
                sThumb = 'tv.png'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', track.location)
            oOutputParameterHandler.addParameter('sMovieTitle', track.title)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            #oGui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt + '/tv/' + sThumb, oOutputParameterHandler)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setTitle(track.title)
            oGuiElement.setFileName(track.title)
            oGuiElement.setIcon('tv.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAZ():

    import string
    oGui = cGui()
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
