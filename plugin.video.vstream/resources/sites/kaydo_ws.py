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

URL_MAIN = 'https://hds-streaming.com/'

MOVIE_NEWS = (URL_MAIN + 'hds-film/', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'top-du-moment/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_ALPHA = (True, 'showAlpha')

SERIE_NEWS = (URL_MAIN + 'hds-series/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'sHowResultSearch')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'sHowResultSearch')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'


def getHost(url):
    parts = url.split('//', 1)
    host = parts[0] + '//' + parts[1].split('/', 1)[0]
    return host
        
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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ALPHA[1], 'Films (Par lettre)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():#creer une liste inversée d'annees
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(MOVIE_NEWS[0])
    sHtmlContent = oRequestHandler.request()

    sStart = '<h2>Date de sorties</h2><ul class="releases falsescroll"><li>'
    sEnd = '<nav class="genres"><h2>Genres</h2>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^"]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAlpha():#creer une liste inversée d'annees
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(MOVIE_NEWS[0])
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="letter_home"><div class="fixresp"><ul class="glossary">'
    sEnd = '<div class="module"><div class="content"><header class="archive_post">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'data-glossary="(.+?)">([^"]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = 'https://hds-streaming.com/wp-json/dooplay/glossary/?term=' + aEntry[0] + '&nonce=b4bced2d3f&type=movies'
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText
        if '' in sSearchText:
            sSearchText.replace('','+')
        sHowResultSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def sHowResultSearch(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="login-box">(.+?)<footer class='
    aResult = re.search(sPattern, sHtmlContent, re.DOTALL)
    if (aResult):
        sHtmlContent = aResult.group(1)

    sPattern = '<img src="([^"]+?)" alt="([^"]+?) streaming.+?<a href="([^"]+?)".+?<p>([^"]+?)</p>'
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

            sUrl = aEntry[2]
            sThumb = aEntry[0]
            sDesc = aEntry[3]
            sTitle = str(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesEpisode', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'genre/action/'] )
    liste.append( ['Action-Aventure',URL_MAIN + 'genre/action-adventure/'])
    liste.append( ['Animation', URL_MAIN + 'genre/animation/'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure/'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie/'] )
    liste.append( ['Crime',URL_MAIN + 'genre/crime/'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique/'] )
    liste.append( ['Famille', URL_MAIN + 'genre/familial/'] )
    liste.append( ['Historique', URL_MAIN + 'genre/histoire/'] )
    liste.append( ['Horreur',URL_MAIN + 'genre/horreur/'] )
    liste.append( ['Musical', URL_MAIN + 'genre/musique/'] )
    liste.append( ['Mystere',URL_MAIN + 'genre/mystere/'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'genre/science-fiction/'] )
    liste.append( ['science-fiction Fantastique',URL_MAIN + 'genre/science-fiction-fantastique/'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'genre/western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('Bande-Annonce', '')

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n', ''))
    #fh.close()

    if "wp-json" in sUrl:
        sPattern1 = 'title.+?"([^"]+)(?:streaming.+?(?:gratuit|gratuitement)).+?url.+?"([^"]+)".+?img.+?"([^"]+)"'
    elif 'top-du-moment' in sUrl:
        sPattern1 = '<img src="([^"]+?)" alt="([^"]+?)(?:streaming.+?|"(?:.+?<span class="quality">([^"]+?)</span>.+?|.+?))href="([^"]+?)"'
    else:
        sPattern1 = '<img src="([^"]+?)" alt="([^"]+?)(?:streaming.+?|"(?:.+?<span class="quality">([^"]+?)</span>.+?|.+?))href="([^"]+?)".+?"texto">([^"]+?)</div>'

    aResult = oParser.parse(sHtmlContent, sPattern1)

    if not (aResult[0] == True):
        aResult = oParser.parse(sHtmlContent, sPattern1)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if "wp-json" in sUrl:
                sThumb = str(aEntry[2]).replace('\/','\\')
                siteUrl = str(aEntry[1]).replace('\/','\\')
                sDesc = ''
                sTitle = aEntry[0].encode('string-escape').decode('utf-8')
            elif 'top-du-moment' in sUrl:
                sThumb = str(aEntry[0])
                siteUrl = str(aEntry[3])
                sDesc = ''
                sTitle = aEntry[1]
                sQual = str(aEntry[2])
                setDisplayName = ('%s  [%s]') % (sTitle , sQual)
            else:
                sThumb = str(aEntry[0])
                siteUrl = str(aEntry[3])
                sDesc = str(aEntry[4])
                sTitle = aEntry[1]
                sQual = str(aEntry[2])
                setDisplayName = ('%s [%s]') % (sTitle , sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/hds-series' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesEpisode', setDisplayName, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', setDisplayName, 'films.png', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeriesEpisode():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img src="([^"]+?)".+?div class="numerando">(.+?)-(.+?)</div>.+?href="([^"]+?)">([^"]+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = str(aEntry[0])
            siteUrl = str(aEntry[3])
            #sDesc = str(aEntry[4])
            sTitle = ('%s : (%s)') % (sMovieTitle, str(aEntry[4]))
            sTitle = 'Saison ' + aEntry[1] + ' Episode' + aEntry[2] +' ' + sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

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

    if 'episodes' in sUrl:
        sPattern = '<li id=".+?" class=".+?" data-type=".+?" data-post="(.+?)" data-nume="1">'
    else:
        sPattern = '<input type="hidden" name="idpost" value="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0]):
        idFilm = aResult[1][0]

    oRequestHandler = cRequestHandler("https://hds-streaming.com/wp-admin/admin-ajax.php")
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent',UA)
    oRequestHandler.addHeaderEntry('Referer',sUrl)
    oRequestHandler.addParameters('action','doo_player_ajax')
    oRequestHandler.addParameters('post',idFilm)
    oRequestHandler.addParameters('nume','1')
    if 'episodes' in sUrl:
        oRequestHandler.addParameters('type','tv')
    else:
        oRequestHandler.addParameters('type','movie')
    sHtmlContent2 = oRequestHandler.request()

    sPattern2 = 'src=["\'](.+?)[\'"]'
    aResult = oParser.parse(sHtmlContent2, sPattern2)

    if (aResult[0] == True):
        VSlog('Url : ' + str(aResult[1][0]))
        url = aResult[1][0]

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent',UA)
    oRequestHandler.addHeaderEntry('Referer',sUrl)
    sHtmlContent3 = oRequestHandler.request()

    sPattern3 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = oParser.parse(sHtmlContent3, sPattern3)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent3)
    #fh.close()

    if aResult[0]:
        str2 = str(aResult[1][0])
        if not str2.endswith(';'):
            str2 = str2 + ';'

        strs = cPacker().unpack(str2)

        sPattern4 = 'file:"(.+?)"'
        aResult = oParser.parse(strs, sPattern4)
        if aResult:
            sHosterUrl = aResult[1][0]
            VSlog(sHosterUrl)
    else:
        url2 = url.split('?')
        tab = url2[1].split('=')
        url3 = getHost(url) + '/embed-'+ tab[0] + '.html?auto=1'
        VSlog(url3)
        
        oRequestHandler = cRequestHandler(url3)
        sHtmlContent3 = oRequestHandler.request()
        
        aResult = oParser.parse(sHtmlContent3, 'sources: *\["([^"\']+)')
        if aResult:
            sHosterUrl = aResult[1][0]
            VSlog(sHosterUrl)

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
    oGui.setEndOfDirectory()
