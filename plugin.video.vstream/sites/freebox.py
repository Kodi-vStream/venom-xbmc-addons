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
import re, urllib2, os

SITE_IDENTIFIER = 'freebox'
SITE_NAME = 'Freebox'
SITE_DESC = 'Regarder la télévision freebox | Uniquement pour les abonnés free'

URL_MAIN = 'http://mafreebox.freebox.fr/freeboxtv/playlist.m3u'
URL_FREE = os.path.join(cConfig().getAddonPath(),'resources/playlist/freetv.m3u')
URL_ORANGE = os.path.join(cConfig().getAddonPath(),'resources/playlist/orangetv.m3u')
URL_SFR = os.path.join(cConfig().getAddonPath(),'resources/playlist/sfrtv.m3u')


class track():
    def __init__(self, length, title, path):
        self.length = length
        self.title = title
        self.path = path

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'load', '[COLOR khaki]Pour lire les chaînes vous devez être chez l\'Opérateur (Si des chaînes ne fonctionnent pas, vous n\'avez peux être pas le bouquet nécessaire[/COLOR]', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_FREE)
    oGui.addDir(SITE_IDENTIFIER, 'showBox', 'Free TV', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SFR)
    oGui.addDir(SITE_IDENTIFIER, 'showBox', 'Sfr TV', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_ORANGE)
    oGui.addDir(SITE_IDENTIFIER, 'showBox', 'Orange TV', 'tv.png', oOutputParameterHandler)

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

### import code https://github.com/dvndrsn/M3uParser ###
### David Anderson code thanck's for good job ###

def parseM3U(infile):
    inf = open(infile,'r')

    # # # all m3u files should start with this line:
        #EXTM3U
    # this is not a valid M3U and we should stop..
    line = inf.readline()
    if not line.startswith('#EXTM3U'):
       return

    # initialize playlist variables before reading file
    playlist=[]
    song=track(None,None,None)

    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            # pull length and title from #EXTINF line
            length,title=line.split('#EXTINF:')[1].split(',',1)
            song=track(length,title,None)
        elif (len(line) != 0):
            # pull song path from all other, non-blank lines
            song.path=line
            playlist.append(song)

            # reset the song variable so it doesn't use the same EXTINF more than once
            song=track(None,None,None)

    inf.close()

    return playlist
    
def play():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('siteTitle')
    
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sTitle)
    oGuiElement.setMediaUrl(sUrl)

    oPlayer = cPlayer()
    oPlayer.clearPlayList()
    oPlayer.addItemToPlaylist(oGuiElement)
    oPlayer.startPlayer()
    return
        
    oGui.setEndOfDirectory()
    