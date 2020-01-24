#-*- coding: utf-8 -*-
#Venom.kodigoal
#from resources.lib.gui.hoster import cHosterGui
#ne fonctionne plus : une reprise depuis twitter vraiment utile ?
return False
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import util
import xbmc
#player
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
import xbmcgui

SITE_IDENTIFIER = 'malaisetv'
SITE_NAME = 'Malaise TV'
SITE_DESC = 'Les séquences les plus embarrassantes de la télévision française'

URL_MAIN = 'https://twitter.com/malaisetele/media?lang=fr'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN, 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_NEWS[1], 'Vidéos (Derniers ajouts)', 'news.png', oOutputParameterHandler)

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

    sPattern = '<a href="([^"]+)" class="tweet.+?" title=".+?\-([^"]+)".+?background-image:url((.+?))">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = util.createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            util.updateDialog(dialog, total)

            sUrl   =  'https://twitter.com' + str(aEntry[0])

            sThumbnail = str(aEntry[2]).replace("'", '').replace('(', '').replace(')', '')

            sTitle  = (' %s ') % (str(aEntry[1]))

            #recup id last tweet pour NextPage
            sNext = str(aEntry[0]).replace( '/malaisetele/status/' , '')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)


            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)

        util.finishDialog(dialog)

        sNextPage = __checkForNextPage(sNext)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(url):

    sUrl = 'https://twitter.com/malaisetele/media?include_available_features=1&include_entities=1&lang=fr&max_position=' + url + '&reset_error_state=false'
    return sUrl

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #recup lien mp4 video twitter via twdown.net
    sUrl2 = 'http://twdown.net/download.php'

    oRequestHandler = cRequestHandler(sUrl2)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('URL', sUrl)
    oRequestHandler.addParameters('submit', 'Download')
    oRequestHandler.addParameters('submit', '')
    sHtmlContent = oRequestHandler.request()

    #recup du lien mp4
    sPattern = '<td>[0-9]+P</td>.+?<a download href="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        sUrl = str(aResult[1][0])

        #on lance video directement
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return

    else:
        return

    oGui.setEndOfDirectory()
