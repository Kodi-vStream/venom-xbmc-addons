#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, xbmc, dialog
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'serie_streaming_watch'
SITE_NAME = 'Serie-Streaming-Watch'
SITE_DESC = 'Séries & Animés en Streaming'

URL_MAIN = 'https://series-en-streaming.xyz/'

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN + 'category/series/?orderby=date', 'showMovies')
SERIE_LIST = (URL_MAIN + 'category/series/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

ANIM_ENFANTS = (URL_MAIN + 'category/series/dessin-anime/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Series (Liste)', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(URL_SEARCH[0] + sSearchText)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'category/series/action/'] )
    liste.append( ['Animation', URL_MAIN + 'category/series/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'category/series/arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'category/series/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'category/series/biopic/'] )
    liste.append( ['Classique', URL_MAIN + 'category/series/classique/'] )
    liste.append( ['Comédie', URL_MAIN + 'category/series/comedie/'] )
    liste.append( ['Comédie dramatique', URL_MAIN + 'category/series/comedie-dramatique/'] )
    liste.append( ['Comédie musicale', URL_MAIN + 'category/series/comedie-musicale/'] )
    liste.append( ['Dessin animés', URL_MAIN + 'category/series/dessin-anime/'] )
    liste.append( ['Divers', URL_MAIN + 'category/series/divers/'] )
    liste.append( ['Documentaire', URL_MAIN + 'category/series/documentaire/'] )
    liste.append( ['Drama', URL_MAIN + 'category/series/drama/'] )
    liste.append( ['Drame', URL_MAIN + 'category/series/drame/'] )
    liste.append( ['Epouvante-Horreur', URL_MAIN + 'category/series/epouvante-horreur/'] )
    liste.append( ['Espionnage', URL_MAIN + 'category/series/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'category/series/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'category/series/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'category/series/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'category/series/historique/'] )
    liste.append( ['Judiciaire', URL_MAIN + 'category/series/judiciaire/'] )
    liste.append( ['Médical', URL_MAIN + 'category/series/medical/'] )
    liste.append( ['Musical', URL_MAIN + 'category/series/musical/'] )
    liste.append( ['Péplum', URL_MAIN + 'category/series/peplum/'] )
    liste.append( ['Policier', URL_MAIN + 'category/series/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'category/series/romance/'] )
    liste.append( ['Science-fiction', URL_MAIN + 'category/series/science-fiction/'] )
    #liste.append( ['Séries', URL_MAIN + 'category/series/'] )
    liste.append( ['Soap', URL_MAIN + 'category/series/soap/'] )
    liste.append( ['Thriller', URL_MAIN + 'category/series/thriller/'] )
    liste.append( ['Webséries', URL_MAIN + 'category/series/webserie/'] )
    liste.append( ['Western', URL_MAIN + 'category/series/western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ','+')

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="(?:fixwidth|video)".+?a href="([^"]+)">.+?<img class="izimg" src="([^"]+)".+?title="([^"]+)"'
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
            sTitle = aEntry[2].replace(' Streaming', '')

            sThumb = aEntry[1]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            #tris search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'ShowEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="son bg"><a href="([^"]+)" *>Suivante'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def ShowEpisode():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #récupération des Synopsis
    sDesc = ''
    try:
        sPattern = '<b>Synopsis :</b>(.+?)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('\\', '').replace('&#8217;', '\'').replace('&#8230;', '...')
    except:
        pass

    sPattern = '<a href="([^"]+)" class="post-page-numbers".+?<span>([^<>]+)<\/span><\/a>'
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
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span class="lg">(.+?)<\/span>|<span class="myLecteur">Lecteur (?:<b>)*([a-z]+)(?:<\/b>)* *:<\/span> <a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                sLang = aEntry[0].replace('Langue(', 'Langue (')
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + sLang + '[/COLOR]')
            else:
                sHost = aEntry[1].capitalize()
                sUrl = aEntry[2]
                if sUrl.startswith('/'):
                    sUrl = URL_MAIN[:-1] + sUrl

                sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

def ProtectstreamBypass(url):

    #lien commencant par VID_
    Codedurl = url
    oRequestHandler = cRequestHandler(Codedurl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'var k=\"([^<>\"]*?)\";'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        postdata = 'k=' + aResult[1][0]

        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        xbmc.sleep(5000)

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

        oRequest = cRequestHandler(URL_MAIN + 'embed_secur.php')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        #oRequest.addHeaderEntry('Host', 'www.protect-stream.com')
        oRequest.addHeaderEntry('Referer', Codedurl)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(postdata)
        sHtmlContent = oRequest.request()

        #Test de fonctionnement
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            dialog().VSinfo('Lien encore protégé', "Erreur", 5)
            return ''

        #recherche du lien embed
        sPattern = '<iframe src=["\']([^<>"\']+?)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        #recherche d'un lien redirigee
        sPattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

    return ''
