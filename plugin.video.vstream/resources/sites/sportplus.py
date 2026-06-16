# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import time
import datetime

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler


SITE_IDENTIFIER = 'sportplus'
SITE_NAME = 'Sport +'
SITE_DESC = 'Regarder le sport en direct'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_API = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_API')

SPORT_SPORTS = (True, 'load')
SPORT_GENRES = ('v3/fr/sidebar.json', 'showGenres')
SPORT_LIVE = ('v3.1/matches/index?fw=3.1&lang=fr&offset=7200&sport_id=top', 'showLive')  # streaming Actif

HEURE_HIVER = False


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Par genres', 'genre_sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'En cours', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in sorted(sHtmlContent, key=lambda genre: genre['name']):
        if 'type' in genre:
            continue
        sUrl = genre['alias']
        sTitle = genre['name']
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLive():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    tournaments = sHtmlContent['resolve']['mapTournaments']
    t2 = {}
    for t in tournaments:
        t2[t] = tournaments[t]['alias']
    tournaments = t2

    oOutputParameterHandler = cOutputParameterHandler()
    for item in sHtmlContent['items']:
        sTitle = item['name']
        sportId = item['sport_id']
        sUrl = 'id=%s&sport_id=%s' % (item['id'], sportId)
        sDate = item['start']
        sDisplayTitle = sTitle
        if sDate:
            # Parse avec timezone
            dt = datetime.datetime(*(time.strptime(sDate[:19], '%Y-%m-%dT%H:%M:%S')[0:6]))
            # Timezone France
            dt = dt - datetime.timedelta(hours= (2 if HEURE_HIVER else 1))
            # Conversion
            sDate = dt.strftime("%d/%m %H:%M")
            sDisplayTitle = ('%s - %s') % (sDate, sTitle)
        
        tournamentId = item['tournament_id']
        if tournamentId:
            tournamentId = str(tournamentId)
            tournament = tournaments.get(tournamentId, None)
            sUrl += '&tournament_id=' + (tournament if tournament else tournamentId)
            if tournament:
                sDisplayTitle += ' [COLOR yellow][%s][/COLOR]' % tournament.replace('-', ' ').upper()

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sportId = oInputParameterHandler.getValue('siteUrl')
    sUrl = URL_API + 'v3.1/matches/index?fw=3.1&lang=fr&offset=7200&sport_id=' + sportId

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    tournaments = sHtmlContent['resolve']['mapTournaments']
    t2 = {}
    for t in tournaments:
        t2[t] = tournaments[t]['alias']
    tournaments = t2

    oOutputParameterHandler = cOutputParameterHandler()
    for item in sHtmlContent['items']:
        taglive = item['status'] == 'live'
        sTitle = item['name']
        sUrl = 'id=%s&sport_id=%s' % (item['id'], sportId)
        sDate = item['start']
        sDisplayTitle = sTitle
        if sDate:
            # Parse avec timezone
            dt = datetime.datetime(*(time.strptime(sDate[:19], '%Y-%m-%dT%H:%M:%S')[0:6]))
            # Timezone France
            dt = dt - datetime.timedelta(hours= (2 if HEURE_HIVER else 1))
            # Conversion
            sDate = dt.strftime("%d/%m %H:%M")
            sDisplayTitle = ('%s - %s') % (sDate, sTitle)
        
        tournamentId = item['tournament_id']
        if tournamentId:
            tournamentId = str(tournamentId)
            tournament = tournaments.get(tournamentId, None)
            sUrl += '&tournament_id=' + (tournament if tournament else tournamentId)
            if tournament:
                sDisplayTitle += ' [COLOR yellow][%s][/COLOR]' % tournament.replace('-', ' ').upper()

        if taglive:
            sDisplayTitle += ' [COLOR green][En cours][/COLOR]'

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl = URL_API + 'v3.1/matches/view?' + sUrl +'&lang=fr&fw=3.1&has_regions=0'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    item = sHtmlContent['item']
    if item:
        oHoster = cHosterGui().checkHoster(".m3u8")
        links = item.get('ls')
        if links:
            for sHosterUrl in links:
                oHoster.setDisplayName(sMovieTitle)  # nom affiche
                oHoster.setFileName(sMovieTitle)  # idem
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
