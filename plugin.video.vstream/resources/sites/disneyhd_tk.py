#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'disneyhd_tk'
SITE_NAME = 'Disney HD'
SITE_DESC = 'Disney HD: Tous les films Disney en streaming'

URL_MAIN = 'https://disneyhd.tk/'
URL_LISTE = URL_MAIN + 'liste_mosaique.php'

ANIM_ENFANTS = ('http://', 'load')

URL_SEARCH = ('', 'sHowResultSearch')
URL_SEARCH_MOVIES = ('', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

sPattern1 = '<a href="([^"]+)".+?src="([^"]+)" alt="(.+?)".+?>'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oOutputParameterHandler.addParameter('filtre', 'ajouts')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Ajouts récents', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oOutputParameterHandler.addParameter('filtre', 'nouveautes')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Nouveautés', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_LISTE)
    oOutputParameterHandler.addParameter('filtre', 'liste')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Liste des films', 'enfants.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sHowResultSearch(str(sSearchText))
        oGui.setEndOfDirectory()
        return

def sHowResultSearch(sSearch = ''):
    oGui = cGui()

    pdata = 'requete=' + sSearch
    oRequest = cRequestHandler(URL_MAIN + 'search.php')
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Host', 'disneyhd.tk')
    oRequest.addHeaderEntry('Referer', URL_MAIN + 'index.php')
    oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = '<a class="searchresult" href="([^"]+)".+?<img src="([^"]+)" alt="(.+?)"/>'
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

            sUrl = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'enfants.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()
        
def order(sList,sIndex):
    #remet en ordre le résultat du parser par un index ici par le titre qui est en position 2
    #exemple: ('http://venom', 'sThumb', 'sTitle')
    #          aResult = order(aResult[1],2)
    aResult = sorted(sList, key=lambda a:a[sIndex])
    #retourne au format du parser
    return True,aResult
    
def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sFiltre = oInputParameterHandler.getValue('filtre')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'ajouts' in sFiltre:
        sHtmlContent = oParser.abParse(sHtmlContent, '<i>Derniers films', '<i>Dernières sorties')
        aResult = oParser.parse(sHtmlContent, sPattern1)
    elif 'nouveautes' in sFiltre:
        sHtmlContent = oParser.abParse(sHtmlContent, '<i>Dernières sorties', '<b>Visionnés en ce moment')
        aResult = oParser.parse(sHtmlContent, sPattern1)
    else:
        sHtmlContent = oParser.abParse(sHtmlContent, 'par date de sortie', '</html>')
        aResult = oParser.parse(sHtmlContent, sPattern1)
        aResult = order(aResult[1],2)
        
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = aEntry[2].replace('streaming', '').replace(' 1080p', '')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'enfants.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()

    #film
    sPattern = '<p.+?<(?:iframe|video).+?src="([^"]+(?<!,))".+?<\/video>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            if '/mp4/' in sHosterUrl and not 'http' in sHosterUrl:
                sHosterUrl = 'http://disneyhd.tk%s' % sHosterUrl

            if '//goo.gl' in sHosterUrl:
                import urllib2
                try:
                    class NoRedirection(urllib2.HTTPErrorProcessor):
                        def http_response(self, request, response):
                            return response
                        https_response = http_response

                    opener = urllib2.build_opener(NoRedirection)
                    opener.addheaders.append (('User-Agent', UA))
                    opener.addheaders.append (('Connection', 'keep-alive'))

                    HttpReponse = opener.open(url8)
                    sHosterUrl = HttpReponse.headers['Location']
                    sHosterUrl = sHosterUrl.replace('https', 'http')
                except:
                    pass

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        #playlist-serie lien direct http pour le moment
        sPattern = '<li data-trackurl="([^"]+)">(.+?)<\/li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHosterUrl = aEntry[0]
                sTitle = aEntry[1]
                
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
             
        else:
            oGui.addText(SITE_IDENTIFIER)
            
    oGui.setEndOfDirectory()
