#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, VSshowYear
from resources.lib.config import cConfig
import re,xbmcgui,urllib2

SITE_IDENTIFIER = 'skstream_co'
SITE_NAME = 'Skstream'
SITE_DESC = 'Films Series Mangas'

URL_MAIN = 'http://www.skstream.ws/'

MOVIE_NEWS = (URL_MAIN + 'films', 'showMovies')
MOVIE_MOVIE = ('http://films', 'showMenuMovies')
MOVIE_GENRES = (MOVIE_NEWS[0] , 'showGenres')
MOVIE_ANNEES = (MOVIE_NEWS[0] + '-produit-en-' , 'showYears')
MOVIE_QLT = (MOVIE_NEWS[0] , 'showQlt')
MOVIE_PAYS = (URL_MAIN + 'films', 'showPays')

SERIE_NEWS = (URL_MAIN + 'series', 'showMovies')
SERIE_SERIES = ('http://series', 'showMenuSeries')
SERIE_GENRES = (SERIE_NEWS[0], 'showGenres')
SERIE_ANNEES = (SERIE_NEWS[0] + '-sortie-en-', 'showYears')
SERIE_QLT = (SERIE_NEWS[0], 'showQlt')
SERIE_PAYS = (URL_MAIN + 'series', 'showPays')

ANIM_NEWS = (URL_MAIN + 'mangas' , 'showMovies')
ANIM_ANIMS = ('http://mangas', 'showMenuMangas')
ANIM_GENRES = (ANIM_NEWS[0], 'showGenres')
ANIM_ANNEES = (ANIM_NEWS[0] + '-sortie-en-', 'showYears')
ANIM_QLT = (ANIM_NEWS[0], 'showQlt')
ANIM_PAYS = (URL_MAIN + 'mangas', 'showPays')

URL_SEARCH = (URL_MAIN + 'recherche?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films (Menu)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries (Menu)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas (Menu)', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_QLT[1], 'Films (Qualités)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Par Pays)', 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_QLT[1], 'Séries (Qualités)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAYS[1], 'Séries (Par Pays)', 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_QLT[1], 'Animés (Qualités)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animés (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_PAYS[1], 'Animés (Par Pays)', 'lang.png', oOutputParameterHandler)

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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'films' in sUrl:
        reqURL = MOVIE_GENRES[0]
        sStart = '</i>&nbsp; Catégories Films</div>'
        sEnd = '<span data-target="md-tab1" class="active">Pays</span>'
    elif 'series' in sUrl:
        reqURL = SERIE_GENRES[0]
        sStart = '</i>&nbsp; Catégories Séries</div>'
        sEnd = '</i>&nbsp; Séries par</div>'
    else:
        reqURL = ANIM_GENRES[0]
        sStart = '</i>&nbsp; Catégories Mangas</div>'
        sEnd = '</i>&nbsp; Mangas par</div>'

    oParser = cParser()

    oRequestHandler = cRequestHandler(reqURL)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a class="list-group-item" href="([^"]+)".+?>(.+?)<span class=.+?>.+?</i> (.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1] + '(' + aEntry[2] + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showPays():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    if 'mangas' in sUrl:
        liste.append( ['Américain', sUrl + '-de-nationalite-u-s-a'] )
        liste.append( ['Français', sUrl + '-de-nationalite-francais'] )
        liste.append( ['Japonais', sUrl + '-de-nationalite-japon'] )
    else:
        liste.append( ['Américain', sUrl + '-de-nationalite-americain'] )
        liste.append( ['Allemand', sUrl + '-de-nationalite-allemand'] )
        liste.append( ['Britanique', sUrl + '-de-nationalite-britannique'] )
        liste.append( ['Canadien', sUrl + '-de-nationalite-canadien'] )
        liste.append( ['Espagnol', sUrl + '-de-nationalite-espagnol'] )
        liste.append( ['Français', sUrl + '-de-nationalite-francais'] )
        liste.append( ['Italien', sUrl + '-de-nationalite-italien'] )
        liste.append( ['Japonais', sUrl + '-de-nationalite-japonais'] )
        liste.append( ['Norvégien', sUrl + '-de-nationalite-norvegien'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showQlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['1080p', sUrl + '-qualites-1080p'] )
    liste.append( ['720p', sUrl + '-qualites-720p'] )
    liste.append( ['HDrip', sUrl + '-qualites-hdrip'] )
    liste.append( ['HDTV', sUrl + '-qualites-hd-tv'] )
    liste.append( ['BDrip', sUrl + '-qualites-bd-rip'] )
    liste.append( ['BRrip', sUrl + '-qualites-brrip'] )
    liste.append( ['DVDrip', sUrl + '-qualites-dvd-rip'] )
    liste.append( ['WEBrip', sUrl + '-qualites-web-rip'] )
    liste.append( ['DVDscr', sUrl + '-qualites-dvdscr'] )

    for sTitle,sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sCheck = VSshowYear(sUrl)
    if not sCheck == None:
        showMovies(yearUrl = sCheck)

def showMovies(sSearch = '', yearUrl = ''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch
    elif yearUrl:
        sUrl = yearUrl
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<a class="unfilm" *HREF="([^"]+)">.+?title="(.+?)".+?src="([^"]+)">'

    aResult = oParser.parse(sHtmlContent,sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if ('/series/' in sUrl or '/mangas/' in sUrl):
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle,'', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + 'Aucun résultat' + '[/COLOR]')

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li> *<a href="([^"]+)">Suivant *<i'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN[:-1] + aResult[1][0]

    return False

def showEpisode():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sDesc = ''
    sPattern = '<div class="more-info">.+?<p>(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = cUtil().removeHtmlTags(aResult[1][0])

    sPattern = '<div class="panel-heading"><h4><i class="fa fa-television" id="(.+?)">|<a class="episode-block" href="([^"]+)" title="(.+?)">'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                sSaison = aEntry[0].replace('-', ' ')
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + sSaison + '[/COLOR]')
            else:
                sUrl = URL_MAIN[:-1] + aEntry[1]
                sDisplayTitle = aEntry[2].replace('En Streaming', '').replace(',', '').replace('Regarder', '').replace('en streaming', '')
                #suppression de la langue pour le titre transmis doublons dans showLinks
                sTitle = sDisplayTitle.replace(' [VF]', '').replace(' [VOSTFR]', '').replace(' [VO]', '')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sDesc = ''
    sPattern = '<div class="more-info">.+?<p>(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]

    sPattern = '<tr class="changeplayer.+?".+?data-embedlien="([^"]+)".+?<i class="server player-.+?"><\/i>(.+?)<.+?<span class="badge">(.+?)<\/span>.+?<td>(.+?)<\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHost = aEntry[1]
            if 'Skstream' in sHost:
                continue
            sLang = aEntry[2]
            sQual = aEntry[3]
            sUrl2 = aEntry[0]

            sTitle = '%s [%s/%s] [COLOR coral]%s[/COLOR]' %(sMovieTitle, sLang, sQual, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('refUrl', sUrl)
            oOutputParameterHandler.addParameter('sUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    refUrl = oInputParameterHandler.getValue('refUrl')
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

    headers = {'User-Agent': UA ,
                'Referer': refUrl ,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    request = urllib2.Request(sUrl,None,headers)
    reponse = urllib2.urlopen(request)
    vUrl = reponse.geturl()
    reponse.close()

    if vUrl:
        sHosterUrl = vUrl
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
