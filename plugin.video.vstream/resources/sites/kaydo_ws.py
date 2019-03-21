#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog
import re, base64

from resources.lib.packer import cPacker
#copie du site http://www.kaydo.ws/
#copie du site https://www.hds.to/

SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo (hds.to)'
SITE_DESC = 'Site de streaming en HD'

URL_MAIN = 'https://hdss.to/'

MOVIE_NEWS = (URL_MAIN+ 'films/', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'mieux-notes/', 'showMovies')
MOVIE_VUE = (URL_MAIN + 'populaires/','showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_ALPHA = (True, 'showAlpha')

SERIE_NEWS = (URL_MAIN+'tv-seriess/','showMovies')

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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Top Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VUE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VUE[1], 'Top Vue Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ALPHA[1], 'Films (Par lettre)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAlpha():#creer une liste inversée d'annees
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(MOVIE_NEWS[0])
    sHtmlContent = oRequestHandler.request()

    sStart = '<ul class="AZList">'
    sEnd = '<section> <div class="Top AAIco-star_border"> <div class="Title">Les plus appréciés<'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li><a href="([^"]+?)">([^"]+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch(): #fonction de recherche
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
      sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #fh = open('d:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    if 'letters' in sUrl:
        sPattern1 = '<img src=\"([^\"]+?)\".+?\s*<a href="([^\"]+?)".+?\s*<strong>([^\"]+?)</strong>\s*.+?">\s*<.+?Qlty">([^\"]+?)</span>'
    else:
        sPattern1 = 'class=\"TPostMv\">.+?\s*.+?<a href=\"([^\"]+?)\">.+?<img src=\"([^\"]+?)\".+?Title\">([^\"]+?)</h3>.+?\s*.+?Qlty\">([^\"]+?)</span>.+?<p>([^\"]+?)</p>'

    aResult = oParser.parse(sHtmlContent, sPattern1)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'letters' in sUrl:
                sThumb = 'https://' + str(aEntry[0])
                siteUrl = str(aEntry[1])
                sDesc = ""
                sTitle = aEntry[2]
                sQual = str(aEntry[3])
                setDisplayName = ('%s [%s]') % (sTitle , sQual)
            else:
                sThumb = 'https://' + str(aEntry[1])
                siteUrl = str(aEntry[0])
                sDesc = str(aEntry[4])
                sTitle = aEntry[2]
                sQual = str(aEntry[3])
                setDisplayName = ('%s [%s]') % (sTitle , sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie/' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', setDisplayName, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', setDisplayName, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)


    if not sSearch:
        oGui.setEndOfDirectory()

#Pour les series, il y a generalement une etape en plus pour la selection des episodes ou saisons.
def ShowSerieSaisonEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="Title AA-Season" data-tab=".+?">Season <span>(.+?)</span>|class="MvTbImg">.+?img src.+?["|;]([^\"]+?)["|;].+?<a href="([^\"]+?)">([^\"]+?)</a>'

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
                oGui.addText(SITE_IDENTIFIER, '[COLOR red] Saison : ' + aEntry[0] + '[/COLOR]')
            else:
                sTitle = sMovieTitle + ' '+ aEntry[3]
                sUrl2 = aEntry[2]
                sThumb = aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showLinks():
    UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb  = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'id=.+?trembed=([^"]+).+?frameborder'
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

    for aEntry in aResult[1]:
        progress_.VSupdate(progress_, total) #dialog update
        if progress_.iscanceled():
            break

        site = URL_MAIN +"?trembed="+aEntry
        oRequestHandler = cRequestHandler(site)
        sHtmlContent = oRequestHandler.request()

        sPattern1 = '<div class="Video"><iframe width=".+?" height=".+?" src="([^"]+)" frameborder'
        aResult = oParser.parse(sHtmlContent, sPattern1)

        Url = ''.join(aResult[1])
        oRequestHandler = cRequestHandler(Url)
        sHtmlContent = oRequestHandler.request()
        #VSlog(sHtmlContent)

        sPattern1 = "var id.+?'(.+?)'"
        aResult = oParser.parse(sHtmlContent, sPattern1)
        sPost = ''.join(aResult[1])[::-1]
        VSlog(''.join(aResult[1])[::-1])

        oRequestHandler = cRequestHandler('https://hdss.to/?trhide=1&trhex='+sPost)
        sHtmlContent = oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()

