#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'pastebin'
SITE_NAME = 'pastebin'
SITE_DESC = 'Liste depuis pastebin'

URL_MAIN = 'https://pastebin.com/raw/'
PASTE_1 = URL_MAIN + 'n5P3Crbz'
PASTE_2 = URL_MAIN + 'mbPxAFNm'
PASTE_3 = URL_MAIN + 'SAjKPcBm'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sMedia', 'film')
    oOutputParameterHandler.addParameter('siteUrl', PASTE_1)
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Films (Genres)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sMedia', 'serie')
    oOutputParameterHandler.addParameter('siteUrl', PASTE_2)
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Séries (Genres)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sMedia', 'film')
    oOutputParameterHandler.addParameter('siteUrl', PASTE_3)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Les Simpson (Intégrale)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMedia = oInputParameterHandler.getValue('sMedia')
 
    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
 
    lines = sContent.splitlines()

    genres = set()     
    for line in lines:
        movie = line.split(';')
     
        if sMedia not in movie[0]:
            continue 

        genre = movie[4]
        genre = eval(genre)
        if genre:
            genres = genres.union(genre)
                
    for sGenre in sorted(genres):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sGenre', sGenre)
        oOutputParameterHandler.addParameter('sMedia', sMedia)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sGenre, 'genres.png', oOutputParameterHandler)
 
 
    oGui.setEndOfDirectory()

 
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMedia = oInputParameterHandler.getValue('sMedia')
    sGenre = oInputParameterHandler.getValue('sGenre')
 
    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
 
    lines = sContent.splitlines()

    total = len(lines)
    progress_ = progress().VScreate(SITE_NAME)
    for line in lines:
        progress_.VSupdate(progress_, total)
        if progress_.iscanceled():
            break
 
        movie = line.split(';')
     
        if sMedia not in movie[0]:
            continue 

        genres = movie[4]
        if sGenre and genres:
            genres = eval(genres)
            if sGenre not in genres:
                continue
        sTmdbId = movie[1].strip()
        sTitle = movie[2].strip()
        year = movie[3].strip()
        if year :
            sTitle = '%s (%s)' % (sTitle, year)
        
        sHost = movie[5]
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sHost', sHost)
        if sTmdbId:
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        
        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', '', '', oOutputParameterHandler)
            
    progress_.VSclose(progress_)
 
    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sHoster = oInputParameterHandler.getValue('sHost')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sHoster = eval(sHoster)
    
    
    for sHosterUrl in sHoster:
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
 
    oGui.setEndOfDirectory()
