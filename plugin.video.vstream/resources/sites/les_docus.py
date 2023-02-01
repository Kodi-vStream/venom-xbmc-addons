# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager

SITE_IDENTIFIER = 'les_docus'
SITE_NAME = 'Les docus'
SITE_DESC = 'Documentaires reportages et vidéos en streaming en francais.'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DOC_DOCS = (True, 'load')
DOC_GENRES = (True, 'showGenres')
DOC_NEWS = (URL_MAIN, 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['[COLOR teal]ARTS[/COLOR]', 'arts/'])
    liste.append(['Architecture', 'arts/architecture/'])
    liste.append(['Cinéma', 'arts/cinema/'])
    liste.append(['Dessin', 'arts/dessin/'])
    liste.append(['Littérature', 'arts/litterature/'])
    liste.append(['Musique', 'arts/musique/'])
    liste.append(['Peinture', 'arts/peinture/'])
    liste.append(['Sculpture', 'arts/sculpture/'])

    liste.append(['[COLOR teal]HISTOIRE[/COLOR]', 'histoire/'])
    liste.append(['Préhistoire', 'histoire/prehistoire/'])
    liste.append(['Antiquité', 'histoire/antiquite/'])
    liste.append(['Moyen age', 'histoire/moyen-age/'])
    liste.append(['Temps modernes', 'histoire/temps-modernes/'])
    liste.append(['Temps révolutionnaires', 'histoire/temps-revolutionnaires/'])
    liste.append(['19 eme siecle', 'histoire/19eme-siecle/'])
    liste.append(['20 eme siecle', 'histoire/20eme-siecle/'])
    liste.append(['Epoque contemporaine', 'histoire/epoque-contemporaine/'])

    liste.append(['[COLOR teal]SOCIETE[/COLOR]', 'societe/'])
    liste.append(['Argent', 'societe/argent/'])
    liste.append(['Monde', 'societe/monde/'])
    liste.append(['Politique', 'societe/politique/'])
    liste.append(['Sexualité', 'societe/sexualite/'])
    liste.append(['Social', 'societe/social/'])

    liste.append(['[COLOR teal]SCIENCES[/COLOR]', 'sciences/'])
    liste.append(['Astronomie', 'sciences/astronomie/'])
    liste.append(['Ecologie', 'sciences/ecologie/'])
    liste.append(['Economie', 'sciences/economie/'])
    liste.append(['Génétique', 'sciences/genetique/'])
    liste.append(['Géographie', 'sciences/geographie/'])
    liste.append(['Géologie', 'sciences/geologie/'])
    liste.append(['Mathématiques', 'sciences/mathematique/'])
    liste.append(['Médecine', 'sciences/medecine/'])
    liste.append(['Physique', 'sciences/physique/'])
    liste.append(['Psychologie', 'sciences/psychologie/'])

    liste.append(['[COLOR teal]TECHNOLOGIE[/COLOR]', 'technologie/'])
    liste.append(['Aviation', 'technologie/aviation/'])
    liste.append(['Informatique', 'technologie/informatique/'])
    liste.append(['Marine', 'technologie/marine/'])
    liste.append(['Téléphonie', 'technologie/telephonie'])

    liste.append(['[COLOR teal]PARANORMAL[/COLOR]', 'paranormal/'])
    liste.append(['Fantames et esprits', 'paranormal/fantomes-et-esprits/'])
    liste.append(['OVNI et extraterrestres', 'paranormal/ovnis-et-extraterrestres/'])
    liste.append(['Cryptozoologie', 'paranormal/cryptozoologie/'])
    liste.append(['Mysteres et legendes', 'paranormal/mysteres-et-legendes/'])
    liste.append(['Divers', 'paranormal/divers/'])

    liste.append(['[COLOR teal]AUTRES[/COLOR]', 'autres/'])
    liste.append(['Animaux', 'autres/animaux/'])
    liste.append(['Gastronomie', 'autres/gastronomie/'])
    liste.append(['Jeux video', 'autres/jeux-video/'])
    liste.append(['Loisirs', 'autres/loisirs/'])
    liste.append(['Métiers', 'autres/metiers/'])
    liste.append(['Militaire', 'autres/militaire/'])
    liste.append(['Nature', 'autres/nature/'])
    liste.append(['Policier', 'autres/policier/'])
    liste.append(['Religion', 'autres/religion/'])
    liste.append(['Santé', 'autres/sante/'])
    liste.append(['Sport', 'autres/sport/'])
    liste.append(['Voyage', 'autres/voyage/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch.replace(" ", "+")
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'post-header"><a href="([^"]+)" title="([^"]+).+?src="(https[^"]+)".+?<p *style.+?>([^<]+)</p>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]
            sDesc = aEntry[3]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a> *<a *class="next page-numbers" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent1 = re.sub('<iframe.+?src="(.+?amazon.+?)"', '', sHtmlContent)

    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent1, sPattern)

    if not (aResult[0] is True):
        sPattern = 'data-video_id="(.+?)"'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            sHosterUrl = 'https://www.youtube.com/embed/' + aResult[1][0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        else:
            sPattern = '<iframe.+?data-src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        for aEntry in list(set(aResult[1])):
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
