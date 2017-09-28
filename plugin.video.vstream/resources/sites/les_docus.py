#-*- coding: utf-8 -*-
#Par jojotango
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
import re
SITE_IDENTIFIER = 'les_docus'
SITE_NAME = 'Les docus'
SITE_DESC = 'Documentaires reportages et vidéos en streaming en francais.'

URL_MAIN = 'http://www.les-docus.com/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DOC_GENRES = (True, 'showGenres')

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_DOCS = ('http://', 'load')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

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
    liste.append( ['[COLOR teal]ARTS[/COLOR]', URL_MAIN + 'arts/'] )
    liste.append( ['Architecture', URL_MAIN + 'arts/architecture/'] )
    liste.append( ['Cinéma', URL_MAIN + 'arts/cinema/'] )
    liste.append( ['Dessin', URL_MAIN + 'arts/dessin/'] )
    liste.append( ['Littérature', URL_MAIN + 'arts/litterature/'] )
    liste.append( ['Musique', URL_MAIN + 'arts/musique/'] )
    liste.append( ['Peinture', URL_MAIN + 'arts/peinture/'] )
    liste.append( ['Sculpture', URL_MAIN + 'arts/sculpture/'] )

    liste.append( ['[COLOR teal]HISTOIRE[/COLOR]', URL_MAIN + 'histoire/'] )
    liste.append( ['Préhistoire', URL_MAIN + 'histoire/prehistoire/'] )
    liste.append( ['Antiquité', URL_MAIN + 'histoire/antiquite/'] )
    liste.append( ['Moyen age', URL_MAIN + 'histoire/moyen-age/'] )
    liste.append( ['Temps modernes', URL_MAIN + 'histoire/temps-modernes/'] )
    liste.append( ['Temps révolutionnaires', URL_MAIN + 'histoire/temps-revolutionnaires/'] )
    liste.append( ['19 eme siecle', URL_MAIN + 'histoire/19eme-siecle/'] )
    liste.append( ['20 eme siecle', URL_MAIN + 'histoire/20eme-siecle/'] )
    liste.append( ['Epoque comtemporaine', URL_MAIN + 'histoire/epoque-contemporaine/'] )

    liste.append( ['[COLOR teal]SOCIETE[/COLOR]', URL_MAIN + 'societe/'] )
    liste.append( ['Argent', URL_MAIN + 'societe/argent/'] )
    liste.append( ['Monde', URL_MAIN + 'societe/monde/'] )
    liste.append( ['Politique', URL_MAIN + 'societe/politique/'] )
    liste.append( ['Sexualité', URL_MAIN + 'societe/sexualite/'] )
    liste.append( ['Social', URL_MAIN + 'societe/social/'] )

    liste.append( ['[COLOR teal]SCIENCES[/COLOR]', URL_MAIN + 'sciences/'] )
    liste.append( ['Astronomie', URL_MAIN + 'sciences/astronomie/'] )
    liste.append( ['Ecologie', URL_MAIN + 'sciences/ecologie/'] )
    liste.append( ['Economie', URL_MAIN + 'sciences/economie/'] )
    liste.append( ['Génétique', URL_MAIN + 'sciences/genetique/'] )
    liste.append( ['Géographie', URL_MAIN + 'sciences/geographie/'] )
    liste.append( ['Géologie', URL_MAIN + 'sciences/geologie/'] )
    liste.append( ['Mathématiques', URL_MAIN + 'sciences/mathematique/'] )
    liste.append( ['Médecine', URL_MAIN + 'sciences/medecine/'] )
    liste.append( ['Physique', URL_MAIN + 'sciences/physique/'] )
    liste.append( ['Psychologie', URL_MAIN + 'sciences/psychologie/'] )

    liste.append( ['[COLOR teal]TECHNOLOGIE[/COLOR]', URL_MAIN + 'technologie/'] )
    liste.append( ['Aviation', URL_MAIN + 'technologie/aviation/'] )
    liste.append( ['Informatique', URL_MAIN + 'technologie/informatique/'] )
    liste.append( ['Marine', URL_MAIN + 'technologie/marine/'] )
    liste.append( ['Téléphonie', URL_MAIN + 'technologie/telephonie'] )

    liste.append( ['[COLOR teal]PARANORMAL[/COLOR]', URL_MAIN + 'paranormal/'] )
    liste.append( ['Fantames et esprits', URL_MAIN + 'paranormal/fantomes-et-esprits/'] )
    liste.append( ['OVNI et extraterrestres', URL_MAIN + 'paranormal/ovnis-et-extraterrestres/'] )
    liste.append( ['Cryptozoologie', URL_MAIN + 'paranormal/cryptozoologie/'] )
    liste.append( ['Mysteres et legendes', URL_MAIN + 'paranormal/mysteres-et-legendes/'] )
    liste.append( ['Divers', URL_MAIN + 'paranormal/divers/'] )

    liste.append( ['[COLOR teal]AUTRES[/COLOR]', URL_MAIN + 'autres/'] )
    liste.append( ['Animaux', URL_MAIN + 'autres/animaux/'] )
    liste.append( ['Gastronomie', URL_MAIN + 'autres/gastronomie/'] )
    liste.append( ['Jeux video', URL_MAIN + 'autres/jeux-video/'] )
    liste.append( ['Loisirs', URL_MAIN + 'autres/loisirs/'] )
    liste.append( ['Métiers', URL_MAIN + 'autres/metiers/'] )
    liste.append( ['Militaire', URL_MAIN + 'autres/militaire/'] )
    liste.append( ['Nature', URL_MAIN + 'autres/nature/'] )
    liste.append( ['Policier', URL_MAIN + 'autres/policier/'] )
    liste.append( ['Religion', URL_MAIN + 'autres/religion/'] )
    liste.append( ['Santé', URL_MAIN + 'autres/sante/'] )
    liste.append( ['Sport', URL_MAIN + 'autres/sport/'] )
    liste.append( ['Voyage', URL_MAIN + 'autres/voyage/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

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

    sPattern = '<div class="post-header">.+?href="([^"]+)" title="([^"]+)">.+?<noscript><img.+?src="([^"]+)".+?<p *style.+?>([^<]+)<\/p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sTitle = aEntry[1]
            sTitle = sTitle.replace('&laquo;','<<').replace('&raquo;','>>').replace('&nbsp;','')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png',  aEntry[2],  aEntry[3], oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a *class="next page-numbers" href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = re.sub('<iframe.+?src="(.+?amazon.+?)".+?</iframe>','',sHtmlContent)

    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not (aResult[0] == True):
        sPattern = 'data-video_id="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHosterUrl = 'https://www.youtube.com/embed/' + aResult[1][0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
    else:
        for aEntry in list(set(aResult[1])):
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
