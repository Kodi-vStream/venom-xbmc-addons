#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
import base64
import re,urllib2


SITE_IDENTIFIER = 'navixsport_com'
SITE_NAME = 'Navixsport'
SITE_DESC = 'live stream sports'

URL_MAIN = 'http://www.navixsport.com/'

SPORT_SPORTS = ('http://url', 'showLive')

#Url menu
PREMIER_LEAGUE = URL_MAIN + 'matches.php?league=epl'
LIGUE_CHAMPION = URL_MAIN + 'matches.php?league=cl'
SERIE_A = URL_MAIN + 'matches.php?league=serie'
LA_LIGA = URL_MAIN + 'matches.php?league=lfp'
NBA = URL_MAIN + 'matches.php?league=nba'
NHL = URL_MAIN + 'matches.php?league=nhl'

sLive = '[COLOR coral][Live] [/COLOR]'

UA = '|User-Agent=Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'

headers = { 'User-Agent' : UA }

def load():

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Live Sports', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLive():

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', PREMIER_LEAGUE)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sLive + 'Premier League', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', LIGUE_CHAMPION)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sLive + 'UEFA Champions League', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', LA_LIGA)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sLive + 'La Liga', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_A)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sLive + 'Série A', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NBA)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sLive + 'NBA Games', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NHL)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sLive + 'NHL Games', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):

    oGui = cGui()

    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Programme des Matchs[/COLOR]')

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)"><li id=.+?><div>(.+?)</div><img src="([^"]+)".+?<img src=.+?<img src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            #Recup Nom Team
            sUrl2 = URL_MAIN + aEntry[0]
            sTitle = aEntry[2] + '[COLOR gray]' +  ' vs ' + '[/COLOR]' + aEntry[3]
            sTitle =sTitle.replace('img/teams/', '').replace('.png', '')

            #Affichage custom Titre Player
            sMovieTitle2 = '[Live] ' + sTitle

            #Affiche sThumb 1ere equipe
            sThumb = URL_MAIN + aEntry[2]
            sThumb = sThumb.replace(' ', '%20')

            #Horaires
            sPattern = '<font color="#46AAE3">(.+?)<font color="grey">(.+?)</font>'

            aResult = re.findall(sPattern, aEntry[1])

            if (aResult):
               for aEntry in aResult:
                   sTime = '[COLOR teal]' + aEntry[0] + aEntry[1] + ' GMT' + '  ' + '[/COLOR]'
                   sTitle = sTime + sTitle

            #Test si live en cours
            if 'STARTED'  in aEntry[1]:

                sTitle = '[COLOR coral]' + '[Live en cours]  ' + '[/COLOR]' + sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sMovieTitle2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER, '(Aucune diffusion prévue pour le moment)')

    if not sSearch:
        oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumb  = oInputParameterHandler.getValue('sThumb')

    oGui.addText(SITE_IDENTIFIER, sMovieTitle)

    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles:[/COLOR]')

    if '[Live' in sMovieTitle:

       request = urllib2.Request(sUrl,None,headers)
       reponse = urllib2.urlopen(request)
       sHtmlContent = reponse.read()
       reponse.close()

       sPattern = '<source src="(.+?)" type="video/mp4"/>'

       oParser = cParser()
       aResult = oParser.parse(sHtmlContent, sPattern)

       #si blocage site limite visiteur ou erreur
       #on force live via lien direct bypass
       if (aResult[0] == True):

           url = aResult[1][0] + UA
           sTitle = 'Navixsport 720p'

       else:
           sTitle = 'Navixsport [bypass] 720p'
           bypass = 'aHR0cDovLzE5NS4xNTQuMjUyLjIyMi9obHMtbGl2ZS9saXZlcGtncnIvX2RlZmluc3RfL215bGl2ZWV2ZW50L215bGl2ZXN0cmVhbS5tM3U4fFVzZXItQWdlbnQ9TW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDQuMi4yOyBOZXh1cyA0IEJ1aWxkL0pEUTM5KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNTMuMC4yNzg1LjEyNCBNb2JpbGUgU2FmYXJpLzUzNy4zNiApIENocm9tZS8xOC4wLjEwMjUuMTMzIE1vYmlsZSBTYWZhcmkvNTM1LjE5'

           s = base64.b64decode(bypass)
           url = s + UA

    else:
        url = ''
        oGui.addText(SITE_IDENTIFIER, '(Live non disponible avant le début du match)')

    if (url):
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle2)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()
