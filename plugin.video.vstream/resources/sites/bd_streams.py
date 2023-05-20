# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser


SITE_IDENTIFIER = 'bd_streams'
SITE_NAME = 'BD Streams'
SITE_DESC = 'Match de foot en direct'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_LIVE = ('/', 'load')
SPORT_GENRES = ('/', 'showGenres')

TV_TV = ('/', 'load')


def load():
    oGui = cGui()
    sUrl = URL_MAIN

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "<li class='archivedate'><a href='(.+?)'>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sUrl = aResult[1][0]
        sPattern = "<h3 class='post-title.+?href='(.+?)'.+?snippetized'>(.+?)<"
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if not aResult[0]:
            oGui.addText(SITE_IDENTIFIER)
        else:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                sUrl = aEntry[0]
                sTitle = aEntry[1].replace(' vs ', ' / ')
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sTitle)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'load', 'Football', 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()



def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "<iframe .+? src='.+?mid=([^&]+)&"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        sUrl2 = "https://dszbok.com/prod-api/match/detail?type=1&pid=6&langtype=en&mid=" + aResult[1][0]
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sDesc', sTitle)

        oGui.addLink(SITE_IDENTIFIER, 'showLink', sTitle, "sport.png", sTitle, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()




def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    result = json.loads(sHtmlContent)

    if result['msg'] == 'ok':
        data = result['data']
        matchinfo = data['matchinfo']
        
        if matchinfo['status'] == 2:
            oGui.addText(SITE_IDENTIFIER, "(" + matchinfo['name'] + ") - Match fini", "none.png")
            sMovieTitle = matchinfo['hteam_name'] + " " + matchinfo['score'] +  " " + matchinfo['ateam_name']
            oGui.addText(SITE_IDENTIFIER, sMovieTitle, "sport.png")
        else:
            sDate = matchinfo['matchtime_en']
            mois = ['filler', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            try:
                sDateTime = re.findall('(\w+) (\d+), (\d+) (\d+):(\d+):(\d+)', str(sDate))
                if sDateTime:
                    month = mois.index(sDateTime[0][0])
                    hour = int(sDateTime[0][3])
                    hour = (hour + 6)%24;
                    sDate = " (" + matchinfo['name'] + ") - " + '%02d/%02d - %02d:%02d' % (int(sDateTime[0][1]), month, hour, int(sDateTime[0][4]))
                    oGui.addText(SITE_IDENTIFIER, sDate, "annees.png")
            except Exception as e:
                pass
            
            urls = matchinfo['global_live_urls']
            for url in urls[::-1]:
                sHosterUrl = url['url'] + '|referer=https://player.huminbird.cn/'
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    sDisplayTitle = sMovieTitle + " [" + url['name'] + "]"
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sDisplayTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()
