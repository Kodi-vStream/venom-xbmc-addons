# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import siteManager, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil

try:    import json
except: import simplejson as json


SITE_IDENTIFIER = 'daddyhd'
SITE_NAME = 'DaddyHD'
SITE_DESC = 'Chaines de Sport et de Divertissement'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_GENRES = ('schedule/schedule-generated.json', 'showGenres')

# extra stream : schedule-extra-generated.json

TV_TV = ('/', 'load')
SPORT_TV = ('31-site-pour-regarder-les-chaines-de-sport.html', 'showTV')

# chaines
channels = {
    116: ['bein Sports 1', 'https://12.webhd.ru/ddh2/premium116/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/n43EXNeoR62GvZlWW2SXKuQi0GA=/788708-HD1.png'],
    117: ['bein Sports 2', 'https://12.webhd.ru/ddh2/premium117/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/dZ2ESOsGlqynphSgs7MAGLwFAcg=/788711-HD2.png'],
    118: ['bein Sports 3', 'https://12.webhd.ru/ddh2/premium118/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/G4M9yQ3f4vbFINuKGIoeJQ6kF_I=/788712-HD3.png'],
    119: ['RMC Sport 1', 'https://12.webhd.ru/ddh2/premium119/tracks-v1a1/mono.m3u8', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1'],
    120: ['RMC Sport 2', 'https://12.webhd.ru/ddh1/premium120/tracks-v1a1/mono.m3u8', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1'],
    121: ['Canal+', 'https://12.webhd.ru/ddh2/premium121/tracks-v1a1/mono.m3u8', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],
    122: ['Canal+ Sport', 'https://12.webhd.ru/ddh2/premium122/tracks-v1a1/mono.m3u8', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_177.PNG'],
    463: ['Canal+ Foot', 'https://12.webhd.ru/ddy4/premium463/tracks-v1a1/mono.m3u8', 'https://thumb.canalplus.pro/bran/unsafe/870x486/image/62dab6a90b84c/uploads/media/C+FOOT_213x160.png'],
    645: ["L'équipe", 'https://12.webhd.ru/ddy5/premium645/tracks-v1a1/mono.m3u8', 'https://upload.wikimedia.org/wikipedia/commons/4/4a/L%27Equipe_logo.png'],
    318: ["Golf Channel USA", 'https://12.webhd.ru/ddy3/premium318/tracks-v1a1/mono.m3u8', 'https://www.golfchannel.fr/upload/media/golf-channel-600af6fe955c3.png'],
    494: ['bein Sports MAX 4', 'https://12.webhd.ru/ddy5/premium494/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/owLVmBRH9cHk6K9JSocpTw0Oc4E=/788713-4MAX.png'],
    495: ['bein Sports MAX 5', 'https://12.webhd.ru/ddy5/premium495/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/FE2dOGMxn1waqAFYxqsGxXKkvCo=/788714-5MAX.png'],
    496: ['bein Sports MAX 6', 'https://12.webhd.ru/ddy5/premium496/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/beNacZewwA5WqFglPAwOaD4n5QA=/788715-6MAX.png'],
    497: ['bein Sports MAX 7', 'https://12.webhd.ru/ddy5/premium497/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/6IXXUorOrK_n756SjT6a2Ko7jiM=/788716-7MAX.png'],
    498: ['bein Sports MAX 8', 'https://12.webhd.ru/ddy5/premium498/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/6aOfeAugcgMy93nrOfk8NAacALs=/788717-8MAX.png'],
    499: ['bein Sports MAX 9', 'https://12.webhd.ru/ddy5/premium499/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/etM_TIm1DmhWr0TZ_CbWGJvaTdQ=/788718-9MAX.png'],
    500: ['bein Sports MAX 10', 'https://12.webhd.ru/ddy5/premium500/tracks-v1a1/mono.m3u8', 'https://images.beinsports.com/LxFG3ZG88jlFsOyWo_C7o4mdY7M=/788719-10MAX.png']
    }



# PROBLEME DE DEBIT et fait planter kodi


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines TV Sports', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()
    oHosterGui = cHosterGui()
    hosterLienDirect = oHosterGui.getHoster('lien_direct')

    chaines = [116, 117, 118, 119, 120, 121, 122, 463, 645, 318, 494, 495, 496, 497, 498, 499, 500]

    for iChannel in chaines:
        channel = channels.get(iChannel)
        sDisplayTitle = channel[0]
        sUrl = channel[1] + '|referer=https://weblivehdplay.ru/'
        sThumb = channel[2]
        hosterLienDirect.setDisplayName(sDisplayTitle)
        hosterLienDirect.setFileName(sDisplayTitle)
        oHosterGui.showHoster(oGui, hosterLienDirect, sUrl, sThumb)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    result = json.loads(sHtmlContent)

    sportGenre = {}
    bMatrix = isMatrix()
    for days in result:
        shows = result[days]
        for sTitle in shows:
            if 'Tv Show' in sTitle:
                continue
            
            if not bMatrix:
                sTitle = sTitle.decode('utf-8', 'ignore')

            sDisplayTitle = str(sTitle) # conversion Unicode -> String

            sDisplayTitle = sDisplayTitle.replace('Soccer', 'Football')
            sDisplayTitle = sDisplayTitle.replace('Darts', 'Flechettes')
            sDisplayTitle = sDisplayTitle.replace('Boxing', 'Boxe')
            sDisplayTitle = sDisplayTitle.replace('Cycling', 'Cyclisme')
            sDisplayTitle = sDisplayTitle.replace('Horse Racing', 'Course de chevaux')
            sDisplayTitle = sDisplayTitle.replace('Ice Hockey', 'Hockey sur glace')
            sDisplayTitle = sDisplayTitle.replace('Alpine Ski', 'Ski')
            sDisplayTitle = sDisplayTitle.replace('Rugby Union', 'Rugby à XV')
            sDisplayTitle = sDisplayTitle.replace('Sailing / Boating', 'Voile')
            
            if sDisplayTitle in sportGenre:
                continue
            sportGenre[sDisplayTitle] = sTitle

    for sDisplayTitle, sTitle in sorted(sportGenre.items()):
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
        oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, 'genres.png',  '', sTitle, oOutputParameterHandler)

            
    oGui.setEndOfDirectory()


def showMovies():

    oGui = cGui()
    oUtil = cUtil()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    result = json.loads(sHtmlContent)

#    mois = ['filler', 'January', 'February', 'March', 'April', 'May', 'June', 'juilly', 'aout', 'September', 'October', 'November', 'December']
    for days in result:
        
#Wednesday 27th December 2023 - Schedule Time UK GMT+1
        # date = days.strip().split(' ')
        # numJour = date[1][0:-2]
        # numMois = mois.index(date[2])

        shows = result[days]
        for showName in shows:
            if showName != sMovieTitle:
                continue

            show = shows[showName]
            for events in show:
                timeEvent = events['time']
                heure, minute = timeEvent.split(':')
                heure = int(heure)
                heure = 0 if heure == 23 else heure +1
#                dateEvent = '%s/%s' % (numJour, numMois)
#                time = '%s %s' % (dateEvent, timeEvent)
                time = '%02d:%s' % (heure, minute)
                sTitle = events['event']
                sTitle = oUtil.formatUTF8(sTitle)
                
                sDisplayTitle = '%s - %s' % (time, sTitle)
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
                oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, 'sport.png',  '', sTitle, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    result = json.loads(sHtmlContent)

    for days in result:
        shows = result[days]
        for showName in shows:
            show = shows[showName]
            for events in show:
                timeEvent = events['time']
                eventName = events['event']
                
                if sMovieTitle != eventName:
                    continue

                heure, minute = timeEvent.split(':')
                heure = int(heure)
                heure = 0 if heure == 23 else heure +1
                time = '%02d:%s' % (heure, minute)
            
                channels = events['channels']
                for channel in channels:
                    channelName = channel['channel_name']
                    channelId = channel['channel_id']
            
                    sDisplayTitle = '%s - %s [%s]' % (time, eventName[0:30], channelName)
                    oOutputParameterHandler.addParameter('siteUrl', channelId)
                    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                    oOutputParameterHandler.addParameter('sDesc', eventName)
        
                    oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'sport.png', eventName, oOutputParameterHandler)
            
            
    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oHosterGui = cHosterGui()
    hosterLienDirect = oHosterGui.getHoster('lien_direct')

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    channel = oInputParameterHandler.getValue('siteUrl')

    sDisplayTitle = sMovieTitle.replace('[', '[1 - ')
    sUrl = 'https://12.webhd.ru/ddh1/premium%s/tracks-v1a1/mono.m3u8' % channel
    sUrl = sUrl + '|referer=https://weblivehdplay.ru/'
    hosterLienDirect.setDisplayName(sDisplayTitle)
    hosterLienDirect.setFileName(sDisplayTitle)
    oHosterGui.showHoster(oGui, hosterLienDirect, sUrl, '')

    sDisplayTitle = sMovieTitle.replace('[', '[2 - ')
    sUrl = 'https://12.webhd.ru/ddh2/premium%s/tracks-v1a1/mono.m3u8' % channel
    sUrl = sUrl + '|referer=https://weblivehdplay.ru/'
    hosterLienDirect.setDisplayName(sDisplayTitle)
    hosterLienDirect.setFileName(sDisplayTitle)
    oHosterGui.showHoster(oGui, hosterLienDirect, sUrl, '')

    sDisplayTitle = sMovieTitle.replace('[', '[3 - ')
    sUrl = 'https://12.webhd.ru/ddy2/premium%s/tracks-v1a1/mono.m3u8' % channel
    sUrl = sUrl + '|referer=https://weblivehdplay.ru/'
    hosterLienDirect.setDisplayName(sDisplayTitle)
    hosterLienDirect.setFileName(sDisplayTitle)
    oHosterGui.showHoster(oGui, hosterLienDirect, sUrl, '')

    sDisplayTitle = sMovieTitle.replace('[', '[4 - ')
    sUrl = 'https://12.webhd.ru/ddy3/premium%s/tracks-v1a1/mono.m3u8' % channel
    sUrl = sUrl + '|referer=https://weblivehdplay.ru/'
    hosterLienDirect.setDisplayName(sDisplayTitle)
    hosterLienDirect.setFileName(sDisplayTitle)
    oHosterGui.showHoster(oGui, hosterLienDirect, sUrl, '')

    sDisplayTitle = sMovieTitle.replace('[', '[5 - ')
    sUrl = 'https://12.webhd.ru/ddy4/premium%s/tracks-v1a1/mono.m3u8' % channel
    sUrl = sUrl + '|referer=https://weblivehdplay.ru/'
    hosterLienDirect.setDisplayName(sDisplayTitle)
    hosterLienDirect.setFileName(sDisplayTitle)
    oHosterGui.showHoster(oGui, hosterLienDirect, sUrl, '')

    sDisplayTitle = sMovieTitle.replace('[', '[6 - ')
    sUrl = 'https://12.webhd.ru/ddy5/premium%s/tracks-v1a1/mono.m3u8' % channel
    sUrl = sUrl + '|referer=https://weblivehdplay.ru/'
    hosterLienDirect.setDisplayName(sDisplayTitle)
    hosterLienDirect.setFileName(sDisplayTitle)
    oHosterGui.showHoster(oGui, hosterLienDirect, sUrl, '')
            
    sDisplayTitle = sMovieTitle.replace('[', '[7 - ')
    sUrl = 'https://12.webhd.ru/esx3/premium%s/tracks-v1a1/mono.m3u8' % channel
    sUrl = sUrl + '|referer=https://weblivehdplay.ru/'
    hosterLienDirect.setDisplayName(sDisplayTitle)
    hosterLienDirect.setFileName(sDisplayTitle)
    oHosterGui.showHoster(oGui, hosterLienDirect, sUrl, '')
            
    oGui.setEndOfDirectory()

