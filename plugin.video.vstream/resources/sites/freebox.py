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
import re, urllib2, urllib, os
import xbmc, xbmcgui

SITE_IDENTIFIER = 'freebox'
SITE_NAME = 'Télévision Direct / Stream'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'http://mafreebox.freebox.fr/freeboxtv/playlist.m3u'
URL_FREE = 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/repo/resources/freetv.m3u'
URL_ORANGE = 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/repo/resources/orangetv.m3u'
URL_SFR = 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/repo/resources/sfrtv.m3u'
URL_WEB = 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/repo/resources/webtv2.m3u'
URL_BG = 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/repo/resources/bouygues.m3u'

URL_LIBRETV = 'http://kodi.libretv.me/Libretv.m3u'

#URL_LIBRETV = 'http://libretv.me/Liste-m3u/Liste-anonymes/(PB)Redeneobux(USA).m3u'


icon = 'tv.png'        
sRootArt = cConfig().getRootArt()

class track():
    def __init__(self, length, title, path, icon):
        self.length = length
        self.title = title
        self.path = path
        self.icon = icon


def load():
    linktv = cConfig().getSetting('pvr-view')
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'load', '[COLOR khaki]Pour lire les chaînes BOX vous devez être chez l\'Opérateur (Si des chaînes ne fonctionnent pas, vous n\'avez peux être pas le bouquet nécessaire[/COLOR]', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_FREE)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', 'Free TV', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SFR)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', 'Sfr TV', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_ORANGE)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', 'Orange TV', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_BG)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', 'Bouygues TV', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_WEB)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', 'Tv du web', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'load', '[COLOR khaki]Tu veux voir ta chaîne sur Libretv.me alors partage ta chaîne![/COLOR]', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_LIBRETV)
    oGui.addDir(SITE_IDENTIFIER, 'showLibretv', 'Libretv.me', 'tv.png', oOutputParameterHandler)

    if (linktv != 'false'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'openwindows', 'Tv direct', 'tv.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()



def showBox():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseM3U(sUrl)

    for track in playlist:
           
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', str(track.path))
        oOutputParameterHandler.addParameter('siteTitle', str(track.title))
        oGui.addDir(SITE_IDENTIFIER, 'play', track.title, 'tv.png', oOutputParameterHandler)
    
  
    oGui.setEndOfDirectory()

def showWeb():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseWebM3U(sUrl)

    for track in playlist:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', str(track.path))
        oOutputParameterHandler.addParameter('siteTitle', str(track.title))
        oOutputParameterHandler.addParameter('sThumbnail', str(sRootArt+'/tv/'+track.icon))
        oGui.addDirectTV(SITE_IDENTIFIER, 'play', track.title, 'tv.png' , sRootArt+'/tv/'+track.icon, oOutputParameterHandler)    
  
    oGui.setEndOfDirectory()
    
def showLibretv():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseLivretvM3U(sUrl)

    for track in playlist:
        #sTitle = unicodedata.normalize('NFKD', str(track.title)).encode('ascii','ignore')
        try: 
            sTitle = urllib.unquote_plus(track.title)
        except:
            sTitle = 'none'
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', str(track.path))
        oOutputParameterHandler.addParameter('siteTitle', str(track.title))
        oOutputParameterHandler.addParameter('sThumbnail', 'none')
        if 'rtmp' in track.path or 'm3u8' in track.path:
            oGui.addDirectTV(SITE_IDENTIFIER, 'play', sTitle, 'tv.png', '', oOutputParameterHandler)   
            
        else : 
            oGui.addDirectTV(SITE_IDENTIFIER, 'showLibretv', sTitle, 'tv.png', '', oOutputParameterHandler)    
  
    oGui.setEndOfDirectory()

# import code https://github.com/dvndrsn/M3uParser #
# David Anderson code thanck's for good job #

def parseWebM3U(infile):
    inf = urllib.urlopen(infile)

    line = inf.readline()

    if not line.startswith('#EXTM3U'):
       return

    playlist=[]
    song=track(None,None,None,None)

    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            length,title=line.split('#EXTINF:')[1].split(',',1)
            try:
                licon = line.split('#EXTINF:')[1].partition('tvg-logo=')[2]
                icon = licon.split('"')[1]
            except:
                icon = "tv.png"
            song=track(length,title,None,icon)
        elif (len(line) != 0):
            if not line.startswith('!'):
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

    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            length,title=line.split('#EXTINF:')[1].split(',',1)
            song=track(length,title,None,None)
        elif (len(line) != 0):
            if not line.startswith('!'):
                song.path=line
                playlist.append(song)
                song=track(None,None,None,None)

    inf.close()

    return playlist
    
def parseLivretvM3U(infile):
    
    
    inf = urllib.urlopen(infile)

    line = inf.readline()

    # if not line.startswith('#EXTM3U'):
        # return

    playlist=[]
    song=track(None,None,None,None)
 
    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            length,title=line.split('#EXTINF:')[1].split(',',1)
            song=track(length,title,None,None)
        elif (len(line) != 0):
            if not line.startswith('#'):
                song.path=line
                playlist.append(song)
                song=track(None,None,None,None)

    inf.close()
    return playlist
    
    
def play():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('siteTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sTitle)
    oGuiElement.setMediaUrl(sUrl)
    oGuiElement.setThumbnail(sThumbnail)

    oPlayer = cPlayer()
    oPlayer.clearPlayList()
    oPlayer.addItemToPlaylist(oGuiElement)
    oPlayer.startPlayer()
    return
        
    oGui.setEndOfDirectory()

def openwindows():
    xbmc.executebuiltin( "ActivateWindow(%d, return)" % ( 10601, ) )
    return
    