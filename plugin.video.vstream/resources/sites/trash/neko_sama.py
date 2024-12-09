# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import base64
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager


SITE_IDENTIFIER = 'neko_sama'
SITE_NAME = 'Neko Sama'
SITE_DESC = 'Animés en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN, 'showLastEp')
ANIM_VFS = (URL_MAIN + 'anime-vf', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime', 'showMovies')

URL_SEARCH = (ANIM_VOSTFRS[0], 'showSearchResult')
URL_SEARCH_ANIMS = (ANIM_VOSTFRS[0], 'showSearchResult')
URL_SEARCH_VF = (ANIM_VFS[0], 'showSearchResult')

FUNCTION_SEARCH = 'showSearchResult'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés (VOSTFR)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_VF[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés (VF)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Dernier ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showSearchResult(sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Erotique', 'erotique'], ['Espionnage', 'espionnage'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'],
             ['Policier', 'policier'], ['Péplum', 'peplum'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Spectacle', 'spectacle'], ['Thriller', 'thriller'],
             ['Western', 'western'], ['Divers', 'divers']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchResult(sSearch):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    searchURL = URL_MAIN[:-1] + re.search('var urlsearch = "([^"]+)";', sHtmlContent).group(1)

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            sSearch = sSearch.replace(URL_SEARCH[0], '')
    sSearch = sSearch.lower()

    oRequestHandler = cRequestHandler(searchURL)
    data = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for dicts in data:
        if sSearch in dicts['title'].lower() or sSearch in dicts['title_english'].lower() or sSearch in dicts['others'].lower():
            sTitle = dicts['title']
            sUrl2 = URL_MAIN[:-1] + dicts['url']
            sThumb = dicts['url_image']
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addAnime(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def showLastEp():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'episode":"([^"]+).+?title":"([^"]+).+?lang":"([^"]+).+?anime_url":"([^"]+).+?url_bg":"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[3]
            sThumb = aEntry[4]
            sLang = aEntry[2].upper()
            sTitle = '%s %s [%s]' % (aEntry[1], aEntry[0], sLang)
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)">.+?src="([^"]+)" alt="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addAnime(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a><a href="([^"]+)" class=""><svg'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisonEpisodes():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    if sUrl.endswith("vostfr"):
        oRequestHandler = cRequestHandler(sUrl.replace('vostfr', 'vf'))
        sHtmlContent = oRequestHandler.request()
        if "404 Not Found" not in sHtmlContent:
            oOutputParameterHandler = cOutputParameterHandler()
            sTitle = "[COLOR red]Cliquez ici pour accéder à la version VF[/COLOR]"
            oOutputParameterHandler.addParameter('siteUrl', sUrl.replace('vostfr', 'vf'))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', oOutputParameterHandler)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = '<p>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = 'episode":"([^"]+).+?url":"([^"]+)","url_image":"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = sMovieTitle + ' ' + aEntry[0].replace('Ep. ', 'E')
            sUrl2 = URL_MAIN[:-1] + aEntry[1].replace('\\/', '/')
            sThumb = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "video\[\d+\] = '([^']+)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            # Enlève les faux liens
            # if 'openload' in aEntry or '.mp4' not in aEntry:
            if 'openload' in aEntry or 'mystream.to' in aEntry or "streamtape" in aEntry:
                continue

            '''
            '''
            # NE FONCTIONNE PAS, le lien direct est pourtant bon dans vlc
            if 'fusevideo' in aEntry:   
                UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
                
                oRequestHandler = cRequestHandler(aEntry)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
                oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.9')
                oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
                sHtmlContent = oRequestHandler.request()

                sPattern = '<\/script> *<script src="([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    oRequestHandler = cRequestHandler(aResult[1][0])
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
                    oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.9')
                    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
                    sHtmlContent = oRequestHandler.request()
                    sPattern = 'atob\("([^"]+)"'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0]:
                        url2 = base64.b64decode(aResult[1][0])
                        sPattern = '(https[^"]+)"'
                        aResult = oParser.parse(url2, sPattern)
                        if aResult[0]:
                            sHosterUrl = aResult[1][0].replace('\\', '')
                #EXTM3U
# #EXT-X-STREAM-INF:BANDWIDTH=4000000,RESOLUTION=1920x1080,NAME="1080"
# https://fusevideo.io/h/720/eyJpdiI6IjZUUmZtZTBQTHl5UlpRNkZwWFBzWkE9PSIsInZhbHVlIjoiTkhXZTM3ZnJMekN5akFpNTNnQTNHQT09IiwibWFjIjoiZjg2NzlkOGZhMzc1ZTFiMzY3NzU0YWVhOTc5MmRlZDczZmQxZWQ5MDYzMDRjOTZjNTk1N2M3ZGZhODkwN2FmOCIsInRhZyI6IiJ9.m3u8?expires=1713665472&signature=df5ab2adae17c09bb5f2ad1587bd389839fb3599b6babc853017339b2ce8a8b5
# #EXT-X-STREAM-INF:BANDWIDTH=4000000,RESOLUTION=1280x720,NAME="720"
# https://fusevideo.io/h/720/eyJpdiI6ImJuMTVNeFI4TTNSS3l4RGZzMnRJMGc9PSIsInZhbHVlIjoiUmV6LytrWTFOS3NNN0F1VWZmUTd6Zz09IiwibWFjIjoiZDkzMDcxYWNmNjUwNTFlMzBhMTc2Nzk4OGI1ODY0M2VkZDQxYmFlZmQzZjY1NmUwYmEzNzM5MDcyZTU2Y2RlMCIsInRhZyI6IiJ9.m3u8?expires=1713665472&signature=fed6e68da3a8f753c0cb0d82ac55af461f9c7b93e7816d3ee131298dced7458c
# #EXT-X-STREAM-INF:BANDWIDTH=4000000,RESOLUTION=854x480,NAME="480"
# https://fusevideo.io/h/720/eyJpdiI6InRJTTRkV2RIUFJISndTcWtmM3JUS1E9PSIsInZhbHVlIjoiTVppelR4YlBkdDlDc0RmTUhudUU4dz09IiwibWFjIjoiMGRjMjU3MDBkOTdiMTQzNWE2ZGRjZmIwYmQyY2IwMzY3ODQ5NzdhMzIxNDJmNWU0OWYzODMwMTFkNGEzOWY5YyIsInRhZyI6IiJ9.m3u8?expires=1713665472&signature=eef26164b1df50dc0bdf97b75ec27c9fd13745f68f29a6ff4392118a24fd8012


                            oRequestHandler = cRequestHandler(sHosterUrl)
                            oRequestHandler.addHeaderEntry('User-Agent', UA)
                            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
                            oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.9')
                            oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
                            sHtmlContent = oRequestHandler.request()
                            sPattern = '(https[^#]+)'
                            aResult = oParser.parse(sHtmlContent, sPattern)
                            if aResult[0]:
                                sHosterUrl = aResult[1][0].replace('https:', 'http:')
            '''
            '''

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
