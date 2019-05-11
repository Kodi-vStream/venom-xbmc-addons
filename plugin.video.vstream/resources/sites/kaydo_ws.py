#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress
import re, base64

from resources.lib.packer import cPacker
#copie du site http://www.kaydo.ws/
#copie du site https://www.hds.to/

SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo (hdss.to)'
SITE_DESC = 'Site de streaming en HD'

URL_MAIN = 'https://hdss.to/'

MOVIE_MOVIE = (URL_MAIN + 'filmss/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'filmss/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'populaires/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'mieux-notes/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_LIST = (True, 'showAlpha')

SERIE_SERIES = (URL_MAIN + 'tv-seriess/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'tv-seriess/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search/', 'showMovies')
FUNCTION_SEARCH = 'sHowResultSearch'

def Decode(chain):
    try:
        chain = 'aHR' + chain
        chain = 'M'.join(chain.split('7A4c1Y9T8c'))
        chain = 'V'.join(chain.split('8A5d1YX84A428s'))
        chain = ''.join(chain.split('$'))

        return base64.b64decode(chain)
    except:
        return chain

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Par lettre)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAlpha():
    oGui = cGui()

    liste = []
    liste.append( ['#', URL_MAIN + 'letters/0-9/'] )
    liste.append( ['A', URL_MAIN + 'letters/a/'] )
    liste.append( ['B', URL_MAIN + 'letters/b/'] )
    liste.append( ['C', URL_MAIN + 'letters/c/'] )
    liste.append( ['D', URL_MAIN + 'letters/d/'] )
    liste.append( ['E', URL_MAIN + 'letters/e/'] )
    liste.append( ['F', URL_MAIN + 'letters/f/'] )
    liste.append( ['G', URL_MAIN + 'letters/g/'] )
    liste.append( ['H', URL_MAIN + 'letters/h/'] )
    liste.append( ['I', URL_MAIN + 'letters/i/'] )
    liste.append( ['J', URL_MAIN + 'letters/j/'] )
    liste.append( ['K', URL_MAIN + 'letters/k/'] )
    liste.append( ['L', URL_MAIN + 'letters/l/'] )
    liste.append( ['M', URL_MAIN + 'letters/m/'] )
    liste.append( ['N', URL_MAIN + 'letters/n/'] )
    liste.append( ['O', URL_MAIN + 'letters/o/'] )
    liste.append( ['P', URL_MAIN + 'letters/p/'] )
    liste.append( ['Q', URL_MAIN + 'letters/q/'] )
    liste.append( ['R', URL_MAIN + 'letters/r/'] )
    liste.append( ['S', URL_MAIN + 'letters/s/'] )
    liste.append( ['T', URL_MAIN + 'letters/t/'] )
    liste.append( ['U', URL_MAIN + 'letters/u/'] )
    liste.append( ['V', URL_MAIN + 'letters/v/'] )
    liste.append( ['W', URL_MAIN + 'letters/w/'] )
    liste.append( ['X', URL_MAIN + 'letters/x/'] )
    liste.append( ['Y', URL_MAIN + 'letters/y/'] )
    liste.append( ['Z', URL_MAIN + 'letters/z/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
    return

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'action/'] )
    liste.append( ['Animation', URL_MAIN + 'animation/'] )
    liste.append( ['Aventure', URL_MAIN + 'aventure/'] )
    liste.append( ['Comédie', URL_MAIN + 'comedie/'] )
    liste.append( ['Crime',URL_MAIN + 'crime/'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'drame/'] )
    liste.append( ['Etranger', URL_MAIN + 'etranger/'] )
    liste.append( ['Fantastique', URL_MAIN + 'fantastique/'] )
    liste.append( ['Famille', URL_MAIN + 'familial/'] )
    liste.append( ['Guerre', URL_MAIN + 'guerre/' ] )
    liste.append( ['Historique', URL_MAIN + 'histoire/'] )
    liste.append( ['Horreur',URL_MAIN + 'horreur/'] )
    liste.append( ['Musical', URL_MAIN + 'musique/'] )
    liste.append( ['Mystere',URL_MAIN + 'mystere/'] )
    liste.append( ['Romance', URL_MAIN + 'romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'science-fiction/'] )
    liste.append( ['Telefilm', URL_MAIN + 'telefilm/'] )
    liste.append( ['Thriller', URL_MAIN + 'thriller/'] )
    liste.append( ['Western', URL_MAIN + 'western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #réécriture pour prendre les séries dans le menu des genres
    sHtmlContent = sHtmlContent.replace('<span class="Qlty">TV</span></div><h3', '</div><h3')

    #fh = open('d:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    if 'letters' in sUrl:
        sPattern = '<td class="MvTbImg"> *<a href="([^"]+)".+?(?:<img |data-wpfc-original-)src="([^"]+)".+?strong>([^<]+)<.+?span class="Qlty">([^<]+)<'
    elif 'serie' in sUrl:
        sPattern = 'href="([^"]+)"><div class="Image"><figure class="Objf TpMvPlay AAIco-play_arrow"><img src="([^"]+)" alt="Image ([^"]+)"><figcaption>.+?</figure></div><h3 class="Title">[^<]+</h3>.+?class="Description"><p>[^,]+,([^<]+)<'
    else:
        sPattern = 'href="([^"]+)"><div class="Image"><figure class="Objf TpMvPlay AAIco-play_arrow"><img src="([^"]+)" alt="Image ([^"]+)"></figure></div><h3 class="Title">[^<]+</h3>.+?class="Qlty">([^<]+)<.+?class="Description"><p>[^,]+,([^<]+)<'

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

            if 'letters' in sUrl:
                siteUrl = aEntry[0]
                sThumb = aEntry[1].replace('w92', 'w342')
                if sThumb.startswith('//'):
                    sThumb = 'https:' + sThumb
                sTitle = aEntry[2]
                sQual = aEntry[3]
                sDesc = ''

                sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            elif 'serie' in sUrl:
                siteUrl = aEntry[0]
                sThumb = aEntry[1].replace('w185', 'w342')
                if sThumb.startswith('//'):
                    sThumb = 'https:' + sThumb
                sTitle = aEntry[2]
                sDesc = aEntry[3]

                sDisplayTitle = sTitle

            else:
                siteUrl = aEntry[0]
                sThumb = aEntry[1].replace('w154', 'w342').replace('w185', 'w342')
                if sThumb.startswith('//'):
                    sThumb = 'https:' + sThumb
                sTitle = aEntry[2]
                sQual = aEntry[3]
                sDesc = aEntry[4]

                sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/serie/' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSaisonEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def ShowSaisonEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="Title AA-Season.+?>Season <span>([^<]+)</span>|class="MvTbImg">.+?img src.+?["|;]([^\"]+?)["|;].+?href="([^"]+)">([^<]+)<'

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
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]Saison: ' + aEntry[0] + '[/COLOR]')
            else:
                sThumb = aEntry[1].replace('w92', 'w342').replace('w185', 'w342')
                if sThumb.startswith('//'):
                    sThumb = 'https:' + sThumb
                sUrl2 = aEntry[2]
                sTitle = aEntry[3]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="next page-numbers" href="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb  = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Recuperer variable pour url de base
    sPattern = 'id=.+?trembed=([^"]+).+?frameborder'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            site = URL_MAIN + "?trembed=" + aEntry
            oRequestHandler = cRequestHandler(site)
            sHtmlContent = oRequestHandler.request()

            #Recuperation de l'url suivante
            sPattern1 = '<div class="Video"><iframe width=".+?" height=".+?" src="([^"]+)&" frameborder'
            aResult = oParser.parse(sHtmlContent, sPattern1)

            Url = ''.join(aResult[1])
            oRequestHandler = cRequestHandler(Url)
            sHtmlContent = oRequestHandler.request()

            #Recuperation de l'id
            sPattern1 = "var id.+?'(.+?)'"
            aResult = oParser.parse(sHtmlContent, sPattern1)
            sPost = ''.join(aResult[1])[::-1]

            oRequestHandler = cRequestHandler(URL_MAIN + '?trhidee=1&trfex=' + sPost)
            oRequestHandler.addHeaderEntry('Referer', Url)
            sHtmlContent = oRequestHandler.request()
            sHosterUrl = oRequestHandler.getRealUrl()

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
