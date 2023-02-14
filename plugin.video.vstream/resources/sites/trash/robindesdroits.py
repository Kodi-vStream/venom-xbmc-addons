# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

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
from resources.lib.util import Unquote

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
SPORT_DIVERS = (URL_MAIN + 'docus-et-divers/', 'showMovies')
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
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_FOOT[1], 'Football', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_RUGBY[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_RUGBY[1], 'Rugby', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_BASKET[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_BASKET[1], 'Basketball', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_AUTO[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_AUTO[1], 'Sport Automobiles', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_US[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_US[1], 'Sport US', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_TENNIS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TENNIS[1], 'Tennis', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_HAND[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_HAND[1], 'Handball', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Football', SPORT_FOOT[0], 'Matchs de Football'])
    liste.append(['Football (Emissions)', SPORT_FOOT[0], 'Emissions de Football'])

    liste.append(['Rugby', SPORT_RUGBY[0], 'Matchs de Rugby'])
    liste.append(['Rugby (Emissions)', SPORT_RUGBY[0], 'Emissions de Rugby'])

    liste.append(['Basketball', SPORT_BASKET[0], 'BASKETBALL'])

    liste.append(['Sports Automobiles', SPORT_AUTO[0], 'Courses de Sports Mécaniques'])
    liste.append(['Sports Automobiles (Emissions)', SPORT_AUTO[0], 'Emissions de Sports Mécaniques'])

    liste.append(['Sports US', SPORT_US[0], 'Matchs de Sports US'])
    liste.append(['Sports US (Emissions)', SPORT_US[0], 'Emissions de Sports US'])

    liste.append(['Tennis (Grand Chelem)', SPORT_TENNIS[0], 'Grand Chelem'])
    liste.append(['Tennis (ATP)', SPORT_TENNIS[0], 'ATP Masters 1000'])
#     liste.append(['Tennis', SPORT_TENNIS[0], 'ATP Finals'])

    liste.append(['Handball', SPORT_HAND[0], 'HANDBALL'])

    for sTitle, sUrl, sFiltre in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('cat', sFiltre)
        oGui.addDir(SITE_IDENTIFIER, 'showCat', sTitle, 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_DIVERS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_DIVERS[1], 'Documentaires', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showCat():

    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    # siteUrl = oInputParameterHandler.getValue('siteUrl')
    sFiltre = oInputParameterHandler.getValue('cat')

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent, sFiltre, '</ul>')
    sPattern = 'href="([^"]+)">(.+?)</a>'


    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)

            if 'Emissions' in sFiltre:
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'sport.png', oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showLinkGenres', sTitle, 'sport.png', oOutputParameterHandler)
    else:
        oGui.addText(SITE_DESC)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<figure class="mh-loop-thumb"><a href="([^"]+)"><img src=".+?" style="background:url\(\'(.+?)\'\).+?rel="bookmark">(.+?)</a></h3>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:

        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showLink', sTitle, 'sport.png', sThumb, '', oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="next page-numbers" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
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
        sPattern = '<p style="text-align: center;"><img src="([^"]+)".+?</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sThumb = aResult[1][0]
    except:
        pass

    sPattern = '<span style="font-family: Arial, Helvetica,.+?font-size:.+?pt;">([^<>]+)<\/span>|<li ><a href="([^"]+)" title=".+?">([^<>]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            if aEntry[0]:
                title = aEntry[0]
                oGui.addText(SITE_IDENTIFIER, '[COLOR gold]' + title + '[/COLOR]')
            else:
                sUrl = aEntry[1]
                sTitle = aEntry[2]


                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addDir(SITE_IDENTIFIER, 'showLink', sTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'a href="([^"]+)">(?:<span.+?|)<b>([^<]+)</b><'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sHost = cUtil().removeHtmlTags(aEntry[1])

            sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addDir(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def AdflyDecoder(url):
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = "var ysmm = '([^']+)'"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        from base64 import b64decode

        code = aResult[1][0]

        A = ''
        B = ''
        # First pass
        for num in enumerate(code):
            if num % 2 == 0:
                A += code[num]
            else:
                B = code[num] + B

        code = A + B

        # Second pass
        m = 0
        code = list(code)
        while m < len(code):
            if code[m].isdigit():
                R = m + 1
                while R < len(code):
                    if code[R].isdigit():
                        S = int(code[m]) ^ int(code[R])
                        if (S < 10):
                            code[m] = str(S)
                        m = R
                        R = len(code)
                    R += 1
            m += 1

        code = ''.join(code)
        code = b64decode(code)
        code = code[16:]
        code = code[:-16]

        return code

    return ''


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # D'abord on saute les redirections.
    if 'replay.robindesdroits' in sUrl:
        sPattern = 'content="0;URL=([^"]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult:
            sUrl = aResult[1][0]
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

    # Ensuite les sites a la con
    if (True):
        if 'AdF' in sHtmlContent:
            sUrl = AdflyDecoder(sUrl)
            if 'motheregarded' in sUrl:
                sPattern = 'href=(.+?)&dp_lp'
                aResult = oParser.parse(sUrl, sPattern)
                if aResult[0]:
                    sUrl = Unquote(''.join(aResult[1])).decode('utf8')
    
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

    # clictune / mylink / ect ...
    sPattern = '<b><a href=".+?redirect\/\?url\=(.+?)\&id.+?">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] == True:
        sUrl = Unquote(aResult[1][0])

    # Et maintenant le ou les liens

    if 'gounlimited' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = '{sources:\["([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if not aResult[0]:
                sPattern = '\[{src:"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
            
            if aResult[0]:
                sHosterUrl = aResult[1][0]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    elif 'jheberg' in sUrl:
        aResult = cJheberg().GetUrls(sUrl)
        if (aResult):
            for aEntry in aResult:
                sHosterUrl = aEntry

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    elif 'multiup' in sUrl:
        aResult = cMultiup().GetUrls(sUrl)

        if (aResult):
            for aEntry in aResult:
                sHosterUrl = aEntry

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        sHosterUrl = sUrl
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
