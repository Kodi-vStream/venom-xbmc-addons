#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Par jojotango
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog
from resources.lib.config import GestionCookie

import random,re
#from resources.lib.util import cUtil

SITE_IDENTIFIER = 'neuf_docu'
SITE_NAME = '9Docu'
SITE_DESC = 'Site pour Telecharger ou Regarder des Documentaires et Emissions TV Gratuitement'

URL_MAIN = 'https://9docu.net/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_GENRES = (True, 'showGenres')
DOC_DOCS = ('http://', 'load')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

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
    liste.append( ['[COLOR gold]CATEGORIES[/COLOR]', ''] )
    liste.append( ['Séries Documentaires', URL_MAIN + 'categorie/series-documentaires/'] )
    liste.append( ['Documentaires Exclus', URL_MAIN + 'categorie/documentaires-exclus/'] )
    liste.append( ['Documentaires Inédits', URL_MAIN + 'categorie/documentaires-inedits/'] )
    liste.append( ['Films Documentaires', URL_MAIN + 'categorie/films-documentaires/'] )
    liste.append( ['Emissions Documentaires / Replay TV', URL_MAIN + 'categorie/emissions-documentaires-replay-tv/'] )

    liste.append( ['[COLOR gold]GENRES[/COLOR]', ''] )
    liste.append( ['Actualités', URL_MAIN + 'categorie/actualites/'] )
    liste.append( ['Animaux', URL_MAIN + 'categorie/animaux/'] )
    liste.append( ['Architecture', URL_MAIN + 'categorie/architecture/'] )
    liste.append( ['Art martiaux', URL_MAIN + 'categorie/art-martiaux/'] )
    liste.append( ['Arts', URL_MAIN + 'categorie/arts/'] )
    liste.append( ['Auto/Moto', URL_MAIN + 'categorie/auto-moto/'] )
    liste.append( ['Aventure', URL_MAIN + 'categorie/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'categorie/biopic/'] )
    liste.append( ['Cinéma/Film', URL_MAIN + 'categorie/cinema-film/'] )
    liste.append( ['Civilisation', URL_MAIN + 'categorie/civilisation/'] )
    liste.append( ['Consommation', URL_MAIN + 'categorie/consommation/'] )
    liste.append( ['Cuisine', URL_MAIN + 'categorie/cuisine/'] )
    liste.append( ['Culture/Littérature', URL_MAIN + 'categorie/culturelitterature/'] )
    liste.append( ['Divertissement', URL_MAIN + 'categorie/divertissement/'] )
    liste.append( ['Economie', URL_MAIN + 'categorie/economie/'] )
    liste.append( ['Education', URL_MAIN + 'categorie/education/'] )
    liste.append( ['Emission TV', URL_MAIN + 'categorie/emission/'] )
    liste.append( ['Emploi/Métier', URL_MAIN + 'categorie/emploi-metier/'] )
    liste.append( ['Enquète', URL_MAIN + 'categorie/enquete/'] )
    liste.append( ['Environnement', URL_MAIN + 'categorie/environnement/'] )
    liste.append( ['Espionnage', URL_MAIN + 'categorie/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'categorie/famille/'] )
    liste.append( ['Guerre', URL_MAIN + 'categorie/guerre/'] )
    liste.append( ['Histoire', URL_MAIN + 'categorie/histoire/'] )
    liste.append( ['Humour', URL_MAIN + 'categorie/humour/'] )
    liste.append( ['Investigations', URL_MAIN + 'categorie/investigations/'] )
    liste.append( ['Jeux vidéo/TV', URL_MAIN + 'categorie/jeux-video-tv/'] )
    liste.append( ['Justice/Criminalité', URL_MAIN + 'categorie/justice-criminalite/'] )
    liste.append( ['Magazine', URL_MAIN + 'categorie/magazine/'] )
    liste.append( ['Médias', URL_MAIN + 'categorie/medias/'] )
    liste.append( ['Mode', URL_MAIN + 'categorie/mode/'] )
    liste.append( ['Musique', URL_MAIN + 'categorie/musique/'] )
    liste.append( ['Nature', URL_MAIN + 'categorie/nature/'] )
    liste.append( ['People', URL_MAIN + 'categorie/people/'] )
    liste.append( ['Politique', URL_MAIN + 'categorie/politique/'] )
    liste.append( ['Religion', URL_MAIN + 'categorie/religion/'] )
    liste.append( ['Reportage', URL_MAIN + 'categorie/reportage/'] )
    liste.append( ['Santé/Bien-etre', URL_MAIN + 'categorie/sante-bien-etre/'] )
    liste.append( ['Science/Technologie', URL_MAIN + 'categorie/science-technologie/'] )
    liste.append( ['Sexualité', URL_MAIN + 'categorie/sexualite/'] )
    liste.append( ['Société', URL_MAIN + 'categorie/societe/'] )
    liste.append( ['Sport/Football/Auto/Moto', URL_MAIN + 'categorie/sport-football-auto-moto/'] )
    liste.append( ['Téléréalite', URL_MAIN + 'categorie/telerealite/'] )
    liste.append( ['Tourisme', URL_MAIN + 'categorie/tourisme/'] )
    liste.append( ['Voyage/Decouverte', URL_MAIN + 'categorie/voyage-decouverte/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
      sUrl = sSearch.replace(" ", "+")
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="attachment-medium aligncenter" src="([^<]+)".+?<a href="([^"<]+)"[^<>]+>([^<>]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="(.+?)" />'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span class="(?:14|15)"><a href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if "ReviveLink" in aEntry:
                url2 = 'http://' + (aEntry.split('/')[2]).lower() + '/qcap/Qaptcha.jquery.php'
                idUrl = aEntry.split('/')[3]

                #Make random key
                s = "azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN_-#@";
                RandomKey = ''.join(random.choice(s) for i in range(32))

                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.setRequestType(1)
                oRequestHandler.addHeaderEntry('Host', 'revivelink.com')
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
                oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
                oRequestHandler.addHeaderEntry('Referer', aEntry)
                oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                oRequestHandler.addHeaderEntry('X-Requested-With','XMLHttpRequest')
                oRequestHandler.addParameters('action', 'qaptcha')
                oRequestHandler.addParameters('qaptcha_key', RandomKey)

                sHtmlContent = oRequestHandler.request()

                cookies = oRequestHandler.GetCookies()
                GestionCookie().SaveCookie('revivelink.com', cookies)
                #VSlog( 'result'  + sHtmlContent)

                if not '"error":false' in sHtmlContent:
                    VSlog('Captcha rate')
                    VSlog(sHtmlContent)
                    return

                cookies = GestionCookie().Readcookie('revivelink.com')
                oRequestHandler = cRequestHandler('http://revivelink.com/slinks.php?R='+idUrl+'&'+RandomKey)
                oRequestHandler.addHeaderEntry('Host', 'revivelink.com')
                oRequestHandler.addHeaderEntry('Referer', aEntry)
                oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
                oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                oRequestHandler.addHeaderEntry('X-Requested-With','XMLHttpRequest')
                oRequestHandler.addHeaderEntry('Cookie',cookies)

                sHtmlContent = oRequestHandler.request()

                result = re.findall('<td><a href="([^<]+)" title=\'([^<]+)\'>',sHtmlContent)
                for url,title in result:
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(title)
                        oHoster.setFileName(title)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            else:

                sHosterUrl = aEntry
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
