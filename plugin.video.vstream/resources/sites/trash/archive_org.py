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

 
SITE_IDENTIFIER = 'archive_org'
SITE_NAME = '[COLOR orange]Archive.org[/COLOR]'
SITE_DESC = 'Film en streaming'
 

URL_MAIN = 'http://www.archive.org'
URL_FILMS = 'https://ia601408.us.archive.org/30/items/urllist_201412/fadoz.txt'
URL_HD1080 = 'https://ia601408.us.archive.org/30/items/urllist_201412/cinema.txt' 
MOVIE_GENRES = (True, 'showGenre')
MOVIE_NEWS = ('https://ia601408.us.archive.org/30/items/urllist_201412/fadoz.txt', 'showWeb')

cover = 'film.jpg'       
#sRootfilm = cConfig().getRootfilm()

#Test update

class track():
    def __init__(self, length, title, path, cover):
        self.length = length
        self.title = title
        self.path = path
        self.cover = cover

def load():
    linktv = cConfig().getSetting('pvr-view')
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_HD1080)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', '[COLOR gold]Vouz pouvez ajoutez vos films favoris dans la section Cinema plus d infos sur le ghithub vstream[/COLOR]', 'film.jpg', oOutputParameterHandler)
            
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_FILMS)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', '[COLOR white]Films Nouveautés[/COLOR]', 'film.jpg', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_HD1080)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', '[COLOR white]Films Cinéma[/COLOR]', 'film.jpg', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', '[COLOR white]Films Genre[/COLOR]', 'genres.jpg', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []

    liste.append( ['Action','https://ia601408.us.archive.org/30/items/urllist_201412/action.txt'] )
    liste.append( ['Aventure','https://ia601408.us.archive.org/30/items/urllist_201412/aventure.txt'] )
    liste.append( ['Comedie','https://ia601408.us.archive.org/30/items/urllist_201412/comedie.txt'] )
    liste.append( ['Drame','https://ia601408.us.archive.org/30/items/urllist_201412/drame.txt'] )
    liste.append( ['Fantastique','https://ia601408.us.archive.org/30/items/urllist_201412/fantastique.txt'] )
    liste.append( ['Horreur','https://ia601408.us.archive.org/30/items/urllist_201412/horreur.txt'] )
    liste.append( ['Policier','https://ia601408.us.archive.org/30/items/urllist_201412/policier.txt'] )
    liste.append( ['Science Fiction','https://ia601408.us.archive.org/30/items/urllist_201412/science-fiction.txt'] )
    liste.append( ['Thriller','https://ia601408.us.archive.org/30/items/urllist_201412/thriller.txt'] )
    liste.append( ['Documentaire','https://ia601408.us.archive.org/30/items/urllist_201412/documentaire.txt'] )
    liste.append( ['Animation','https://ia601408.us.archive.org/30/items/urllist_201412/animation.txt'] )
    liste.append( ['Spectacle','https://ia601408.us.archive.org/30/items/urllist_201412/spectacle.txt'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'genres.jpg', oOutputParameterHandler)

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
        oGui.addDir(SITE_IDENTIFIER, 'play', track.title, 'film.jpg', oOutputParameterHandler)
    
  
    oGui.setEndOfDirectory()

def showWeb():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    playlist = parseWebM3U(sUrl)

    for track in playlist:
        
        sTitle = cUtil().DecoTitle(track.title)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', str(track.path))
        oOutputParameterHandler.addParameter('siteTitle', str(track.title))
        oOutputParameterHandler.addParameter('sThumbnail', str(track.cover))
        oGui.addMisc(SITE_IDENTIFIER, 'play', sTitle, 'film.jpg' , track.cover, '', oOutputParameterHandler)    
  
    oGui.setEndOfDirectory()

# import code https://github.com/dvndrsn/MP4Parser ###
# David Anderson code thanck's for good job ###

def parseWebM3U(infile):
    inf = urllib.urlopen(infile)

    line = inf.readline()

    if not line.startswith('#EXTMMP4'):
       return

    playlist=[]
    song=track(None,None,None,None)

    for line in inf:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            length,title=line.split('#EXTINF:')[1].split(',',1)
            try:
                lcover = line.split('#EXTINF:')[1].partition('film-logo=')[2]
                cover = lcover.split('"')[1]
            except:
                cover = "film.jpg"
            song=track(length,title,None,cover)
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
    if not line.startswith('#EXTMMP4'):
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
    
