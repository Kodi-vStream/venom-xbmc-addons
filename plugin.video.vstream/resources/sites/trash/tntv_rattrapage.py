#-*- coding: utf-8 -*-
#Venom.
#desactiver le 07/12/17
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,unicodedata

#11/12/17 le site fonctionne mais pas verifier
SITE_IDENTIFIER = 'tntv_rattrapage'
SITE_NAME = 'Tntv-rattrapage'
SITE_DESC = 'Replay TV'

URL_MAIN = 'http://tntv-rattrapage.overblog.com/'

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = ('xyz', 'showGenre')

URL_SEARCH = (URL_MAIN + 'search/','showMovies')
URL_SEARCH_MISC = (URL_MAIN + 'search/','showMovies')


#FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Nouvelles Emissions', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Emissions par Catégories', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        #sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText + '/'

        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []

    if sUrl == 'xyz':
        liste.append( ['Chaines','1'] )
        liste.append( ['Téléréalités','2'] )
        liste.append( ['Divertissement','3'] )
        liste.append( ['Infos et magazines','4'] )
        liste.append( ['Sport','5'] )
        liste.append( ['Série VF',URL_MAIN + 'tag/series%20vf/'] )
        liste.append( ['Série VOSTFR',URL_MAIN + 'tag/series%20vostfr/'] )

        for sTitle,sUrl2 in liste:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            if not sUrl2.startswith('http'):
                oGui.addDir(SITE_IDENTIFIER, 'showGenre', sTitle, 'genres.png', oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
    else:

        oRequestHandler = cRequestHandler(URL_MAIN)
        sHtmlContent = oRequestHandler.request()

        sPattern = ''

        if sUrl == '1':
            sPattern = 'class="NavElement-link" href="#">Cat..gories<\/a>(.+?)class="NavElement-link" href="#">Archives<\/a>'
        if sUrl == '2':
            sPattern = 'class="NavElement-link" href="#">T..l..r..alit..s<\/a>(.+?)class="NavElement-link" href="#">Divertissement<\/a>'
        if sUrl == '3':
            sPattern = 'class="NavElement-link" href="#">Divertissement<\/a>(.+?)class="NavElement-link" href="#">Infos et Magazine<\/a>'
        if sUrl == '4':
            sPattern = 'class="NavElement-link" href="#">Infos et Magazine<\/a>(.+?)class="NavElement-link" href="#">Sport<\/a>'
        if sUrl == '5':
            sPattern = 'class="NavElement-link" href="#">Sport<\/a>(.+?)class="NavElement-link" href="\/tag\/archive">Les int..grales<\/a>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        if (aResult[0] == True):
            tmp = aResult[1][0]
            sPattern = 'class="NavElement-link" href="(.+?)">(.+?)<\/a>'
            oParser = cParser()
            aResult = oParser.parse(tmp, sPattern)

        if (aResult[0] == True):

            for aEntry in aResult[1]:
                sTitle = aEntry[1]
                sUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN[:-1] + sUrl)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl = sUrl.replace(' ','%20')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('direct','')

    sPattern = '<img class="PostPreview-coverImage" src="(.+?)" alt="(.+?)".+?<p class="PostPreview-snippet">(.+?)</p>.+?<a class="PostPreview-link" href="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #print aResult
    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = unicode(aEntry[1], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            sTitle = sTitle.encode( "utf-8")

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],'')[:-1],sTitle) == 0:
                    continue

            #Reformatage
            sTitle = re.sub('[0-9:]{5} \| ([0-9-]{8}) \|','[\\1]', sTitle)

            sMovieTitle = sTitle#re.sub('(\[.*\])','', str.strip(aEntry[1]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[3]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))

            #if '[direct]' in aEntry[1]:
                #oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sTitle, aEntry[0], aEntry[2], oOutputParameterHandler)
            #else:
            if not '[direct]' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showHoster', sTitle, '', aEntry[0], aEntry[2], oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'class="ob-page ob-page-current ".+?href="(.+?)".+?class="ob-page ob-page-link ob-page-next"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return str(URL_MAIN[:-1]) + aResult[1][0]

    return False

def showHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    #sUrl = sUrl.replace("\'", '').replace('')', '')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    sPattern = '<a (?:sl-processed="1" )*(?:class="episode-number" )*href="#itsthetable1" on[cC]lick="(.+?)_player\( *\'(.+?)\' *\);">(?:<span class="ep-numb">(.+?)<\/span>)*'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if 'exashare' in aEntry[0]:
                sUrl = 'http://www.exashare.com/embed-' + str(aEntry[1]) + '-624x360.html'

            if 'flashx' in aEntry[0]:
                sUrl = 'http://www.flashx.tv/embed-' + str(aEntry[1]) + '-624x360.html'

            if 'youwatch' in aEntry[0]:
                sUrl = 'http://youwatch.org/embed-' + str(aEntry[1]) + '-624x360.html'

            if 'streamin2' in aEntry[0]:
                sUrl = 'http://streamin.to/embed-' + str(aEntry[1]) + '-624x360.html'

            if 'vodlocker' in aEntry[0]:
                sUrl = 'http://vodlocker.com/embed-' + str(aEntry[1]) + '-624x360.html'

            sTitle = sMovieTitle
            if aEntry[2]:
                sTitle = sTitle + 'Ep ' + aEntry[2]

            sHosterUrl = sUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
