#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
import re

SITE_IDENTIFIER = 'disneyhd_tk'
SITE_NAME = 'Disney HD'
SITE_DESC = 'Disney HD: Tous les films Disney en streaming'

URL_MAIN = 'http://disneyhd.tk/'
URL_LISTE = URL_MAIN + 'liste_mosaique.php'

ANIM_ENFANTS = ('http://', 'load')

URL_SEARCH = ('', 'sHowResultSearch')
URL_SEARCH_MOVIES = ('', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

sPattern1 = '<a href="([^"]+)"><img.+?src="([^"]+)" alt="(.+?)".+?>'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'index.php')
    oOutputParameterHandler.addParameter('filtre', 'ajouts')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Ajouts récents', 'animes_enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'index.php')
    oOutputParameterHandler.addParameter('filtre', 'nouveautes')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Nouveautés', 'animes_enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_LISTE)
    oOutputParameterHandler.addParameter('filtre', 'liste')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Liste des films', 'animes_enfants.png', oOutputParameterHandler)

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
    oRequest.addHeaderEntry('User-Agent',UA)
    oRequest.addHeaderEntry('Host','disneyhd.tk')
    oRequest.addHeaderEntry('Referer',URL_MAIN + 'index.php')
    oRequest.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequest.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = '<a href="([^"]+)"><img.+?src="([^"]+)" alt="(.+?)"/><\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'animes_enfants.png',sThumb, '', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sFiltre = oInputParameterHandler.getValue('filtre')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'ajouts' in sFiltre:
        sPattern = '<i>Derniers films.+?</i>(.+?)<i>Dernières sorties.+?</i>'
        sHtmlContent = re.search(sPattern,sHtmlContent,re.DOTALL)
        aResult = oParser.parse(sHtmlContent.group(1), sPattern1)
    elif 'nouveautes' in sFiltre:
        sPattern = '<i>Dernières sorties.+?</i>(.+?)<div id="pieddepage">'
        sHtmlContent = re.search(sPattern,sHtmlContent,re.DOTALL)
        aResult = oParser.parse(sHtmlContent.group(1), sPattern1)
    else:
        aResult = oParser.parse(sHtmlContent, sPattern1)
        aResult[1].sort()

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = aEntry[2].replace('streaming','')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'animes_enfants.png',sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<p.+?<(?:iframe|video).+?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)
            if '/mp4/' in sHosterUrl:
                sHosterUrl = 'http://disneyhd.tk%s' % sHosterUrl

            if '//goo.gl' in sHosterUrl:
                import urllib2
                try:
                    class NoRedirection(urllib2.HTTPErrorProcessor):
                        def http_response(self, request, response):
                            return response

                    url8 = sHosterUrl.replace('https','http')

                    opener = urllib2.build_opener(NoRedirection)
                    opener.addheaders.append (('User-Agent', UA))
                    opener.addheaders.append (('Connection', 'keep-alive'))

                    HttpReponse = opener.open(url8)
                    sHosterUrl = HttpReponse.headers['Location']
                    sHosterUrl = sHosterUrl.replace('https','http')
                except:
                    pass

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
