# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import time
from datetime import datetime

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler


SITE_IDENTIFIER = 'kzstream'
SITE_NAME = 'KZSTREAM'
SITE_DESC = 'Regardez tous vos matchs en direct, gratuitement.'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_API = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_api')

SPORT_SPORTS = (True, 'load')
SPORT_LIVE = ('index.php?table=matches&nocache=1', 'showMovies')

def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Sports (En direct)', 'replay.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    data = oRequestHandler.request(True)

    for day in ['today', 'tomorrow']:
        today = data.get(day, [])
    
        oOutputParameterHandler = cOutputParameterHandler()
        for matche in today:
            sTitle = matche['home']['name']
            sTitle2 = matche['away']['name']
            if sTitle2:
                sTitle += ' / ' + sTitle2
            sUrl = '?action=stream&slug=' + matche['slug']
            sDate = matche['date']
            sTime = matche['time']
            sThumb = matche['compLogo']
            isLive = matche['isLive']
            tournament = matche['competition']
            # hasSources = matche['hasSources']
            sDesc = sTitle
    
            try:
                sDate += ' ' + sTime
                d = datetime(*(time.strptime(sDate, '%Y-%m-%d %H:%M')[0:6]))
                #d += timedelta(hours=1 if HEURE_HIVER else 2)
                sTime = d.strftime("%d/%m/%y %H:%M")
            except Exception:
                pass
            
            sDisplayTitle = sTime + ' - ' + sTitle
    
            if isLive:
                sDisplayTitle += '[COLOR limegreen] - EN COURS[/COLOR]'
                
            if tournament:
                sDisplayTitle += ' [COLOR yellow][%s][/COLOR]' % tournament

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
            oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    data = oRequestHandler.request(True)
    if data['success']:
        oHoster = oHosterGui.getHoster('lien_direct')

        for source in data['sources']:
            sHosterUrl = source.get('url', None)
            if sHosterUrl:
                sDisplayTitle = sMovieTitle
                # sLinkName = source.get('label', None)
                # if sLinkName:
                #     sDisplayTitle += ' [%s]' % sLinkName
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sDisplayTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

