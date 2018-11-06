#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom 

# pas fini
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.player import cPlayer
from resources.lib.gui.hoster import cHosterGui


from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog, dialog

import re, urllib2, urllib, sys, requests, random, json, string
import xbmcplugin, xbmcvfs

SITE_IDENTIFIER = 'radio'
SITE_NAME = '[COLOR orange]Radio[/COLOR]'
SITE_DESC = 'Radio'

URL_RADIO = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/repo/resources/radio.m3u'


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
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showGenresRadio', addons.VSlang(30203) +' (Genres)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showAZRadio', addons.VSlang(30203) +' (A-Z)', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30203), 'music.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def parseWebM3U():#Traite les m3u
    playlist=[]
    song=track(None, None, None, None)

    file = "special://home/addons/plugin.video.vstream/resources/extra/radio.m3u"

    if not xbmcvfs.exists(file):
        return

    f = xbmcvfs.File(file, 'rb')
    sHtmlContent = f.read()
    f.close()


    line = re.compile('EXTINF:.+?,(.+?)\n(.+?)\n').findall(sHtmlContent)

    if line:
        total = len(line)

    for sTitle, sUrl2 in line:
        sUrl2 = sUrl2.replace('\r', '')

        song=track(None, sTitle, sUrl2, 'tv.png')
        playlist.append(song)

    print playlist
    return playlist

def showWeb():#Code qui s'occupe de liens TV du Web
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseWebM3U()
    print playlist

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

            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

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

def parseWebM3URegex(infile):#Ancien fonction pour traiter les m3u
    site= infile
    import xbmcvfs
    user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(site, headers=headers)
    file = "special://home/addons/plugin.video.vstream/resources/extra/radio.m3u"

    #if xbmcvfs.exists(file):

    f = xbmcvfs.File (file, 'w')
    inf = f.read()
    f.close()

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
