#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
#from resources.lib.util import cUtil
import re

#Ce site a des probleme en http/1.1 >> incomplete read error
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

SITE_IDENTIFIER = 'adkami_com'
SITE_NAME = 'ADKami'
SITE_DESC = 'Bienvenue sur ADKami un site Animés Manga & Série en streaming.'

URL_MAIN = 'https://www.adkami.com/'

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN + 'anime', 'showMovies')
ANIM_VIEWS = (URL_MAIN + 'video?search=&t=0&order=3', 'showMovies')
ANIM_LIST = (URL_MAIN + 'anime', 'showAZ')
#ANIM_GENRES = (URL_MAIN + 'video?search=&t=0', 'showMovies')

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN + 'serie', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'video?search=&t=1&order=3', 'showMovies')
SERIE_LIST = (URL_MAIN + 'serie', 'showAZ')
#SERIE_GENRES = (URL_MAIN + 'video?search=&t=1', 'showMovies')

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
    oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], 'Animés (Les Plus Vus)', 'animes_views.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    # oOutputParameterHandler.addParameter('type2', 0)
    # oOutputParameterHandler.addParameter('title', 'Animés')
    # oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'series_az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les Plus Vus)', 'series_views.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    # oOutputParameterHandler.addParameter('type2', 1)
    # oOutputParameterHandler.addParameter('title', 'Séries')
    # oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

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
    #sVersion = oInputParameterHandler.getValue('version')
    sType2 = oInputParameterHandler.getValue('type2')

    liste = []
    liste.append( ['Action', URL_MAIN + 'video?recherche=&genre3=1&type2=' + str(sType2)] )
    liste.append( ['Aventure', URL_MAIN + 'video?recherche=&genre3=2&type2=' + str(sType2)] )
    liste.append( ['Amour & Amitié', URL_MAIN + 'video?recherche=&genre3=3&type2=' + str(sType2)] )
    liste.append( ['Combat', URL_MAIN + 'video?recherche=&genre3=4&type2=' + str(sType2)] )
    liste.append( ['Comédie', URL_MAIN + 'video?recherche=&genre3=5&type2=' + str(sType2)] )
    liste.append( ['Contes & Récits', URL_MAIN + 'video?recherche=&genre3=6&type2=' + str(sType2)] )
    liste.append( ['Cyber & Mecha', URL_MAIN + 'video?recherche=&genre3=7&type2=' + str(sType2)] )
    liste.append( ['Dark Fantasy', URL_MAIN + 'video?recherche=&genre3=8&type2=' + str(sType2)] )
    liste.append( ['Drame', URL_MAIN + 'video?recherche=&genre3=9&type2=' + str(sType2)] )
    liste.append( ['Ecchi', URL_MAIN + 'video?recherche=&genre3=10&type2=' + str(sType2)] )
    liste.append( ['Éducatif', URL_MAIN + 'video?recherche=&genre3=11&type2=' + str(sType2)] )
    liste.append( ['Énigme & Policier', URL_MAIN + 'video?recherche=&genre3=12&type2=' + str(sType2)] )
    liste.append( ['Épique & Héroique', URL_MAIN + 'video?recherche=&genre3=13&type2=' + str(sType2)] )
    liste.append( ['Espace & Sci-Fiction', URL_MAIN + 'video?recherche=&genre3=14&type2=' + str(sType2)] )
    liste.append( ['Familial & Jeunesse', URL_MAIN + 'video?recherche=&genre3=15&type2=' + str(sType2)] )
    liste.append( ['Fantastique & Mythe', URL_MAIN + 'video?recherche=&genre3=16&type2=' + str(sType2)] )
    liste.append( ['Hentai', URL_MAIN + 'video?recherche=&genre3=17&type2=' + str(sType2)] )
    liste.append( ['Historique', URL_MAIN + 'video?recherche=&genre3=18&type2=' + str(sType2)] )
    liste.append( ['Horreur', URL_MAIN + 'video?recherche=&genre3=19&type2=' + str(sType2)] )
    liste.append( ['Magical Girl', URL_MAIN + 'video?recherche=&genre3=20&type2=' + str(sType2)] )
    liste.append( ['Musical', URL_MAIN + 'video?recherche=&genre3=21&type2=' + str(sType2)] )
    liste.append( ['Psychologique', URL_MAIN + 'video?recherche=&genre3=22&type2=' + str(sType2)] )
    liste.append( ['Sport', URL_MAIN + 'video?recherche=&genre3=23&type2=' + str(sType2)] )
    liste.append( ['Tranche de vie', URL_MAIN + 'video?recherche=&genre3=24&type2=' + str(sType2)] )
    liste.append( ['Shôjo-Ai', URL_MAIN + 'video?recherche=&genre3=25&type2=' + str(sType2)] )
    liste.append( ['Shônen-Ai', URL_MAIN + 'video?recherche=&genre3=26&type2=' + str(sType2)] )
    liste.append( ['Yaoi/BL', URL_MAIN + 'video?recherche=&genre3=27&type2=' + str(sType2)] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0, 27):
        cConfig().updateDialog(dialog, 36)
        if dialog.iscanceled():
            break

        if (i < 1):
            sTitle = '123'
        else:
            sTitle = chr(64 + i)
        cConfig().log(sUrl)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sLetter', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showList', '[COLOR teal] Lettre [COLOR red]' + sTitle + '[/COLOR][/COLOR]', 'series_az.png', oOutputParameterHandler)

    cConfig().finishDialog(dialog)

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
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = str(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if '/anime/' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showEpisode', sTitle, 'animes.png', oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showEpisode', sTitle, 'series.png', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showMoviesAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sAZ = oInputParameterHandler.getValue('sLetter')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<li><a href="([^<]+)">.+?<span class="bold">(.+?)</span></p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if len(sAZ)>0 and aEntry[1].upper()[0] == sAZ :

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
                oGui.addDir(SITE_IDENTIFIER, 'showEpisode', sTitle, 'az.png', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

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
    sPattern = '<span class="top"><a href="([^"]+)"><span class="title">([^<>]+)<\/span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = str(aEntry[0])
            sTitle = str(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if 't=1' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'series.png', '', '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'animes.png', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sThumb = ''
    sDesc = ''

    #info anime et serie
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
        dialog = cConfig().createDialog(SITE_NAME)
        cConfig().updateDialog(dialog, 1)

        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Animé licencié' + '[/COLOR]')

        cConfig().finishDialog(dialog)

    else:

        sPattern = '<li class="saison">([^<>]+)</li>|<a href="(https:\/\/www\.adkami\.com[^"]+)"[^<>]+>([^<>]+)<\/a><\/li>'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            total = len(aResult[1])
            dialog = cConfig().createDialog(SITE_NAME)
            for aEntry in aResult[1]:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                    break

                if aEntry[0]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]).capitalize() + '[/COLOR]')
                else:
                    sUrl = str(aEntry[1])
                    sTitle = sMovieTitle + ' ' + aEntry[2]
                    sTitle = re.sub(' vf',' [VF]', sTitle, re.IGNORECASE)
                    sTitle = re.sub(' vostfr',' [VOSTFR]', sTitle, re.IGNORECASE)

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle , 'series.png', sThumb, sDesc, oOutputParameterHandler)

            cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #cConfig().log(sUrl)

    sPattern = '<div class="video-video"><iframe[^<>]+src="([^"]+)"|<a rel="nofollow" target="_back" href="([^"]+)" [^<>]+">[^<>]+Redirection<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if (aEntry[0]):
                sHosterUrl = str(aEntry[0])
            else:
                sHosterUrl = str(aEntry[1])

            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()
