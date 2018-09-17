#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cJheberg
from resources.lib.multihost import cMultiup
from resources.lib.packer import cPacker
from resources.lib.comaddon import progress, VSlog

SITE_IDENTIFIER = 'robindesdroits'
SITE_NAME = 'Robin des Droits'
SITE_DESC = 'Replay sports'

URL_MAIN = 'http://robindesdroits.me/'

SPORT_NEWS = (URL_MAIN + 'derniers-uploads/', 'showMovies')
SPORT_FOOT = (URL_MAIN + 'football/', 'showMovies')
SPORT_US = (URL_MAIN + 'sports-us/', 'showMovies')
SPORT_AUTO = (URL_MAIN + 'sports-automobiles/', 'showMovies')
SPORT_RUGBY = (URL_MAIN + 'rugby/', 'showMovies')
SPORT_TENNIS = (URL_MAIN + 'tennis/', 'showMovies')
SPORT_HAND = (URL_MAIN + 'handball/', 'showMovies')
SPORT_BASKET = (URL_MAIN + 'basketball/', 'showMovies')
SPORT_DIVERS = (URL_MAIN + 'divers/', 'showMovies')
SPORT_SPORTS = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_FOOT[1], 'Football', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_US[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_US[1], 'Sport US', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_AUTO[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_AUTO[1], 'Sport Automobiles', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_RUGBY[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_RUGBY[1], 'Rugby', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_TENNIS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TENNIS[1], 'Tennis', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_HAND[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_HAND[1], 'Handball', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_BASKET[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_BASKET[1], 'Basketball', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_DIVERS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_DIVERS[1], 'Divers', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Genres', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
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
    liste.append( ['[COLOR gold]Football[/COLOR]', '', 'match'] )
    liste.append( ['Ligue 1', URL_MAIN + 'football/ligue-1/', 'match'] )
    liste.append( ['Ligue 2', URL_MAIN + 'football/ligue-2/', 'match'] )
    liste.append( ['Premier ligue', URL_MAIN + 'football/premier-league/', 'match'] )
    liste.append( ['Liga', URL_MAIN + 'football/liga/', 'match'] )
    liste.append( ['Bundesliga', URL_MAIN + 'football/bundesliga/', 'match'] )
    liste.append( ['Série A', URL_MAIN + 'football/serie-a/', 'match'] )
    liste.append( ['UEFA Chammpions League', URL_MAIN + 'football/uefa-champions-league/', 'match'] )
    liste.append( ['UEFA Europa League', URL_MAIN + 'football/uefa-europa-league', 'match'] )
    liste.append( ['Coupe de France', URL_MAIN + 'football/coupe-de-france/', 'match'] )
    liste.append( ['Coupe de la League', URL_MAIN + 'football/coupe-de-la-ligue/', 'match'] )
    liste.append( ['Coupe d\'Angleterre (FA Cup)', URL_MAIN + 'football/coupe-dangleterre/', 'match'] )
    liste.append( ['Coupe de la ligue anglaise (EFL Cup)', URL_MAIN + 'football/coupe-de-la-ligue-anglaise/', 'match'] )
    liste.append( ['Coupe d\'Espagne (Copa del Rey)', URL_MAIN + 'football/coupe-despagne/', 'match'] )
    liste.append( ['Coupe d\'Allemagne (DFB Pokal)', URL_MAIN + 'football/coupe-dallemagne/', 'match'] )
    liste.append( ['Coupe d\'Italie (TIM Cup)', URL_MAIN + 'football/coupe-ditalie/', 'match'] )
    liste.append( ['UEFA Women\'s Champions League', URL_MAIN + 'football/uefa-womens-champions-league/', 'match'] )
    liste.append( ['Equipe de France', URL_MAIN + 'football/equipe-de-france/', 'match'] )

    liste.append( ['[COLOR gold]Emissions de Football[/COLOR]', '', 'tv'] )
    liste.append( ['19h30 PM', URL_MAIN + 'football/19h30-pm/', 'tv'] )
    liste.append( ['Vendredi ligue 1', URL_MAIN + 'football/vendredi-ligue-1/', 'tv'] )
    liste.append( ['Jour de Foot', URL_MAIN + 'football/jour-de-foot/', 'tv'] )
    liste.append( ['PL Zone', URL_MAIN + 'football/pl-zone/', 'tv'] )
    liste.append( ['Télé Foot', URL_MAIN + 'football/emissions-de-football/telefoot/', 'tv'] )
    liste.append( ['CFC', URL_MAIN + 'football/cfc/', 'tv'] )
    liste.append( ['CFC Le Debrief', URL_MAIN + 'football/cfc-le-debrief/', 'tv'] )
    liste.append( ['J+1', URL_MAIN + 'football/j1/', 'tv'] )
    liste.append( ['Club Europe', URL_MAIN + 'football/club-europe/', 'tv'] )
    liste.append( ['19h30 Sport', URL_MAIN + 'football/19h30-sport/', 'tv'] )
    liste.append( ['Club Europe Giga Liga', URL_MAIN + 'football/club-europe-giga-liga/', 'tv'] )
    liste.append( ['Club Europe Tutta Serie A', URL_MAIN + 'football/club-europe-tutta-serie-a/', 'tv'] )
    liste.append( ['Club Europe Die Bulischau', URL_MAIN + 'football/club-europe-die-bulischau/', 'tv'] )
    liste.append( ['Le Décrassage de Luis', URL_MAIN + 'football/le-decrasage-de-luis/', 'tv'] )
    liste.append( ['Champions Show', URL_MAIN + 'football/champions-show/', 'tv'] )

    liste.append( ['[COLOR gold]Sports US[/COLOR]', '', 'match'] )
    liste.append( ['NBA', URL_MAIN + 'sport-us/nba/', 'match'] )
    liste.append( ['NFL', URL_MAIN + 'sport-us/nfl/', 'match'] )

    liste.append( ['[COLOR gold]Emissions de sports US[/COLOR]', '', 'tv'] )
    liste.append( ['NBA Extra', URL_MAIN + 'sport-us/nba-extra/', 'tv'] )

    liste.append( ['[COLOR gold]Sports Automobiles[/COLOR]', '', 'match'] )
    liste.append( ['Formule 1', URL_MAIN + 'sports-automobiles/formule-1/', 'match'] )
    liste.append( ['Formule 2', URL_MAIN + 'sports-automobiles/formule-2/', 'match'] )
    liste.append( ['Formule E', URL_MAIN + 'sports-automobiles/formule-e/', 'match'] )
    liste.append( ['Moto GP', URL_MAIN + 'sports-automobiles/moto-gp/', 'match'] )
    liste.append( ['Moto 2', URL_MAIN + 'sports-automobiles/moto-2/', 'match'] )
    liste.append( ['Moto 3', URL_MAIN + 'sports-automobiles/moto-3/', 'match'] )
    liste.append( ['Indycar', URL_MAIN + 'sports-automobiles/indycar/', 'match'] )

    liste.append( ['[COLOR gold]Emissions de sports Automobiles[/COLOR]', '', 'tv'] )
    liste.append( ['Formula One', URL_MAIN + 'sports-automobiles/formula-one/', 'tv'] )
    liste.append( ['On Board', URL_MAIN + 'sports-automobiles/on-board/', 'tv'] )

    liste.append( ['[COLOR gold]Rugby[/COLOR]', '', 'match'] )
    liste.append( ['Top 14', URL_MAIN + 'rugby/top-14/', 'match'] )
    liste.append( ['Champions Cup', URL_MAIN + 'rugby/champions-cup/', 'match'] )
    liste.append( ['Challenge Cup', URL_MAIN + 'rugby/challenge-cup/', 'match'] )
    liste.append( ['Tournoi des 6 Nations', URL_MAIN + 'rugby/tournoi-des-6-nations/', 'match'] )

    liste.append( ['[COLOR gold]Emissions de Rugby[/COLOR]', '', 'tv'] )
    liste.append( ['Jour de Rugby', URL_MAIN + 'rugby/emissions-de-rugby/jour-de-rugby/', 'tv'] )

    liste.append( ['[COLOR gold]Tennis[/COLOR]', '', 'match'] )
    liste.append( ['Open d\'Australie', URL_MAIN + 'tennis/open-daustralie/', 'match'] )
    liste.append( ['Roland Garros', URL_MAIN + 'tennis/roland-garros/', 'match'] )
    liste.append( ['Wimbledon', URL_MAIN + 'tennis/wimbledon/', 'match'] )

    liste.append( ['[COLOR gold]Handball[/COLOR]', '', 'match'] )
    liste.append( ['Championnat du Monde 2017', URL_MAIN + 'handball/championnat-du-monde-2017/', 'match'] )
    liste.append( ['Euro 2018', URL_MAIN + 'handball/euro-2018/', 'match'] )

    liste.append( ['[COLOR gold]Basketball[/COLOR]', '', 'match'] )
    liste.append( ['Eurobasket 2017', URL_MAIN + 'baskettball/eurobasket-2017/', 'match'] )

    for sTitle, sUrl, sFiltre in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        if 'tv' in sFiltre:
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        else:
            oGui.addDir(SITE_IDENTIFIER, 'showLinkGenres', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="mh-loop-thumb"><a href="([^"]+)"><img src=".+?" style="background:url\(\'(.+?)\'\).+?rel="bookmark">(.+?)</a></h3>'

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
            sThumb = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

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

def showLinkGenres():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sThumb = ''
    try:
        sPattern = '<p style="text-align: center;"><img src="([^"]+)".+?/>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sThumb = aResult[1][0]
    except:
        pass

    sPattern = '<span style="font-family: Arial, Helvetica,.+?font-size: 16pt;">(.+?)</span>|(<h3 class="entry-title mh-loop-title"|<li )><a href="([^"]+)".+?>(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)


    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR gold]' + aEntry[0] + '[/COLOR]')
            else:
                sUrl = aEntry[2]
                sTitle = aEntry[3]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

                oGui.addTV(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    VSlog(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #recup liens clictune
    sPattern = '<a href="(http://www.clictune.+?)".+?<b>(.+?)</b>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sHost = aEntry[1].capitalize()
            
            sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
    
    #Second cas de figure
    if (aResult[0] == False):
        sPattern = '<a href="(http:\/\/zipansion\.com\/[^"]+)">(.+?)<\/a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sUrl = aEntry[0]
                sHost = cUtil().removeHtmlTags(aEntry[1])
                
                sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n', ''))
    #fh.close()

    sPattern = '<b><a href=".+?redirect\/\?url\=(.+?)\&id.+?">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = cUtil().urlDecode(aResult[1][0])

        if 'gounlimited' in sUrl:
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])

                sPattern = '{sources:\["([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    sHosterUrl = aResult[1][0]
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        elif 'jheberg' in sUrl:

            aResult = cJheberg().GetUrls(sUrl)
            if (aResult):
                for aEntry in aResult:
                    sHosterUrl = aEntry

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        elif 'multiup' in sUrl:

            aResult = cMultiup().GetUrls(sUrl)
            
            if (aResult):
                for aEntry in aResult:
                    sHosterUrl = aEntry

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        else:
            sHosterUrl = sUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
