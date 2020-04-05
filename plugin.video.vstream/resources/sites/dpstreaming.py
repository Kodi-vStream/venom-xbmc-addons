#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, dialog, xbmc
import re
import requests

SITE_IDENTIFIER = 'dpstreaming'
SITE_NAME = 'DP Streaming'
SITE_DESC = 'Séries en Streaming'

URL_MAIN = 'https://dpstreaming.to/'

SERIE_SERIES = (URL_MAIN + 'serie-category/series/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'serie-category/series/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

ANIM_ENFANTS = (URL_MAIN + 'serie-category/series/dessin-anime/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def ProtectstreamBypass(url):
    if url.startswith('/'):
        url = URL_MAIN[:-1] + url


    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

    session = requests.Session()
    session.headers.update({
        'User-Agent': UA,
        'Referer': URL_MAIN,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    })

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print 'erreur ' + str(e)
        return ''

    sHtmlContent = response.text

    oParser = cParser()
    sPattern = 'var k=\"([^<>\"]*?)\";'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        dialog().VSinfo('Décodage en cours', 'Patientez', 5)
        xbmc.sleep(5000)

        postdata = aResult[1][0]
        headers = {
            'User-Agent': UA,
            'Accept': '*/*',
            'Referer': url,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        session.headers.update(headers)
        data = {'k': postdata}

        try:
            response = session.post(URL_MAIN + 'embed_secur.php', data = data)
        except requests.exceptions.RequestException as e:
            print 'erreur' + str(e)
            return ''

        data = response.text
        data = data.encode('utf-8', 'ignore')

        # VSlog(type(data))
        # VSlog(repr(data))

        #fh = open('c:\\test.txt', 'w')
        #fh.write(data)
        #fh.close()

        #Test de fonctionnement
        aResult = oParser.parse(data, sPattern)
        if aResult[0]:
            dialog().VSinfo('Lien encore protegé', 'Erreur', 5)
            return ''

        #recherche du lien embed
        sPattern = '<iframe src=["\']([^<>"\']+?)["\']'
        aResult = oParser.parse(data, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        #recherche d'un lien redirigee
        sPattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        aResult = oParser.parse(data, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

    return ''

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'serie-category/series/action/'] )
    liste.append( ['Animation', URL_MAIN + 'serie-category/series/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'serie-category/series/arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'serie-category/series/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'serie-category/series/biopic/'] )
    liste.append( ['Classique', URL_MAIN + 'serie-category/series/classique/'] )
    liste.append( ['Comédie', URL_MAIN + 'serie-category/series/comedie/'] )
    liste.append( ['Comédie dramatique', URL_MAIN + 'serie-category/series/comedie-dramatique/'] )
    liste.append( ['Comédie musicale', URL_MAIN + 'serie-category/series/comedie-musicale/'] )
    liste.append( ['Dessin animés', URL_MAIN + 'serie-category/series/dessin-anime/'] )
    liste.append( ['Divers', URL_MAIN + 'serie-category/series/divers/'] )
    liste.append( ['Documentaires', URL_MAIN + 'serie-category/series/documentaire/'] )
    liste.append( ['Drama', URL_MAIN + 'serie-category/series/drama/'] )
    liste.append( ['Drame', URL_MAIN + 'serie-category/series/drame/'] )
    liste.append( ['Epouvante-Horreur', URL_MAIN + 'serie-category/series/epouvante-horreur/'] )
    liste.append( ['Espionnage', URL_MAIN + 'serie-category/series/espionnage/'] )
    liste.append( ['Expérimental', URL_MAIN + 'serie-category/series/experimental/'] )
    liste.append( ['Famille', URL_MAIN + 'serie-category/series/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'serie-category/series/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'serie-category/series/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'serie-category/series/historique/'] )
    liste.append( ['Judiciaire', URL_MAIN + 'serie-category/series/judiciaire/'] )
    liste.append( ['Médical', URL_MAIN + 'serie-category/series/medical/'] )
    liste.append( ['Musical', URL_MAIN + 'serie-category/series/musical/'] )
    liste.append( ['Péplum', URL_MAIN + 'serie-category/series/peplum/'] )
    liste.append( ['Policier', URL_MAIN + 'serie-category/series/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'serie-category/series/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'serie-category/series/science-fiction/'] )
    liste.append( ['soap', URL_MAIN + 'serie-category/series/soap/'] )
    liste.append( ['Thriller', URL_MAIN + 'serie-category/series/thriller/'] )
    liste.append( ['Websérie', URL_MAIN + 'serie-category/series/webserie/'] )
    liste.append( ['Western', URL_MAIN + 'serie-category/series/western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch
        sUrl = sUrl.replace('%20', '+').replace(' ', '+')

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = re.sub('src="https://dpstreaming.to/wp-content/plugins/wp-fastest-cache-premium/pro/images/blank.gif"', '', sHtmlContent)
    sPattern = '<div class="moviefilm".+?<a href="([^"]+)".+?<img.+?src="([^"]+)" alt="([^"]+)".+?<p>(.+?)</p>'
    oParser = cParser()
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

            sUrl = aEntry[0]
            sThumb = re.sub('-119x125', '', aEntry[1])
            sTitle = aEntry[2].replace(' Streaming', '')
            sDesc = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">»</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeries():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #récupération du Synopsis plus complet que dans showmovies
    sDesc = ''
    try:
        sPattern = 'class="lab_syn">Synopsis :</span>(.+?)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].decode('utf-8')
            sDesc = cUtil().unescape(sDesc).encode('utf-8')
    except:
        pass

    sPattern = '<a href="([^<]+)" class.+?><span>(.+?)</span></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = sMovieTitle + ' episode ' + aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')

    sPattern = '<td class="lg" width=".+?">(?:(VF|VOSTFR|VO))<\/td>.+?<td class="lg" width=".+?">(.+?)</td>.+?<a href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sLang = aEntry[0]
            sHost = aEntry[1]
            sUrl = aEntry[2]

            sDisplayTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHosterUrl = ProtectstreamBypass(sUrl)

    oHoster = cHosterGui().checkHoster(sHosterUrl)

    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
