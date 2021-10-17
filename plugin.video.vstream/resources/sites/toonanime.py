# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import time

from resources.lib.gui.hoster import cHosterGui  
from resources.lib.gui.gui import cGui  
from resources.lib.handler.inputParameterHandler import cInputParameterHandler  
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler  
from resources.lib.handler.requestHandler import cRequestHandler  
from resources.lib.parser import cParser  
from resources.lib.comaddon import progress
from resources.lib.util import urlEncode

SITE_IDENTIFIER = 'toonanime'
SITE_NAME = 'toonanime'  
SITE_DESC = 'anime en VF/VOSTFR' 

URL_MAIN = 'https://toonanime.cc/'  

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN, 'showMovies')
ANIM_VFS = (URL_MAIN + 'anime-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime-vostfr/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Dernier ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():  
    oGui = cGui()

    
    liste = []
    liste.append(['Action', URL_MAIN + 'action/'])
    liste.append(['Animation', URL_MAIN + 'animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'arts-martiaux/'])
    liste.append(['Aventure', URL_MAIN + 'aventure/'])
    liste.append(['Biopic', URL_MAIN + 'biopic/'])
    liste.append(['Comédie', URL_MAIN + 'comedie/'])
    liste.append(['Comédie Dramatique', URL_MAIN + 'comedie-dramatique/'])
    liste.append(['Comédie Musicale', URL_MAIN + 'comedie-musicale/'])
    liste.append(['Documentaire', URL_MAIN + 'documentaire/'])
    liste.append(['Drame', URL_MAIN + 'drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'epouvante-horreur/'])
    liste.append(['Erotique', URL_MAIN + 'erotique'])
    liste.append(['Espionnage', URL_MAIN + 'espionnage/'])
    liste.append(['Famille', URL_MAIN + 'famille/'])
    liste.append(['Fantastique', URL_MAIN + 'fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'guerre/'])
    liste.append(['Historique', URL_MAIN + 'historique/'])
    liste.append(['Musical', URL_MAIN + 'musical/'])
    liste.append(['Policier', URL_MAIN + 'policier/'])
    liste.append(['Péplum', URL_MAIN + 'peplum/'])
    liste.append(['Romance', URL_MAIN + 'romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'science-fiction/'])
    liste.append(['Spectacle', URL_MAIN + 'spectacle/'])
    liste.append(['Thriller', URL_MAIN + 'thriller/'])
    liste.append(['Western', URL_MAIN + 'western/'])
    liste.append(['Divers', URL_MAIN + 'divers/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:  
        oOutputParameterHandler.addParameter('siteUrl', sUrl) 
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        

    oGui.setEndOfDirectory()


def showMovieYears():  
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(xrange(1913, 2021)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(xrange(1936, 2021)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()  

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')  

    bGlobal_Search = False

    if sSearch:

        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch = sSearch.replace(URL_SEARCH[0], '')

        query_args = (('do', 'search'), ('subaction', 'search'), ('story', sSearch), ('titleonly', '0'), ('full_search','1'))

        data = urlEncode(query_args)

        oRequestHandler = cRequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParametersLine(data)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_SEARCH[0])
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addHeaderEntry('Content-Length',str(len(data)))
        sHtmlContent = oRequestHandler.request()

    else:
        oRequestHandler = cRequestHandler(sUrl)  
        sHtmlContent = oRequestHandler.request()  

    sPattern = '<article class="short__story.+?href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)".+?pg">([^<]+).+?cat">([^<]+).+?text">([^<]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
     
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sLang = aEntry[2].split(" ")[-1]
            sTitle = re.sub('Saison \d+','',aEntry[2][:aEntry[2].rfind('')].replace(sLang,"")) + " " + aEntry[4]
            sQual = aEntry[3]
            sDesc = aEntry[5]
            
            sTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang.upper())

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)  
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)  
            oOutputParameterHandler.addParameter('sThumb', sThumb)  
            oOutputParameterHandler.addParameter('sDesc', sDesc)  
            oOutputParameterHandler.addParameter('referer', sUrl)  

            oGui.addAnime(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                
        progress_.VSclose(progress_)  

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)  
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()  


def __checkForNextPage(sHtmlContent):  
    oParser = cParser()
    sPattern = '<a href="([^"]+)"><span class="md__icon md-arrowr"></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def ShowSerieSaisonEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    sMovieTitle = re.sub('Episode \d+','',sMovieTitle)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="buttons_.+?"(.+?)/div></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    i = 0
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            i = i + 1

            sPattern = 'id="(.+?)".+?>(.+?)<'
            aResult1 = oParser.parse(aEntry, sPattern)

            for aEntry1 in aResult1[1]:
                sTitle = sMovieTitle + " E" + str(i) + " [COLOR coral]Lecteur " + aEntry1[1] + "[/COLOR]"
                sUrl2 = aEntry1[0]

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sReferer', sUrl)

                oGui.addAnime(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def seriesHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sReferer = oInputParameterHandler.getValue('sReferer')

    Id = sReferer.split('/')[4].split('-')[0]

    query_args = (('newsId',Id), ('preset',''), ('preset2',Id), ('template',''), ('d',time.time() * 1000))

    data = urlEncode(query_args)

    oRequestHandler = cRequestHandler(URL_MAIN + "engine/ajax/full-story.php")
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sReferer)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'id="content_' + sUrl + '".+?>(.+?)<'

    oParser = cParser()
    aEntry = oParser.parse(sHtmlContent, sPattern)[1][0]

    if "https" in aEntry:
        sHosterUrl = aEntry

    elif "ToonVip" in sMovieTitle:
        sHosterUrl = "https://lb.toonanime.xyz/playlist/" +  aEntry + "/" + str(round(time.time() * 1000))
    elif "Sibnet" in sMovieTitle:
        sHosterUrl = "https://video.sibnet.ru/shell.php?videoid=" + aEntry
    elif "ToonHY" in sMovieTitle:
        sHosterUrl = "https://geoip.redirect-ads.com/?v=" + aEntry   

    sMovieTitle = re.sub("\[COLOR coral\](.+?)\[/COLOR\]","",sMovieTitle)

    if "toonanime" in sHosterUrl:
        oHoster = cHosterGui().checkHoster("mp4")
    else:
        oHoster = cHosterGui().checkHoster(sHosterUrl)

    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
