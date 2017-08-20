#-*- coding: utf-8 -*-
#Venom.kodigoal
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cJheberg
from resources.lib.multihost import cMultiup
import re

SITE_IDENTIFIER = 'robindesdroits'
SITE_NAME = 'Robin des Droits'
SITE_DESC = 'Replay sports'

URL_MAIN = 'http://www.robindesdroits.me/'

SPORT_SPORTS = (True, 'showGenres')
SPORT_NEWS = (URL_MAIN + 'derniers-uploads/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Nouveautés', URL_MAIN + 'derniers-uploads/'] )
    liste.append( ['Football', URL_MAIN + 'football/'] )
    liste.append( ['Sports US', URL_MAIN + 'sports-us/'] )
    liste.append( ['Sports Automobiles', URL_MAIN + 'sports-automobiles/'] )
    liste.append( ['Rugby', URL_MAIN + 'rugby/'] )
    liste.append( ['Tennis', URL_MAIN + 'tennis/'] )
    liste.append( ['Autres Sports', URL_MAIN + 'autres-sports/'] )
    liste.append( ['Divers', URL_MAIN + 'divers/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<div class="mh-loop-thumb"><a href="([^"]+)"><img src=".+?" style="background:url\(\'(.+?)\'\).+?rel="bookmark">(.+?)</a></h3>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            sUrl    = str(aEntry[0])
            sThumbnail = str(aEntry[1])
            sTitle  = (' %s ') % (str(aEntry[2]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail,'', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="next page-numbers" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def __showLink(url):

    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request();

    #recup liens clictune
    sPattern = '<a href="(http://www.clictune.+?)"'
    aResult = re.findall(sPattern,sHtmlContent)

    #recup liens sans delai X secondes
    if (aResult):
        sLink =[]
        for aEntry in aResult:

            sUrl = str(aEntry)
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request();

            sPattern = '<b><a href\="http\:\/\/www\.clictune\.com\/link\/redirect\/\?url\=(.+?)\&id.+?">'
            aResult = re.findall(sPattern,sHtmlContent)

            #decode url & retourne liens a showHosters
            url = cUtil().urlDecode(aResult[0])
            sLink.append(url)

        return sLink
    return False

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #recup liens watchvideo&Jheberg&Multiup et liens direct raptu&uptobox par showLink()
    sLink = __showLink(sUrl)

    #si vidéos découpées en X parties
    count = 0
    count2 = 0
    count3 = 0

    if (sLink):
        for aEntry in sLink:

            sUrl = str(aEntry)
            sHost = []

            if 'jheberg' in aEntry:

                aResult = cJheberg().GetUrls(sUrl)

                if (aResult):
                    if (count >0):
                        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Liens via Jheberg (suite partie vidéo)[/COLOR]')
                    else:
                        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Liens via Jheberg[/COLOR]')
                    count= count +1
                    for aEntry in aResult:
                        if 'nitroflare' not in aEntry:
                            sHost.append(aEntry)

            elif 'multiup' in aEntry:
                 #modif temp org en eu
                 NewUrl = sUrl.replace('http://www.multiup.org/fr/download','http://www.multiup.eu/fr/mirror').replace('http://www.multiup.eu/fr/download','http://www.multiup.eu/fr/mirror').replace('http://www.multiup.org/download', 'http://www.multiup.eu/fr/mirror')

                 aResult = cMultiup().GetUrls(NewUrl)

                 if (aResult):
                     if (count >0):
                         oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Liens via Multiup (suite partie vidéo)[/COLOR]')
                     else:
                         oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Liens via Multiup[/COLOR]')
                     count= count +1
                     for aEntry in aResult:
                         if 'nitroflare' not in aEntry:
                             sHost.append(aEntry)

            elif 'watchvideo' in sUrl:
                  oRequestHandler = cRequestHandler(sUrl)
                  sHtmlContent = oRequestHandler.request();
                  oParser = cParser()
                  sPattern = '{file:"([^"]+)"\,label:"([^"]+)"}'
                  aResult = oParser.parse(sHtmlContent, sPattern)

                  if (aResult[0] == True):
                      if (count2 >0):
                          oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Liens via WatchVideo (suite partie vidéo)[/COLOR]')
                      else:
                          oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Liens via WatchVideo[/COLOR]')
                      count2 = count2 +1
                      for aEntry in aResult[1]:
                          sHost.append(aEntry)

            #si liens directs raptu&uptobox
            else:
                if (count3 == 0):
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Liens divers[/COLOR]')
                count3 = count3 +1
                sHost.append(aEntry)

            if (sHost):

                for aEntry in sHost:
                    if 'watchvideo' in sUrl:
                        sHosterUrl = str(aEntry[0])
                        sQual = str(aEntry[1])
                        sDisplayTitle = ('[%s] %s') % (sQual, sMovieTitle)
                    else:
                        sHosterUrl = str(aEntry)
                        sDisplayTitle = (' %s ') % (sMovieTitle)

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sDisplayTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
