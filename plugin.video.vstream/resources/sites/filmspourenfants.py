#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog

SITE_IDENTIFIER = 'filmspourenfants'
SITE_NAME = 'Films pour Enfants'
SITE_DESC = 'Des films poétiques pour sensibiliser les enfants aux pratiques artistiques. Des films éducatifs pour accompagner les programmes scolaires'

URL_MAIN = 'https://films-pour-enfants.com/'

ANIM_ENFANTS = ('http://', 'load')

AGE_3ANS = (URL_MAIN + 'films-enfants-3-ans.html', 'showMovies')
AGE_5ANS = (URL_MAIN + 'films-enfants-5-ans.html', 'showMovies')
AGE_7ANS = (URL_MAIN + 'films-enfants-7-ans.html', 'showMovies')
AGE_9ANS = (URL_MAIN + 'films-enfants-9-ans.html', 'showMovies')
AGE_11ANSETPLUS = (URL_MAIN + 'films-enfants-11-ans.html', 'showMovies')
ALL_ALL = (URL_MAIN + 'tous-les-films-pour-enfants.html', 'showMovies')
# BY_THEMES = (URL_MAIN + 'films-programmes-thematiques.html', 'showThemes')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', AGE_3ANS[0])
    oGui.addDir(SITE_IDENTIFIER, AGE_3ANS[1], 'A partir de 3 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', AGE_5ANS[0])
    oGui.addDir(SITE_IDENTIFIER, AGE_5ANS[1], 'A partir de  5 ans', 'enfants.png', oOutputParameterHandler)


    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', AGE_7ANS[0])
    oGui.addDir(SITE_IDENTIFIER, AGE_7ANS[1], 'A partir de 7 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', AGE_9ANS[0])
    oGui.addDir(SITE_IDENTIFIER, AGE_9ANS[1], 'A partir de 9 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', AGE_11ANSETPLUS[0])
    oGui.addDir(SITE_IDENTIFIER, AGE_11ANSETPLUS[1], 'A partir de 11 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ALL_ALL[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_ALL[1], 'Tous les films pour Enfants', 'enfants.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', BY_THEMES[0])
    # oGui.addDir(SITE_IDENTIFIER, BY_THEMES[1], 'Films pour Enfants (Thèmes)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showThemes():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(BY_THEMES[0])
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent, '<lien1>Portail pour les familles</lien1><br>', '<lien1><i class=icon-circle>')

    sPattern = '<a href=([^>]+)><lien3><i class=icon-circle></i>([^<]+)<\/lien3><\/a><br>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # sPattern = 'class=portfolio-image>.*?src=([^ ]+) itemprop.*?synopsis>([^<]+)<.*?href=.*?href=([^ ]+).*?<h3>([^<]+)<'
    sPattern = 'class=portfolio-image>.*?data-src="([^"]+)".*?synopsis>([^<]+)<.*?href=.*?href="([^"]+)".*?<h4>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = URL_MAIN + aEntry[0]
            sDesc = aEntry[1]
            sUrl = URL_MAIN + aEntry[2]
            sTitle = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showFiche', sTitle, 'enfants.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showFiche():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<br>', ' ')
    sPattern = '<a href=".+?" title=".*?" data-lightbox=iframe>.*?</h3><span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sDesc = aEntry

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sMovieTitle, 'enfants.png', sThumb, sDesc, oOutputParameterHandler)

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

    sPattern = '<a href="([^"]+)" title=".*?" data-lightbox=iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
