#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.player import cPlayer
from resources.lib.config import cConfig
from resources.lib.epg import cePg

import re, urllib2, urllib, os, time, unicodedata
import xbmc, xbmcgui

SITE_IDENTIFIER = 'freebox'
SITE_NAME = '[COLOR orange]Télévision Direct / Stream[/COLOR]'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'http://mafreebox.freebox.fr/freeboxtv/playlist.m3u'
URL_WEB = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/Beta/repo/resources/webtv2.m3u'
URL_RADIO = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/repo/resources/radio.m3u'

UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

icon = 'tv.png'
sRootArt = cConfig().getRootArt()

class track():
    def __init__(self, length, title, path, icon,data=''):
        self.length = length
        self.title = title
        self.path = path
        self.icon = icon
        self.data = data


def load():
    linktv = cConfig().getSetting('pvr-view')
    oGui = cGui()
    oConfig = cConfig()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_WEB)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', oConfig.getlanguage(30332), 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showAZRadio', oConfig.getlanguage(30203)+' (A-Z)', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_RADIO)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', oConfig.getlanguage(30203), 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showWeb():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseWebM3U(sUrl)

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

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url2)
            oOutputParameterHandler.addParameter('sMovieTitle', str(track.title))
            oOutputParameterHandler.addParameter('sThumbnail', str(sRootArt + '/tv/' + sThumb))

            #oGui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt+'/tv/'+sThumb, oOutputParameterHandler)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('play__')
            oGuiElement.setTitle(track.title)
            oGuiElement.setFileName(track.title)
            oGuiElement.setIcon('tv.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(sRootArt+'/tv/'+sThumb)
            oGuiElement.setDirectTvFanart()
            oGuiElement.setCat(6)

            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,SITE_IDENTIFIER,SITE_IDENTIFIER,'direct_epg','Guide tv Direct')
            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,SITE_IDENTIFIER,SITE_IDENTIFIER,'soir_epg','Guide tv Soir')
            oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def direct_epg():
    oGuiElement = cGuiElement()
    oInputParameterHandler = cInputParameterHandler()
    #aParams = oInputParameterHandler.getAllParameter()
    #print aParams
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sCom = cePg().get_epg(sTitle,'direct')

def soir_epg():
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
        dialog = cConfig().createDialog(SITE_NAME)

        #affiche par
        if (oInputParameterHandler.exist('AZ')):
            sAZ = oInputParameterHandler.getValue('AZ')
            string = filter(lambda t: t[0].strip().capitalize().startswith(sAZ), aResult[1])
            string = sorted(string, key=lambda t: t[0].strip().capitalize())
        else :
            string = sorted(aResult[1], key=lambda t: t[0].strip().capitalize())

        total = len(string)
        for aEntry in string:
            cConfig().updateDialog(dialog, total)

            if dialog.iscanceled():
                break

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[0])
            oOutputParameterHandler.addParameter('sThumbnail', str('tv.png'))
            oOutputParameterHandler.addParameter('sThumbnail', str(sRootArt + '/tv.png'))

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

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

# def showLibretv():
    # oGui = cGui()

    # oInputParameterHandler = cInputParameterHandler()
    # sUrl = oInputParameterHandler.getValue('siteUrl')

    # playlist = parseLibretvM3U(sUrl)

    # for track in playlist:

        # sTitle = track.title
        # sTitle = unicode(sTitle, 'latin-1')#converti en unicode
        # sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
        # sTitle = sTitle.encode( "utf-8")

        # try:
            # sTitle = urllib.unquote_plus(sTitle)
        # except:

            # sTitle = 'none'

        # sthumb = str(track.icon)
        # if len(sthumb) > 0:
            # sthumb = 'http://libretv.me/icon/' + sthumb
        # else:
            # sthumb = 'http://libretv.me/icon/libretv.png'

        # sData = str(track.data)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', str(track.path))
        # oOutputParameterHandler.addParameter('sMovieTitle', str(track.title))
        # oOutputParameterHandler.addParameter('sThumbnail', sthumb)

        # #garbage
        # if 'http://touski' in track.path or re.search('[0-9]\.[0-9]\.[0-9].[0-9]', track.path):
            # oGui.addText(SITE_IDENTIFIER, sTitle, oOutputParameterHandler)
        # #real stream
        # elif 'rtmp' in track.path or 'm3u8' in track.path:
            # oGui.addDirectTV(SITE_IDENTIFIER, 'play__', sTitle, sthumb, sthumb, oOutputParameterHandler)
        # #folder
        # elif '.m3u' in track.path :
            # oGui.addDirectTV(SITE_IDENTIFIER, 'showLibretv', sTitle, sthumb, sthumb, oOutputParameterHandler)
        # #unknow link, loaded as normal stream
        # else:
            # oGui.addDirectTV(SITE_IDENTIFIER, 'play__', sTitle, sthumb, sthumb, oOutputParameterHandler)

    # oGui.setEndOfDirectory()

# import code https://github.com/dvndrsn/M3uParser #
# David Anderson code thanck's for good job #

def parseWebM3U(infile):
    inf = urllib.urlopen(infile)

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

def parseM3U(infile):
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


#http://libretv.me/Liste-m3u/Liste-anonymes/(PB)Marchannel.m3u
def parseLibretvM3U(infile):

    #print infile

    #version normale
    inf = urllib.urlopen(infile)

    #version qui memorise les m3u
    #file = GetLibreTVFile(infile)
    #inf = open(file, "r")

    line = inf.readline()

    playlist=[]

    #if not (line.startswith('#EXTM3U') or line.startswith('#EXTINF:')):
    #    return playlist

    song=track(None,None,None,None)

    ValidEntry = False

    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):

            m = re.search(',([^,]+?)$', line)
            if m:
                title = m.groups(1)[0]
                length = 0

                ValidEntry = True

                m = re.search('tvg-logo="(.+?)"', line)
                if m:
                    logo = m.groups(1)[0]
                else:
                    logo = ''

                m = re.search('group-title="(.+?)"', line)
                if m:
                    data = m.groups(1)[0]
                else:
                    data = None

                song=track(length,title,None,logo,data)
        elif (len(line) != 0):
            if (not line.startswith('#') and ValidEntry):
                ValidEntry = False
                song.path=line
                playlist.append(song)
                song=track(None,None,None,None)

    inf.close()
    return playlist


def play__():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S','+')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #Special url with tag
    if '[' in sUrl and ']' in sUrl:
        sUrl = GetRealUrl(sUrl)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sTitle)
    sUrl = sUrl.replace(' ','%20')
    oGuiElement.setMediaUrl(sUrl)
    oGuiElement.setThumbnail(sThumbnail)

    #cConfig().log("Hoster - play " + str(sTitle))
    oPlayer = cPlayer()
    oPlayer.clearPlayList()
    oPlayer.addItemToPlaylist(oGuiElement)
    #tout repetter
    #xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")

    oPlayer.startPlayer()
    return

    oGui.setEndOfDirectory()

def GetRealUrl(chain):

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
