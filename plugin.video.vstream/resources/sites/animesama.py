# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import addon, siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'animesama'
SITE_NAME = 'Anime Sama'
SITE_DESC = 'Animés - Films et séries'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_GENRES = ('catalogue/?genre%5B%5D=%s', 'showGenres')

URL_SEARCH = ('catalogue/?search=', 'showSeries')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showSeries')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showSeries')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Par genre', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    liste = [
        'Action','Adolescence','Amitié','Amour','Arts martiaux','Assassinat',
        'Autre monde','Aventure','Combats','Comédie','Crime','Démons','Donghua','Drame','Ecchi',
        'Ecole','Famille','Fantastique','Fantasy','Ghibli','Guerre','Harem','Historique','Horreur',
        'Isekai','Jeux','Josei','Magie','Mechas','Militaire','Monstres','Musique','Mystère','Nostalgie',
        'Politique','Psychologique','Quotidien','Romance','Samouraïs','School Life','Science-fiction',
        'Seinen','Shôjo','Shônen','Slice of Life','Sport','Surnaturel',
        'Thriller','Tournois','Travail','Vampires','Vengeance','Voyage temporel']

    oOutputParameterHandler = cOutputParameterHandler()
    for sGenre in liste:
        sUrl = siteUrl % sGenre.replace(' ', '%20')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sGenre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showSeries(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.split('=')[-1]
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = siteUrl = oInputParameterHandler.getValue('siteUrl')
        sPage = oInputParameterHandler.getValue('sPage')
        if sPage:
            sUrl += '&page=' + sPage

    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'flex divide-x.+?href="([^"]+)".+?src="([^"]+).+?clamp-2">([^<]+)<.+?truncate">([^<]*).+?truncate">([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sType = aEntry[4]
            
            if 'Film' not in sType and 'Anime' not in sType:
                continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'Film' in sType:
                oGui.addMovie(SITE_IDENTIFIER, 'showSaison', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'showSaison', sTitle, 'animes.png', sThumb, '', oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sPage', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sNextPage, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "Pagination.+?mt-5 bg-sky-900.+?<a href='\?.+?(\d+)\'"
    aResult = oParser.parse(sHtmlContent, sPattern)
    return aResult[1][0] if aResult[0] else False


def showSaison():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'panneauAnime\("([^"]+)", "([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDecoColor = addon().getSetting('deco_color')

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sorted(aResult[1]):

            sSaison = aEntry[0]
            sUrlSaison = aEntry[1]
            if sUrlSaison == 'url':
                continue
            
            bMovie = False
            if 'Saison' not in sSaison:
                bMovie = True
                sSaison = sSaison.replace('Film', '[COLOR %s][Film][/COLOR] ' % sDecoColor) + ' - '

            sDisplayTitle = sSaison + ' ' + sMovieTitle
            sTitle = sMovieTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl + '/' + sUrlSaison)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if bMovie:
                oGui.addMovie(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    addEpisode(sUrl.replace('/vostfr', '/vf'), sMovieTitle)
    addEpisode(sUrl.replace('/vf', '/vostfr'), sMovieTitle)

    oGui.setEndOfDirectory()


def addEpisode(sUrl, sMovieTitle):
    
    try:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    except:
        return

    oGui = cGui()
    oParser = cParser()

    data = sUrl.split('/')
    sSaison = data[-2]
    sLang = data[-1].upper()

    sPattern = '<script type="text/javascript" src="([^"]+)\" defer'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:

        sUrl += '/' + aResult[1][0]
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        
        sPattern = 'var eps\d = (\[.+?\]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            episodes = eval(aResult[1][0])
            for numEp in range (len(episodes)):
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sLang', sLang)
                if 'saison' in sSaison:
                    sDisplayTitle = sTitle = '%s %s E%d' % (sMovieTitle, sSaison, numEp + 1)
                    sDisplayTitle += ' (%s)' % sLang
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sEpisode', numEp)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
                else:
                    sDisplayTitle = sTitle = sMovieTitle
                    sDisplayTitle += ' (%s)' % sLang
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', '', oOutputParameterHandler)


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sEpisode = oInputParameterHandler.getValue('sEpisode')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'var eps\d = (\[.+?\]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        numEp = int(sEpisode)-1
        for entry in aResult[1]:
            episodes = eval(entry)
            if numEp < len(episodes):
                sHosterUrl = episodes[numEp]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl)

    oGui.setEndOfDirectory()

