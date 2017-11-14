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
import re,urllib,urllib2

SITE_IDENTIFIER = 'filmsvostfr_biz'
SITE_NAME = 'Filmsvostfr'
SITE_DESC = 'Films/Séries/Animés'

URL_MAIN = 'http://filmsvostfr.ws/'

MOVIE_NEWS = (URL_MAIN + 'films-en-streaming', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showMovieAnnees')

SERIE_NEWS = (URL_MAIN + 'series-en-streaming', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series-en-streaming', 'showMovies')
SERIE_GENRES = ('http://seriegenre', 'showGenres')
SERIE_ANNEES = (True, 'showSerieAnnees')

ANIM_NEWS = (URL_MAIN + 'animes-en-streaming', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes-en-streaming', 'showMovies')
ANIM_GENRES = ('http://animgenre', 'showGenres')
ANIM_ANNEES = (True, 'showAnimeAnnees')

URL_SEARCH = (URL_MAIN + 'recherche.htm?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche.htm?q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche.htm?q=', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'series_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animés (Par Années)', 'animes_annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + '1_1_action.html'] )
    liste.append( ['Animation',URL_MAIN + '2_1_animation.html'] )
    liste.append( ['Arts Martiaux',URL_MAIN + '24_1_arts-martiaux.html'] )
    liste.append( ['Aventure',URL_MAIN + '3_1_aventure.html'] )
    liste.append( ['Biopic',URL_MAIN + '13_1_biopic.html'] )
    liste.append( ['Bollywood',URL_MAIN + '26_1_bollywood.html'] )
    liste.append( ['Comédie',URL_MAIN + '4_1_comedie.html'] )
    liste.append( ['Comédie dramatique',URL_MAIN + '22_1_comedie-dramatique.html'] )
    liste.append( ['Comédie Musicale',URL_MAIN + '17_1_comedie_musicale.html'] )
    liste.append( ['Concert',URL_MAIN + '28_1_concert.html'] )
    liste.append( ['Divers',URL_MAIN + '14_1_divers.html'] )
    liste.append( ['Documentaire',URL_MAIN + '15_1_documentaire.html'] )
    liste.append( ['Drame',URL_MAIN + '5_1_drame.html'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '6_1_epouvante-horreur.html'] )
    liste.append( ['Erotique',URL_MAIN + '25_1_erotique.html'] )
    liste.append( ['Espionnage',URL_MAIN + '12_1_espionnage.html'] )
    liste.append( ['Famille',URL_MAIN + '18_1_famille.html'] )
    liste.append( ['Fantastique',URL_MAIN + '7_1_fantastique.html'] )
    liste.append( ['Guerre',URL_MAIN + '21_1_guerre.html'] )
    liste.append( ['Historique',URL_MAIN + '23_1_historique.html'] )
    liste.append( ['Musical',URL_MAIN + '16_1_musical.html'] )
    liste.append( ['Non Classé',URL_MAIN + '26_1_bollywood.html'] )
    liste.append( ['Opéra',URL_MAIN + '27_1_opera.html'] )
    liste.append( ['Péplum',URL_MAIN + '20_1_peplum.html'] )
    liste.append( ['Policier',URL_MAIN + '8_1_policier.html'] )
    liste.append( ['Romance',URL_MAIN + '9_1_romance.html'] )
    liste.append( ['Science Fiction',URL_MAIN + '10_1_science-fiction.html'] )
    liste.append( ['Thriller',URL_MAIN + '11_1_thriller.html'] )
    liste.append( ['Western',URL_MAIN + '19_1_western.html'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'serie' in sUrl:
        code = 'series/'
    else:
        code = 'animes/'

    liste = []
    liste.append( ['Action',URL_MAIN + code + 'action.html'] )
    liste.append( ['Animation',URL_MAIN + code + 'animation.html'] )
    liste.append( ['Arts Martiaux',URL_MAIN + code + 'arts-martiaux.html'] )
    liste.append( ['Aventure',URL_MAIN + code + 'aventure.html'] )
    liste.append( ['Biopic',URL_MAIN + code + 'biopic.html'] )
    liste.append( ['Comédie',URL_MAIN + code + 'comedie.html'] )
    liste.append( ['Comédie dramatique',URL_MAIN + code + 'comedie-dramatique.html'] )
    liste.append( ['Comédie Musicale',URL_MAIN + code + 'comedie_musicale.html'] )
    liste.append( ['Divers',URL_MAIN + code + 'divers.html'] )
    liste.append( ['Documentaire',URL_MAIN + code + 'documentaire.html'] )
    liste.append( ['Drame',URL_MAIN + code + 'drame.html'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + code + 'epouvante-horreur.html'] )
    liste.append( ['Espionnage',URL_MAIN + code + 'espionnage.html'] )
    liste.append( ['Famille',URL_MAIN + code + 'famille.html'] )
    liste.append( ['Fantastique',URL_MAIN + code + 'fantastique.html'] )
    liste.append( ['Guerre',URL_MAIN + code + 'guerre.html'] )
    liste.append( ['Historique',URL_MAIN + code + 'historique.html'] )
    liste.append( ['Musical',URL_MAIN + code + 'musical.html'] )
    liste.append( ['Policier',URL_MAIN + code + 'policier.html'] )
    liste.append( ['Romance',URL_MAIN + code + 'romance.html'] )
    liste.append( ['Science Fiction',URL_MAIN + code + 'science-fiction.html'] )
    liste.append( ['Thriller',URL_MAIN + code + 'thriller.html'] )
    liste.append( ['Western',URL_MAIN + code + 'western.html'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1921, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films-produit-en-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1940, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series-produit-en-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimeAnnees():
    oGui = cGui()

    for i in reversed (xrange(1969, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'animes-produit-en-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

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

    sPattern = 'format-video hentry item-video">.+?<img src="(.+?)".+?<a href="([^<>"]+?)".+?<b>(.+?)<\/b>'

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

            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle)
            try:
                sTitle = sTitle.encode("utf-8")
            except:
                pass

            sUrl = aEntry[1]
            sThumb = aEntry[0]
            if not sThumb.startswith('http'):
               sThumb = URL_MAIN + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            elif '/anime' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'animes.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        if not sSearch:
            if '/serie' in sUrl or  '/anime' in sUrl:
                sNextPage = __checkForNextPage2(sHtmlContent)
            else:
                sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^<>']+?)' rel='nofollow' class=\"last\">suiv »<\/a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def __checkForNextPage2(sHtmlContent):
    sPattern = "<span class=\"courante\">.+?<a href='(.+?)' rel='nofollow'>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

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

    #resume
    sDesc= ''
    if '/anime' in sUrl:
        sPattern = '<span>Synopsis.+?<\/span><span>([^<]+)<\/span><\/p>'
    else:
        sPattern = '<span>Résumé.+?<\/span><span>([^<]+)<\/span><\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sDesc = aResult[1][0]

    sPattern = '<span>(.aison *\d+.+?)<\/span>'
    sPattern = sPattern + '|href="([^"]+)">(épisode.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    SaisonNum = '0'

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                SaisonNum = oParser.getNumberFromString(aEntry[0])
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]Saison ' + SaisonNum + '[/COLOR]')
            else:
                if 'aison' in sMovieTitle:
                    sTitle = sMovieTitle + aEntry[2]
                else:
                    sTitle = sMovieTitle + ' S' + SaisonNum + aEntry[2]

                sUrl = URL_MAIN[:-1] + aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
    sHtmlContent = sHtmlContent.replace('HD streaming', '').replace('télécharger sur ', '')
    oParser = cParser()

    sPattern = '<img src="(\/images\/video-coming-soon\.jpg)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        oGui.addText(SITE_IDENTIFIER,'[COLOR crimson]' + 'Vidéo bientôt disponible' + '[/COLOR]')

    #resume
    sDesc= ''
    sPattern = '<span class="synopsis">([^<]+)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sDesc = aResult[1][0]

    sPattern = '<a href="([^"]+)" class="sinactive ilink.+?" rel="nofollow" title="([^"]+)">.+?<span class="quality" title="(.+?)">.+?<span class="langue" title="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0].replace('p=watchers', 'p=30').replace('p=16do', 'p=16').replace('p=the23eo', 'p=23').replace('p=the24', 'p=24') #a del si correction sur le site
            if sUrl.endswith('&c=') or '?p=0&c=' in sUrl: #vide ou redirection
                continue

            sHost = aEntry[1]
            sQual = aEntry[2]
            sLang = aEntry[3]
            #sTitle = ('[COLOR coral]' + '[' + sLang + ']' + '[/COLOR]' + ' ' + sMovieTitle + ' ' + '(' + sHost + ')')
            sTitle = '%s [%s/%s] (%s)' % (sMovieTitle, sLang, sQual, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    #evite redirection vers fausse video hs
    if 'filmsvostfr.vip' in sUrl:
        sHost = 'www.filmsvostfr.vip'
    elif 'voirstream.org' in sUrl:
        sHost = 'www.voirstream.org'

    if 'filmsvostfr.vip' in sUrl or 'voirstream.org' in sUrl:
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

        headers = {'User-Agent': UA,
                   'Host': sHost,
                   'Referer': URL_MAIN,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Content-Type': 'text/html; charset=utf-8'}

        request = urllib2.Request(sUrl, None, headers)
        reponse = urllib2.urlopen(request)
        repok = reponse.read()
        reponse.close()

        vUrl = re.search('url=([^"]+)"', repok)
        if vUrl:
           sHosterUrl = vUrl.group(1)
           if 'uptobox' in sHosterUrl:
               sHosterUrl = re.sub(r'(http://www\.filmsvostfr.+?/uptoboxlink\.php\?link=)', 'http://uptobox.com/', sHosterUrl)
           elif '1fichier' in sHosterUrl:
               sHosterUrl = re.sub(r'(http://www\.filmsvostfr.+?/1fichierlink\.php\?link=)', 'https://1fichier.com/?', sHosterUrl)

    else:
        sHosterUrl = sUrl

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
