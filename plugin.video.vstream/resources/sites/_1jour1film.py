# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# 1jour1film (1J1F) - Dooplay/WordPress. Domaine tournant, resolu via /go/.
#
# Les listes de lecteurs ne sont PAS dans le HTML brut : elles sont base64 dans
# des <script src="data:text/javascript;base64,...">.
#   Films  : var J1F_SRV     = [{label, url, type, source}, ...]
#   Series : var j1fEpsData  = [{num, label, servers:[{label, u|url, type}]}]
# Les lecteurs "manual" sont de la famille SeekStreaming (hoster seekstreaming.py).
import re
import base64
import json
from urllib.parse import urlparse

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager, VSlog
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

SITE_IDENTIFIER = '_1jour1film'
SITE_NAME = '1jour1film'
SITE_DESC = 'Films & Séries en streaming VF/VOSTFR'

# Menu global HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

# Recherche (drive la recherche globale vStream). Préfixe vide : la fonction
# reçoit le texte recherché directement (cf. search.py _pluginSearch).
URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showSeries')

MOVIE_NEWS = ('', 'showMovies')     # page d'accueil = nouveautes
SERIE_NEWS = ('', 'showSeries')

# Cartes (recherche j1f-search-card ET accueil/genre j1f-card) - un seul motif.
CARD_PATTERN = (r'<a href="([^"]+/(?:films|tvshows)/[^"]+)" class="j1f-(?:search-)?card">'
                r'.+?src="(https://image\.tmdb\.org/[^"]+)".+?__title">([^<]+)</div>')


# === Réseau : le site gate sur des en-têtes navigateur complets ===
def _getHtml(sUrl):
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequest.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.9,en;q=0.8')
    oRequest.addHeaderEntry('Sec-Fetch-Mode', 'navigate')
    return oRequest.request()


# === Résolution du domaine (le domaine tourne, /go/ pointe le domaine actif) ===
def getUrlMain():
    siteInfo = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'site_info')
    if siteInfo:
        try:
            html = _getHtml(siteInfo)
            m = re.search(r'TARGET_URL\s*=\s*"([^"]+)"', html)
            if m:
                base = m.group(1).replace('\\/', '/').rstrip('/')
                return base + '/'
        except Exception as e:
            VSlog('[1J1F] getUrlMain: %s' % str(e))
    return siteManager().getUrlMain(SITE_IDENTIFIER)


# === Décodage des lecteurs (base64 dans les data: scripts) ===
def _decodeDataScripts(html):
    out = []
    for m in re.finditer(r'data:text/javascript;base64,([A-Za-z0-9+/=]+)', html):
        try:
            out.append(base64.b64decode(m.group(1)).decode('utf-8', 'replace'))
        except Exception:
            pass
    return out


def _extractJsArray(html, varName):
    pat = re.compile(r'(?:var|let|const)\s+' + re.escape(varName) + r'\s*=\s*(\[[\s\S]*?\])\s*;')
    for js in _decodeDataScripts(html) + [html]:   # data: scripts d'abord, page brute en secours
        m = pat.search(js)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass
    return None


def _decodeUrl(u):
    # Le champ url/u est souvent base64 ; laisse tel quel s'il est déjà en http(s).
    if not isinstance(u, str) or not u:
        return ''
    if re.match(r'^https?://', u, re.I):
        return u
    try:
        dec = base64.b64decode(u).decode('utf-8')
        return dec if re.match(r'^https?://', dec, re.I) else ''
    except Exception:
        return ''


def _isSeekShape(url):
    # Embed SeekStreaming : https://<host>/#<id> (id dans le fragment, path vide).
    p = urlparse(url)
    return bool(p.fragment) and (not p.path or p.path == '/')


def _yearFromUrl(sUrl):
    m = re.search(r'-(\d{4})(?:[-/]|$)', sUrl)
    return m.group(1) if m else ''


def _routeServers(oGui, servers, sTitle, sThumb):
    oHosterGui = cHosterGui()
    for s in servers or []:
        if not isinstance(s, dict):
            continue
        url = _decodeUrl(s.get('url') or s.get('u') or '')
        if not url:
            continue
        source = str(s.get('source') or '').lower()
        label = s.get('label') or ''
        # "manual" (ou forme d'embed seek) => SeekStreaming, sinon routage classique.
        if source == 'manual' or _isSeekShape(url):
            oHoster = oHosterGui.getHoster('seekstreaming')
        else:
            oHoster = oHosterGui.checkHoster(url)
        if not oHoster:
            continue
        sDisplay = ('%s [%s]' % (sTitle, label)).strip() if label else sTitle
        oHoster.setDisplayName(sDisplay)
        oHoster.setFileName(sTitle)
        oHosterGui.showHoster(oGui, oHoster, url, sThumb)


# === Menus ===
def load():
    oGui = cGui()
    oOut = cOutputParameterHandler()
    oOut.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOut)
    oOut.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOut)
    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()
    oOut = cOutputParameterHandler()
    oOut.addParameter('siteUrl', 'film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOut)
    oOut.addParameter('siteUrl', 'home')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Nouveautés', 'news.png', oOut)
    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()
    oOut = cOutputParameterHandler()
    oOut.addParameter('siteUrl', 'serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOut)
    oOut.addParameter('siteUrl', 'home')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Nouveautés', 'news.png', oOut)
    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearch = oGui.showKeyBoard()
    if sSearch:
        sUrl = cInputParameterHandler().getValue('siteUrl')
        if sUrl and 'serie' in sUrl:
            showSeries(sSearch)
        else:
            showMovies(sSearch)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    _showResults(sSearch, 'movie')


def showSeries(sSearch=''):
    _showResults(sSearch, 'tv')


def _showResults(sSearch, wantType):
    oGui = cGui()
    oParser = cParser()
    oUtil = cUtil()
    URL_MAIN = getUrlMain()

    sSearchText = ''
    if sSearch:
        # sSearch peut arriver déjà url-quoté (%20) via la recherche globale.
        sSearchText = oUtil.CleanName(sSearch.replace('%20', ' '))
        sUrl = URL_MAIN + '?s=' + sSearch.replace(' ', '+')
    else:
        # 'home' (ou vide) = page d'accueil = nouveautés
        sUrl = URL_MAIN

    html = _getHtml(sUrl)
    aResult = oParser.parse(html, CARD_PATTERN)

    if aResult[0]:
        seen = set()
        oOut = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sMovieUrl = aEntry[0]
            isMovie = '/films/' in sMovieUrl
            if wantType == 'movie' and not isMovie:
                continue
            if wantType == 'tv' and isMovie:
                continue
            if sMovieUrl in seen:
                continue
            seen.add(sMovieUrl)

            sThumb = aEntry[1]
            sTitle = oUtil.unescape(aEntry[2]).strip()
            if sSearch and not oUtil.CheckOccurence(sSearchText, sTitle):
                continue

            sYear = _yearFromUrl(sMovieUrl)
            oOut.addParameter('siteUrl', sMovieUrl)
            oOut.addParameter('sMovieTitle', sTitle)
            oOut.addParameter('sThumb', sThumb)
            oOut.addParameter('sYear', sYear)

            if isMovie:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieHosters', sTitle, '', sThumb, '', oOut)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOut)
    else:
        oGui.addText(SITE_IDENTIFIER)

    if not sSearch:
        oGui.setEndOfDirectory()


# === Films : page -> J1F_SRV -> lecteurs ===
def showMovieHosters():
    oGui = cGui()
    oIn = cInputParameterHandler()
    sUrl = oIn.getValue('siteUrl')
    sTitle = oIn.getValue('sMovieTitle')
    sThumb = oIn.getValue('sThumb')

    html = _getHtml(sUrl)
    srv = _extractJsArray(html, 'J1F_SRV')
    if srv:
        _routeServers(oGui, srv, sTitle, sThumb)
    else:
        oGui.addText(SITE_IDENTIFIER)
    oGui.setEndOfDirectory()


# === Séries : tvshow -> saisons -> j1fEpsData -> episodes -> lecteurs ===
def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oIn = cInputParameterHandler()
    sUrl = oIn.getValue('siteUrl')
    sThumb = oIn.getValue('sThumb')
    sDesc = oIn.getValue('sDesc')
    sTitle = oIn.getValue('sMovieTitle')

    html = _getHtml(sUrl)
    aResult = oParser.parse(html, r'href="([^"]+/saisons/[^"]*saison-(\d+)[^"]*)"')

    if aResult[0]:
        seen = set()
        oOut = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sSeasonUrl = aEntry[0]
            sSeason = aEntry[1]
            if sSeason in seen:
                continue
            seen.add(sSeason)
            sSeasonTitle = '%s - Saison %s' % (sTitle, sSeason)
            oOut.addParameter('siteUrl', sSeasonUrl)
            oOut.addParameter('sMovieTitle', sSeasonTitle)
            oOut.addParameter('sThumb', sThumb)
            oOut.addParameter('sDesc', sDesc)
            oOut.addParameter('sSeason', sSeason)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sSeasonTitle, '', sThumb, sDesc, oOut)
    else:
        oGui.addText(SITE_IDENTIFIER)
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oIn = cInputParameterHandler()
    sUrl = oIn.getValue('siteUrl')
    sThumb = oIn.getValue('sThumb')
    sDesc = oIn.getValue('sDesc')
    sTitle = oIn.getValue('sMovieTitle')       # "<titre> - Saison N"
    sSeason = oIn.getValue('sSeason')

    html = _getHtml(sUrl)
    eps = _extractJsArray(html, 'j1fEpsData')

    if eps:
        oOut = cOutputParameterHandler()
        for e in eps:
            if not isinstance(e, dict):
                continue
            sNum = str(e.get('num') or '')
            if not sNum:
                continue
            sLabel = e.get('label') or ''
            sEpTitle = '%s Episode %s' % (sTitle, sNum)
            sDisplay = ('%s - %s' % (sEpTitle, sLabel)) if sLabel else sEpTitle
            oOut.addParameter('siteUrl', sUrl)
            oOut.addParameter('sMovieTitle', sEpTitle)
            oOut.addParameter('sThumb', sThumb)
            oOut.addParameter('sSeason', sSeason)
            oOut.addParameter('sEpisode', sNum)
            oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodeHosters', sDisplay, '', sThumb, sDesc, oOut)
    else:
        oGui.addText(SITE_IDENTIFIER)
    oGui.setEndOfDirectory()


def showEpisodeHosters():
    oGui = cGui()
    oIn = cInputParameterHandler()
    sUrl = oIn.getValue('siteUrl')
    sThumb = oIn.getValue('sThumb')
    sTitle = oIn.getValue('sMovieTitle')
    sEpisode = str(oIn.getValue('sEpisode'))

    html = _getHtml(sUrl)
    eps = _extractJsArray(html, 'j1fEpsData')

    servers = []
    if eps:
        for e in eps:
            if isinstance(e, dict) and str(e.get('num') or '') == sEpisode:
                servers = e.get('servers') or []
                break

    if servers:
        _routeServers(oGui, servers, sTitle, sThumb)
    else:
        oGui.addText(SITE_IDENTIFIER)
    oGui.setEndOfDirectory()
