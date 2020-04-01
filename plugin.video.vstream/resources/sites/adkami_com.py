#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress#, VSlog
import re

SITE_IDENTIFIER = 'adkami_com'
SITE_NAME = 'ADKami'
SITE_DESC = 'Bienvenue sur ADKami un site Animés Manga & Série en streaming.'

URL_MAIN = 'https://www.adkami.com/'

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN + 'anime', 'showMovies')
ANIM_VIEWS = (URL_MAIN + 'video?search=&t=0&order=3', 'showMovies')
ANIM_LIST = (URL_MAIN + 'anime', 'showAZ')

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN + 'serie', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'video?search=&t=1&order=3', 'showMovies')
SERIE_LIST = (URL_MAIN + 'serie', 'showAZ')

URL_SEARCH = (URL_MAIN + 'video?search=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

URL_SEARCH_SERIES = (URL_MAIN + 'video?search=', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Liste)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], 'Animés (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sType2 = oInputParameterHandler.getValue('type2')

    liste = []
    liste.append( ['Action', URL_MAIN + 'video?recherche=&genre3=1&type2=' + sType2] )
    liste.append( ['Aventure', URL_MAIN + 'video?recherche=&genre3=2&type2=' + sType2] )
    liste.append( ['Amour & Amitié', URL_MAIN + 'video?recherche=&genre3=3&type2=' + sType2] )
    liste.append( ['Combat', URL_MAIN + 'video?recherche=&genre3=4&type2=' + sType2] )
    liste.append( ['Comédie', URL_MAIN + 'video?recherche=&genre3=5&type2=' + sType2] )
    liste.append( ['Contes & Récits', URL_MAIN + 'video?recherche=&genre3=6&type2=' + sType2] )
    liste.append( ['Cyber & Mecha', URL_MAIN + 'video?recherche=&genre3=7&type2=' + sType2] )
    liste.append( ['Dark Fantasy', URL_MAIN + 'video?recherche=&genre3=8&type2=' + sType2] )
    liste.append( ['Drame', URL_MAIN + 'video?recherche=&genre3=9&type2=' + sType2] )
    liste.append( ['Ecchi', URL_MAIN + 'video?recherche=&genre3=10&type2=' + sType2] )
    liste.append( ['Éducatif', URL_MAIN + 'video?recherche=&genre3=11&type2=' + sType2] )
    liste.append( ['Énigme & Policier', URL_MAIN + 'video?recherche=&genre3=12&type2=' + sType2] )
    liste.append( ['Épique & Héroique', URL_MAIN + 'video?recherche=&genre3=13&type2=' + sType2] )
    liste.append( ['Espace & Sci-Fiction', URL_MAIN + 'video?recherche=&genre3=14&type2=' + sType2] )
    liste.append( ['Familial & Jeunesse', URL_MAIN + 'video?recherche=&genre3=15&type2=' + sType2] )
    liste.append( ['Fantastique & Mythe', URL_MAIN + 'video?recherche=&genre3=16&type2=' + sType2] )
    liste.append( ['Hentai', URL_MAIN + 'video?recherche=&genre3=17&type2=' + sType2] )
    liste.append( ['Historique', URL_MAIN + 'video?recherche=&genre3=18&type2=' + sType2] )
    liste.append( ['Horreur', URL_MAIN + 'video?recherche=&genre3=19&type2=' + sType2] )
    liste.append( ['Magical Girl', URL_MAIN + 'video?recherche=&genre3=20&type2=' + sType2] )
    liste.append( ['Musical', URL_MAIN + 'video?recherche=&genre3=21&type2=' + sType2] )
    liste.append( ['Psychologique', URL_MAIN + 'video?recherche=&genre3=22&type2=' + sType2] )
    liste.append( ['Sport', URL_MAIN + 'video?recherche=&genre3=23&type2=' + sType2] )
    liste.append( ['Tranche de vie', URL_MAIN + 'video?recherche=&genre3=24&type2=' + sType2] )
    liste.append( ['Shôjo-Ai', URL_MAIN + 'video?recherche=&genre3=25&type2=' + sType2] )
    liste.append( ['Shônen-Ai', URL_MAIN + 'video?recherche=&genre3=26&type2=' + sType2] )
    liste.append( ['Yaoi/BL', URL_MAIN + 'video?recherche=&genre3=27&type2=' + sType2] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    for i in range(0, 27):

        if (i < 1):
            sTitle = '123'
        else:
            sTitle = chr(64 + i)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sLetter', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showList', '[COLOR teal] Lettre [COLOR red]' + sTitle + '[/COLOR][/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showList():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sLetter = oInputParameterHandler.getValue('sLetter')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Decoupage pour cibler une partie Film
    sPattern = 'class="video-item-list-days"><h5>Lettre ' + sLetter + '</h5></div>(.+?)<(div id=|div class="col-12 col-l-3")'
    sHtmlContent = oParser.parse(sHtmlContent, sPattern)

    #regex pour listage films sur la partie decoupée
    sPattern = '<span class="top"><a href="([^"]+)"><span class="title">([^<>]+)<\/span>'
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
            sTitle = aEntry[1].decode("unicode_escape").encode("latin-1")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if '/anime/' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showEpisode', sTitle, 'animes.png', oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showEpisode', sTitle, 'series.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

#n'exite plus, plus de films
# def showMoviesAZ():
#     oGui = cGui()
#     oInputParameterHandler = cInputParameterHandler()
#     sUrl = oInputParameterHandler.getValue('siteUrl')
#     sAZ = oInputParameterHandler.getValue('sLetter')

#     oRequestHandler = cRequestHandler(sUrl)
#     sHtmlContent = oRequestHandler.request()
#     sPattern = '<li><a href="([^<]+)">.+?<span class="bold">(.+?)</span></p>'
#     oParser = cParser()
#     aResult = oParser.parse(sHtmlContent, sPattern)
#     if (aResult[0] == True):
#         total = len(aResult[1])
#         progress_ = progress().VScreate(SITE_NAME)
#         for aEntry in aResult[1]:
#             progress_.VSupdate(progress_, total)
#             if progress_.iscanceled():
#                 break

#             if len(sAZ)>0 and aEntry[1].upper()[0] == sAZ :

#                 oOutputParameterHandler = cOutputParameterHandler()
#                 oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
#                 oOutputParameterHandler.addParameter('sMovieTitle', aEntry[1])
#                 oGui.addDir(SITE_IDENTIFIER, 'showEpisode', sTitle, 'az.png', oOutputParameterHandler)

#        progress_.VSclose(progress_)

#     oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<span class="top"><a href="([^"]+)"><span class="title">([^<>]+)<\/span>'
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
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if 't=1' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'series.png', '', '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'animes.png', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #info anime et serie
    sThumb = ''
    sDesc = ''
    try:
        oParser = cParser()
        sPattern = '<img itemprop="image".+?src="([^<]+)">.+?<strong>(.+?)</strong>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sThumb = aResult[1][0][0]
            sDesc = aResult[1][0][1]
            sDesc = sDesc.replace('<br />', '')
    except:
        pass

    oParser = cParser()
    sPattern = 'line-height:200px;font-size:26px;text-align:center;">L.anime est licencié<.p>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Animé licencié[/COLOR]')

    else:
        sPattern = '<li class="saison">([^<>]+)</li>|<a href="(https:\/\/www\.adkami\.com[^"]+)"[^<>]+>([^<>]+)<\/a><\/li>'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            total = len(aResult[1])

            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                if aEntry[0]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0].capitalize() + '[/COLOR]')
                else:
                    sUrl = aEntry[1]
                    sTitle = sMovieTitle + ' ' + aEntry[2]
                    sTitle = re.sub(' vf',' (VF)', sTitle, re.IGNORECASE)
                    sDisplayTitle = re.sub(' vostfr',' (VOSTFR)', sTitle, re.IGNORECASE)
                    sTitle = sDisplayTitle.replace(' (VF)', '').replace(' (VOSTFR)', '')

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle , 'series.png', sThumb, sDesc, oOutputParameterHandler)

            progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '(?:iframe.+?|<div class="video-video".+?)data-src="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        sPattern = '<div class="video-video".+?src="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

    for aEntry in aResult[1]:
        sUrl = aEntry.replace('+', 'plus')
        try:
            sUrl = decodex(sUrl)
        except Exception:
            pass

        if sUrl.startswith('//'):
            sUrl = 'https:' + sUrl

        if 'www.' in sUrl:
            sHost = sUrl.split("/")[2].split('.')[1]
        else:
            sHost = sUrl.split("/")[2].split('.')[0]

        if sHost:
            if "crunchyroll" in str(sHost) or "wakanim" in str(sHost) or "animedigitalnetwork" in str(sHost):
                sTitle = "[COLOR red]Licencié par : %s [/COLOR]" % str(sHost)
            else:
                sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
        else:
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, 'Inconnu')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    #bidouille facile
    sUrl = sUrl.replace('plus', '+')
    sHosterUrl  = sUrl

    if (sHosterUrl):
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()

def decodex(x):
    from itertools import chain
    import base64

    e = base64.b64decode(x.replace('https://www.youtube.com/embed/', ''))
    t = ''
    r = "ETEfazefzeaZa13MnZEe"
    a = 0

    px = chain(e)
    for y in list(px):
        t += chr(int(175 ^ ord(y[0])) - ord(r[a]))
        a = 0 if a > len(r) - 2 else a + 1
    return t
