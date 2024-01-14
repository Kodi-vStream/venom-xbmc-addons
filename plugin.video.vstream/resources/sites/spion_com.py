# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Par jojotango
return False
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog

SITE_IDENTIFIER = 'spion_com'
SITE_NAME = 'Spi0n'
SITE_DESC = 'Insolite du web'

URL_MAIN = "https://www.spi0n.com/"

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN + 'page/1/', 'showMovies')
NETS_GENRES = (True, 'showGenres')

# True : Contenu Censuré | False : Contenu Non Censuré
SPION_CENSURE = True

# logo censure -18ans
LOGO_CSA = 'http://a398.idata.over-blog.com/1/40/34/11/archives/0/16588469.jpg'


def showCensure():

    content = 'Pour activer le contenu (+18) mettre: \n[COLOR coral]SPION_CENSURE = False[/COLOR]\ndans le fichier:\n[COLOR coral]plugin.video.vstream/resources/sites/spion_com.py[/COLOR]'
    dialog().VSok(content)


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_NEWS[1], 'Vidéos (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Vidéos (Genres)', 'genres.png', oOutputParameterHandler)

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
    liste.append(['Actualité', URL_MAIN + 'category/actualite/'])
    liste.append(['Animaux', URL_MAIN + 'category/animaux/'])
    liste.append(['Art', URL_MAIN + 'category/art-technique/'])
    liste.append(['Danse', URL_MAIN + 'category/danse/'])
    liste.append(['Expérience', URL_MAIN + 'category/experiences/'])
    liste.append(['Fake', URL_MAIN + 'category/fake-trucage/'])
    liste.append(['Guerre', URL_MAIN + 'category/guerre-militaire/'])
    liste.append(['Humour', URL_MAIN + 'category/humour-comedie/'])
    liste.append(['Internet', URL_MAIN + 'category/siteweb-internet/'])
    liste.append(['Jeux Vidéo', URL_MAIN + 'category/jeuxvideo-consoles/'])
    liste.append(['Musique', URL_MAIN + 'category/musique/'])
    liste.append(['Non Classé', URL_MAIN + 'category/non-classe/'])
    liste.append(['Owned', URL_MAIN + 'category/owned/'])
    liste.append(['Pub', URL_MAIN + 'category/publicite-marque/'])
    liste.append(['Rewind', URL_MAIN + 'category/rewind/'])
    liste.append(['Santé', URL_MAIN + 'category/sante-corps/'])
    liste.append(['Sport', URL_MAIN + 'category/sport/'])
    liste.append(['Technologie', URL_MAIN + 'category/technologie-innovations/'])
    liste.append(['Transport', URL_MAIN + 'category/auto-transport/'])
    liste.append(['TV & Cinéma', URL_MAIN + 'category/tv-cinema/'])
    liste.append(['WTF?!', URL_MAIN + 'category/wtf/'])
    liste.append(['Zapping', URL_MAIN + 'category/zapping-web/'])

    if (SPION_CENSURE == False):
        liste.append(['NSFW (+18)', URL_MAIN + 'nsfw/'])
        liste.append(['Trash (+18)', URL_MAIN + 'category/trash-gore/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '')

    sPattern = 'id="(post-[0-9]+)".+?src="([^"]+?)".+?href="([^"]+?)" rel="bookmark" title="([^"]+?)".+?title="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sPoster = aEntry[1]
            sUrlp = aEntry[2]
            sTitle = aEntry[3]

            # categorie video
            sCat = aEntry[4]

            # vire lien categorie image
            if (sCat != 'Image'):

                oOutputParameterHandler.addParameter('siteUrl', sUrlp)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sPoster)

                if (SPION_CENSURE == True):
                    if (sCat == 'NSFW') or (sCat == 'Trash'):
                        sPoster = LOGO_CSA
                        oGui.addMisc(SITE_IDENTIFIER, 'showCensure', sTitle, '', sPoster, '', oOutputParameterHandler)
                    else:
                        oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sPoster, '', oOutputParameterHandler)
                else:
                    oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sPoster, '', oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="nav-previous"><a href="([^"<>]+/[0-9]/?[^"]+)" class="nq_previous">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')\
                               .replace('<iframe src=\'http://creative.rev2pub.com', '')\
                               .replace('dai.ly', 'www.dailymotion.com/video')\
                               .replace('youtu.be/', 'www.youtube.com/watch?v=')
    oParser = cParser()

    # prise en compte lien direct mp4
    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        sPattern = '<div class="video_tabs"><a href="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            # Certains URL "dailymotion" sont écrits: //www.dailymotion.com
            if sHosterUrl[:4] != 'http':
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
