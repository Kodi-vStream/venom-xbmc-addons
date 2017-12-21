#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

SITE_IDENTIFIER = 'full_stream_org'
SITE_NAME = 'Full-Stream'
SITE_DESC = 'Films, Séries & Animés en Streaming HD'
URL_MAIN = 'http://full-stream.su/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'seriestv/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'seriestv/vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'seriestv/vostfr/', 'showMovies')

#URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&titleonly=3&story=', 'showMovies')
#URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&titleonly=3&story=', 'showMovies')
#URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&titleonly=3&story=', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series_vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

# def showSearch():
    # oGui = cGui()

    # sSearchText = oGui.showKeyBoard()
    # if (sSearchText != False):
        # sUrl = URL_SEARCH[0] + sSearchText
        # showMovies(sUrl)
        # oGui.setEndOfDirectory()
        # return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'film-action/'] )
    liste.append( ['Aventure', URL_MAIN + 'film-aventure/'] )
    liste.append( ['Animation', URL_MAIN + 'film-animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'film-arts-martiaux/'] )
    liste.append( ['Biographie', URL_MAIN + 'film-biographie/'] )
    liste.append( ['Box-office', URL_MAIN + 'film-box-office/'] )
    liste.append( ['Comédie', URL_MAIN + 'film-comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'film-comedie-dramatique/'] )
    liste.append( ['Dramatique', URL_MAIN + 'film-dramatique/'] )
    liste.append( ['Documentaire', URL_MAIN + 'film-documentaire/'] )
    liste.append( ['Familial', URL_MAIN + 'film-familial/'] )
    liste.append( ['Fantastique', URL_MAIN + 'fantastique/'] )
    liste.append( ['Espionnage', URL_MAIN + 'film-espionnage'] )
    liste.append( ['Historique', URL_MAIN + 'film-historique/'] )
    liste.append( ['Horreur', URL_MAIN + 'film-horreur/'] )
    liste.append( ['Musique', URL_MAIN + 'film-musical/'] )
    liste.append( ['Policier', URL_MAIN + 'film-policier/'] )
    liste.append( ['Romance', URL_MAIN + 'film-romance/'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'film-science-fiction/'] )
    liste.append( ['Sport', URL_MAIN + 'film-sport/'] )
    liste.append( ['Thriller', URL_MAIN + 'film-thriller/'] )
    liste.append( ['Western', URL_MAIN + 'film-western/'] )
    liste.append( ['En VOSTFR', URL_MAIN + 'film-vostfr'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    sType = ''

    if sSearch:
        sUrl = sSearch

        #partie en test
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    #sPattern = 'fullstreaming">.*?<img src="(.+?)".+?<h3.+?><a href="(.+?)">(.+?)<\/a>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*<span style="font-family:.+?>(.+?)<\/span>'
    #sPattern = 'fullstreaming".*?img src="(.+?)".+?href="(.+?)">(.+?)<\/a>.*?(?:Version</strong> :([^<]+)<hr/>.*?)*style="font-family:.*?>(.+?)<\/span>'
    sPattern = 'fullstreaming".*?img src="(.+?)".+?<span class="xquality">(.+?)</span>.+?href="(.+?)">(.+?)<\/a>.*?style="font-family:.*?>(.+?)<\/span>'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    cConfig().log(sHtmlContent)
    #page bloquee ?
    if sHtmlContent.startswith('<noscript>'):
        code = re.search('value="([^"]+)"\/>', sHtmlContent, re.DOTALL).group(1)

        oRequestHandler2 = cRequestHandler(sUrl)
        
        oRequestHandler2.addHeaderEntry('Referer', 'http://fullstream.su/')
        oRequestHandler2.addHeaderEntry('User-Agent', UA)
        oRequestHandler2.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        
        oRequestHandler2.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler2.addParametersLine('_authfer=' + code)
     
        sHtmlContent = oRequestHandler2.request()
    
    #cConfig().log(sUrl)
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
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

            sThumb = str(aEntry[0])
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sDesc = aEntry[4]
            sQual = str(aEntry[1]).replace('Haute-qualité', 'HQ').replace(' ', '')
            sTitle = str(aEntry[3])
            sDisplayTitle = sTitle
            if (aEntry[1]):
                sDisplayTitle = sTitle + ' (' + sQual + ')'


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/seriestv/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+)" rel="next">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
        
    return False

def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


    sPattern = '<div class=".+?tab"><i class="fa fa-play-circle-o"><\/i>(.+?)<\/div>|<a href="([^"]+)" title=".+?" target=".+?layer" class="fstab"><i class="fa fa-youtube-play"></i>(.+?)</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if (aEntry[0]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')

            else:
                sUrl2 = URL_MAIN[:-1]+aEntry[1]
                sTitle = '%s [%s]' % (sMovieTitle, aEntry[2])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('referer', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sRef = oInputParameterHandler.getValue('referer')

    oParser = cParser()

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sRef)
    sHtmlContent = oRequest.request()

    sPattern = '; eval\(unescape\("(.+?);",\[(.+?)\],\[(.+)\]'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):

        test1 = aResult[1][0][0]
        test2 = [x.strip('"') for x in aResult[1][0][1].split(',')]
        test3 = [x.strip('"') for x in aResult[1][0][2].split(',')]
        
        sHtmlContent2 = unescape(test1,test2,test3)
        # cConfig().log(sHtmlContent2)
        if sHtmlContent2:
            sHtmlContent = cUtil().unescape(sHtmlContent2)
            # cConfig().log(sHtmlContent)
            sPattern = '<iframe src=(.+?)style='
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHosterUrl = aResult[1][0]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
  
def showLinkSerie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sReftitle = oInputParameterHandler.getValue('reftitle')

    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern ='<div id="'+sReftitle+'" class="fullsfeature">(.+?)/a></ul>'
    aResult1 = oParser.parse(sHtmlContent, sPattern)
    
    sPattern = '<a href="([^"]+)" target=".+?layer" class="fsctab".+?</span>(.+?)<'

    aResult = oParser.parse(aResult1[1], sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sHost = re.sub('Ep:\d+', '', aEntry[1])
            sTitle = '%s [%s]' % (sMovieTitle, sHost)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<div class=".+?tab"><i class="fa fa-play-circle-o"></i>(.+?)<\/div>|title="([^"]+)" data-rel="([^"]+)"'
    
    aResult = re.findall(sPattern,sHtmlContent)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if (aEntry[0]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            else:
  
                sTitle = '%s %s' % (sMovieTitle.replace('VOSTFR', '').replace('VF', '').replace('VOST', ''), aEntry[1])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('reftitle', aEntry[2])
                oGui.addTV(SITE_IDENTIFIER, 'showLinkSerie', sTitle, '', sThumb,'', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def unescape(b, a, c):
    d = b
    j = 0
    while (j < len(a)):
            d = d.replace(a[j], c[j])
            j+=1

    d = d.replace('%26', '&')
    d = d.replace('%3B', ';')

    return d
