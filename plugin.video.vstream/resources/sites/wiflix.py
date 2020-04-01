#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress#, VSlog
# from resources.lib.util import cUtil

import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = 'wiflix'
SITE_NAME = 'Wiflix'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = 'https://vvw.wiflix.net/'

MOVIE_NEWS = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'serie-en-streaming/', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'serie-streaming/', 'showMovies')
# SERIE_LIST = (URL_MAIN + 'serie-streaming/', 'showSeriesList')

URL_SEARCH = (URL_MAIN, 'showSearch')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showSeries')
FUNCTION_SEARCH = 'showSearch'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):

        if 'film' in sUrl:
            showMovies(sSearchText)
        else:
            showSeries(sSearchText)

        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'film-en-streaming/action/'] )
    liste.append( ['Animation', URL_MAIN + 'film-en-streaming/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'film-en-streaming/arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'film-en-streaming/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'film-en-streaming/biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'film-en-streaming/comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'film-en-streaming/comedie-dramatique/'] )
    liste.append( ['Drame', URL_MAIN + 'film-en-streaming/drame/'] )
    liste.append( ['Documentaire', URL_MAIN + 'film-en-streaming/documentaire/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'film-en-streaming/horreur/'] )
    liste.append( ['Espionnage', URL_MAIN + 'film-en-streaming/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'film-en-streaming/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'film-en-streaming/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'film-en-streaming/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'film-en-streaming/historique/'] )
    liste.append( ['Musical', URL_MAIN + 'film-en-streaming/musical/'] )
    liste.append( ['Policier', URL_MAIN + 'film-en-streaming/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'film-en-streaming/romance/'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'film-en-streaming/science-fiction/'] )
    liste.append( ['Spectacles', URL_MAIN + 'film-en-streaming/spectacles/'] )
    liste.append( ['Thriller', URL_MAIN + 'film-en-streaming/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'film-en-streaming/western/'] )

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')

        pdata = 'do=search&subaction=search&story=' + sUrl + '&titleonly=3&all_word_seach=1&catlist[]=1'
        
        oRequest = cRequestHandler(URL_SEARCH[0])
        #oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Origin', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="mov clearfix">.+?<img *src="([^"]+)" *alt="([^"]+)".+?data-link="([^"]+)".+?class="nbloc1">([^<]+)<\/span.+?class="nbloc2">([^<]+)*<\/span'
    sPattern += '.+?"ml-label">Date de sortie:</div> <div class="ml-desc"> (.+?)</div>.+?"ml-label">Synopsis:</div> <div class="ml-desc">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sTitle = aEntry[1].replace(' wiflix', '')
            sUrl =  aEntry[2]
            sLang = aEntry[3]
            Squal = aEntry[4]
            sYear = aEntry[5]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[0]

            # Nettoyage du titre
            sDesc = str(aEntry[6])
            sDesc = sDesc.replace('en streaming ', '')
            sDesc = sDesc.replace('Regarder film ' + sTitle +';', '')
            sDesc = sDesc.replace('Regarder film ' + sTitle +':', '')
            sDesc = sDesc.replace('Voir film ' + sTitle +';', '')
            sDesc = sDesc.replace('Voir film ' + sTitle +':', '')
            sDesc = sDesc.replace('Voir Film ' + sTitle +':', '')
            sDesc = sDesc.replace('Voir film ' + sTitle +' :', '')
            sDesc = sDesc.replace('Regarder ' + sTitle +';', '')
            sDesc = sDesc.replace('Regarder ' + sTitle +' :', '')
            sDesc = sDesc.replace('Regarder ' + sTitle +':', '')
            sDesc = sDesc.replace('voir ' + sTitle +';', '')
            sDesc = sDesc.replace('voir ' + sTitle +':', '')
            sDesc = sDesc.replace('Voir ' + sTitle +':', '')
            sDesc = sDesc.replace('Regarder film ', '')
            sDesc = sDesc.strip()

            sDisplaytitle = '%s [%s] (%s)' % (sTitle, Squal, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplaytitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="pnext"><a href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeries(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')

        pdata = 'do=search&subaction=search&story=' + sUrl + '&titleonly=3&all_word_seach=1&catlist[]=31'

        oRequest = cRequestHandler(URL_SEARCH[0])
        #oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="mov clearfix">.+?<img *src="([^"]+)" *alt="([^"]+)".+?data-link="([^"]+)".+?<span class="block-sai">([^<]+)</span>.+?div class="ml-label">Synopsis.+?<div class="ml-desc">(.+?)<\/div>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[0]

            sTitle = aEntry[1].replace(' wiflix', '')
            sLang = re.sub('Saison \d+', '', aEntry[3]).replace(' ', '')
            sDisplaytitle = '%s (%s)' % (sTitle, sLang)
            sUrl =  aEntry[2]
            sDesc = aEntry[4]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'sHowEpisodes', sDisplaytitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def sHowEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="(ep.+?)"|<a href="([^"]+)" target="x_player">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                if 'epblocks' in aEntry[0]:
                    continue
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0].replace('ep', 'Episode ').replace('vs', ' Vostfr').replace('vf', ' VF') + '[/COLOR]')

            if aEntry[1]:
                sHosterUrl = aEntry[1]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a href="([^"]+)" *target="x_player_wfx"><span>.+?<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

