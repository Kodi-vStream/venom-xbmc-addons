# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'

SITE_IDENTIFIER = 'wawacity'
SITE_NAME = '[COLOR violet]Wawacity[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + '?search=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

tagmovies = '&p=films'
tagseries = '&p=series'
tagmangas = '&p=mangas'
URL_SEARCH_MOVIES = (URL_SEARCH[0] + tagmovies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + tagseries, 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0] + tagmangas, 'showMovies')
# URL_SEARCH_MANGAS = (URL_SEARCH[0], 'showMovies')
# URL_SEARCH_SPECTACLES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = ('http://', 'showMenuMovies')
MOVIE_EXCLU = (URL_MAIN + '?p=films&s=exclus', 'showMovies')
MOVIE_HD = (URL_MAIN + '?p=films&s=blu-ray_1080p-720p', 'showMovies')
MOVIE_3D = (URL_MAIN + '?p=films&s=blu-ray_3d', 'showMovies')
MOVIE_4K = (URL_MAIN + '?p=films&s=ultra-hd-4k', 'showMovies')
MOVIE_ANIMATION = (URL_MAIN + '?p=films&s=dessins_animes', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + '?p=films&s=dvdrip-dbrip', 'showMovies')
MOVIE_BDRIP_MKV = (URL_MAIN + '?p=films&s=dvdrip-hq', 'showMovies')
MOVIE_CAM = (URL_MAIN + '?p=films&s=dvdsrc-r5-ts-cam', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + '?p=films&s=film-vostfr', 'showMovies')
MOVIE_VO = (URL_MAIN + '?p=films&s=_film-vo', 'showMovies')
VIEUX_FILM = (URL_MAIN + '?p=films&s=vieux-films', 'showMovies')
MOVIE_MALENTENDANTS = (URL_MAIN + '?p=films&s=film-sourds-et-malentendants', 'showMovies')
MOVIE_LISTS = (URL_MAIN + '?p=films', 'showMovies')
MOVIE_GENRES = (True, 'showGenresMovies')

ANIM_ANIMS = ('http://', 'showMenuMangas')
ANIM_VFS = (URL_MAIN + '?p=mangas&s=vf', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + '?p=mangas&s=vostfr', 'showMovies')
ANIM_LIST = (URL_MAIN + '?p=mangas', 'showMovies')
ANIM_GENRES = (True, 'showGenreAnime')

DIVERTISSEMENTS = (URL_MAIN + '?p=autres-videos&s=divertissements', 'showMovies')
SPECTACLES = (URL_MAIN + '?p=autres-videos&s=spectacles', 'showMovies')
DOC_DOCS = (URL_MAIN + '?p=autres-videos&s=documentaires', 'showMovies')
DIVERS_LIST = (URL_MAIN + '?p=autres-videos', 'showMovies')
DIVERS_GENRES = (True, 'showGenreDivers')

SERIE_SERIES = ('http://', 'showMenuTvShows')
SERIE_VF_SD = (URL_MAIN + '?p=series&s=vf', 'showMovies')
SERIE_VF_HD = (URL_MAIN + '?p=series&s=vf-hq', 'showMovies')
SERIE_VOSTFR_SD = (URL_MAIN + '?p=series&s=vostfr', 'showMovies')
SERIE_VOSTFR_HD = (URL_MAIN + '?p=series&s=vostfr-hq', 'showMovies')
SERIE_LIST = (URL_MAIN + '?p=series', 'showMovies')
SERIE_GENRES = (True, 'showGenreSeries')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Mangas', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuDivers', 'Divers', 'buzz.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Recherche de Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLU[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLU[1], 'Films Exclus', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films en 3D', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films (4K)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIMATION[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANIMATION[1], 'Films D\'animation', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRip)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP_MKV[1], 'Films (BDRip MKV)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CAM[1], 'Films (Cam)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VO[1], 'Films (VO)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', VIEUX_FILM[0])
    oGui.addDir(SITE_IDENTIFIER, VIEUX_FILM[1], 'Films ancien', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MALENTENDANTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MALENTENDANTS[1], 'Films sourds et malentendants', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LISTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LISTS[1], 'Liste des films', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche de Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_SD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF_SD[1], 'Séries (VF SD)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF_HD[1], 'Séries (VF HD)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR_SD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR_SD[1], 'Séries (VOSTFR SD)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR_HD[1], 'Séries (VOSTFR HD)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Liste des séries', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMangas', 'Recherche de Manga', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Liste des animés', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuDivers():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchDivers', 'Recherche Divers', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DIVERTISSEMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, DIVERTISSEMENTS[1], 'Divertissements', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPECTACLES[0])
    oGui.addDir(SITE_IDENTIFIER, SPECTACLES[1], 'Spectacles', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_DOCS[1], 'Documentaire', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DIVERS_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, DIVERS_LIST[1], 'Liste divers', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DIVERS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DIVERS_GENRES[1], 'Divers (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchMovies():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + tagmovies + sSearchText  # + '&p=films'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + tagseries + sSearchText  # + '&p=series'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchMangas():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + tagmangas + sSearchText  # + '&p=mangas'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchDivers():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + sSearchText + '&p=autres-videos'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenresMovies():
    oGui = cGui()

    liste = []
    liste.append(['Action', '?p=films&genre=action'])
    liste.append(['Animation', '?p=films&genre=animation'])
    liste.append(['Arts Martiaux', '?p=films&genre=arts_martiaux'])
    liste.append(['Aventure', '?p=films&genre=aventure'])
    liste.append(['Biographie', '?p=films&genre=biographie'])
    liste.append(['Biopic', '?p=films&genre=biopic'])
    liste.append(['Comédie', '?p=films&genre=_comedie'])
    liste.append(['Comédie dramatique', '?p=films&genre=comedie_dramatique'])
    liste.append(['Comédie musicale', '?p=films&genre=comedie_musical'])
    liste.append(['Documentaire', '?p=films&genre=documentaire'])
    liste.append(['Drame', '?p=films&genre=drame'])
    liste.append(['Espionnage', '?p=films&genre=espionnage'])
    liste.append(['Famille', '?p=films&genre=en_famille'])
    liste.append(['Fantastique', '?p=films&genre=fantastique'])
    liste.append(['Guerre', '?p=films&genre=guerre'])
    liste.append(['Historique', '?p=films&genre=historique'])
    liste.append(['Horreur', '?p=films&genre=horreur-epouvante'])
    liste.append(['Musical', '?p=films&genre=musical'])
    liste.append(['Péplum', '?p=films&genre=peplum'])
    liste.append(['Policier', '?p=films&genre=policier'])
    liste.append(['Romance', '?p=films&genre=romance'])
    liste.append(['Science fiction', '?p=films&genre=science-fiction'])
    liste.append(['Spectacle', '?p=films&genre=spectacle'])
    liste.append(['Thriller', '?p=films&genre=thriller'])
    liste.append(['Western', '?p=films&genre=western'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenreSeries():
    oGui = cGui()

    liste = []
    liste.append(['Action', '?p=series&genre=action'])
    liste.append(['Animation', '?p=series&genre=animation'])
    liste.append(['Arts Martiaux', '?p=series&genre=arts_martiaux'])
    liste.append(['Aventure', '?p=series&genre=aventure'])
    liste.append(['Biographie', '?p=series&genre=biographie'])
    liste.append(['Biopic', '?p=series&genre=biopic'])
    liste.append(['Comédie', '?p=series&genre=_comedie'])
    liste.append(['Comédie dramatique', '?p=series&genre=comedie_dramatique'])
    liste.append(['Comédie musicale', '?p=series&genre=comedie_musical'])
    liste.append(['Documentaire', '?p=series&genre=documentaire'])
    liste.append(['Drame', '?p=series&genre=drame'])
    liste.append(['Espionnage', '?p=series&genre=espionnage'])
    liste.append(['Famille', '?p=series&genre=en_famille'])
    liste.append(['Fantastique', '?p=series&genre=fantastique'])
    liste.append(['Guerre', '?p=series&genre=guerre'])
    liste.append(['Historique', '?p=series&genre=historique'])
    liste.append(['Horreur', '?p=series&genre=horreur-epouvante'])
    liste.append(['Musical', '?p=series&genre=musical'])
    liste.append(['Péplum', '?p=series&genre=peplum'])
    liste.append(['Policier', '?p=series&genre=policier'])
    liste.append(['Romance', '?p=series&genre=romance'])
    liste.append(['Science fiction', '?p=series&genre=science-fiction'])
    liste.append(['Spectacle', '?p=series&genre=spectacle'])
    liste.append(['Thriller', '?p=series&genre=thriller'])
    liste.append(['Western', '?p=series&genre=western'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenreAnime():
    oGui = cGui()

    liste = []
    liste.append(['Action', '?p=mangas&genre=action'])
    liste.append(['Arts Martiaux', '?p=mangas&genre=arts_martiaux'])
    liste.append(['Aventure', '?p=mangas&genre=aventure'])
    liste.append(['Combat', '?p=mangas&genre=combat'])
    liste.append(['Comédie', '?p=mangas&genre=comedie'])
    liste.append(['Cyberpunk', '?p=mangas&genre=cyberpunk'])
    liste.append(['Dark Fantasy', '?p=mangas&genre=dark-fantasy'])
    liste.append(['Drame', '?p=mangas&genre=drame'])
    liste.append(['Ecchi', '?p=mangas&genre=ecchi'])
    liste.append(['Ecole', '?p=mangas&genre=ecole'])
    liste.append(['Fantastique', '?p=mangas&genre=fantastique'])
    liste.append(['Gastronomie', '?p=mangas&genre=gastronomie'])
    liste.append(['Harem', '?p=mangas&genre=_harem'])
    liste.append(['Harem Inversé', '?p=mangas&genre=harem-inverse'])
    liste.append(['Heroic Fantasy', '?p=mangas&genre=heroïc-fantasy'])
    liste.append(['Historique', '?p=mangas&genre=historique'])
    liste.append(['Horreur', '?p=mangas&genre=horreur'])
    liste.append(['Magical Girl', '?p=mangas&genre=magical-girl'])
    liste.append(['Mature', '?p=mangas&genre=mature'])
    liste.append(['Mecha', '?p=mangas&genre=mecha'])
    liste.append(['Musical', '?p=mangas&genre=musical'])
    liste.append(['Mystère', '?p=mangas&genre=mystere'])
    liste.append(['Policier', '?p=mangas&genre=policier'])
    liste.append(['Psychologie', '?p=mangas&genre=psychologie'])
    liste.append(['Romance', '?p=mangas&genre=romance'])
    liste.append(['Science Fiction', '?p=mangas&genre=science-fiction'])
    liste.append(['Space Opera', '?p=mangas&genre=space-opera'])
    liste.append(['Sport', '?p=mangas&genre=sport'])
    liste.append(['Steampunk', '?p=mangas&genre=steampunk'])
    liste.append(['Surnaturel', '?p=mangas&genre=surnaturel'])
    liste.append(['Suspense', '?p=mangas&genre=suspense'])
    liste.append(['Tranche de Vie', '?p=mangas&genre=tranche-de-vie'])
    liste.append(['Thriller', '?p=mangas&genre=thriller'])
    liste.append(['Tournois', '?p=mangas&genre=tournois'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenreDivers():
    oGui = cGui()

    liste = []
    liste.append(['Actualités', '?p=autres-videos&genre=actualites'])
    liste.append(['Animaux', '?p=autres-videos&genre=animaux'])
    liste.append(['Concerts', '?p=autres-videos&genre=concerts'])
    liste.append(['Emission TV', '?p=autres-videos&genre=emissions-tv'])
    liste.append(['Géographie', '?p=autres-videos&genre=geographie'])
    liste.append(['High-tech', '?p=autres-videos&genre=high-tech'])
    liste.append(['Histoire', '?p=autres-videos&genre=histoire'])
    liste.append(['Humour', '?p=autres-videos&genre=humour'])
    liste.append(['Nature', '?p=autres-videos&genre=nature'])
    liste.append(['Sport', '?p=autres-videos&genre=sport'])
    liste.append(['Autres', '?p=autres-videos&genre=autres'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_ANIMS[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

        # par défaut
        sUrl = sSearch.replace(' ', '+').replace('%20', '+')
        # on replace le tag à la fin quelle que soit la position du tag trouvé
        if tagmovies in sUrl:
            sUrl = sUrl.replace(tagmovies, '')
            sUrl = sUrl + tagmovies

        if tagseries in sUrl:
            sUrl = sUrl.replace(tagseries, '')
            sUrl = sUrl + tagseries

        if tagmangas in sUrl:
            sUrl = sUrl.replace(tagmangas, '')
            sUrl = sUrl + tagmangas

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)"><img alt="([^"]+)" src="([^"]+)" class="img-responsive">.+?<p>([^<]+)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sLang = ''
            if 'p=autre' in sUrl:
                sTitle = aEntry[1]
                sThumb = URL_MAIN + aEntry[2]

            elif 'films' not in sUrl:
                sTitle = aEntry[1].split(' - ')[0] + ' ' + aEntry[1].split(' - ')[1]
                sTitle = sTitle.replace('Saison ', ' S')
                sLang = aEntry[1].split(' - ')[2].upper()
                sThumb = URL_MAIN + aEntry[2]

            else:
                sTitle = aEntry[1]
                sLang = aEntry[1].split(' - ')[1]
                sThumb = URL_MAIN + aEntry[2]

            sUrl2 = URL_MAIN + aEntry[0]
            sDesc = aEntry[3]

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche

            sDisplayTitle = ('%s (%s)') % (sTitle, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'p=autre' in sUrl:
                if ' Saison ' in sTitle:
                    oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, sDesc, sThumb, '', oOutputParameterHandler)
                else:
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sDesc, sThumb, '', oOutputParameterHandler)
            elif 'p=series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, sDesc, sThumb, '', oOutputParameterHandler)
            elif 'p=mangas' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, sDesc, sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, sDesc, sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = ">([^<]+)</a></li><li ><a href='([^']+)' rel='next'>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN + aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showMoviesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour ce film:[/COLOR]')

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = '<p>(.+?)<br /></p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<span>', '').replace('<b><i>', '').replace('</i></b>', '').replace('</span>', '')
            sDesc = sDesc.replace('<br>', ' ').replace('<br /><br />', ' ')
    except:
        pass

    # on recherche d'abord la qualité courante
    sPattern = '<i class="fa fa-folder-open"></i>\s*.+?<i>([^"]+)</i>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sQual = aResult[1][0].split(' - ')[0]
        sLang = aResult[1][0].split(' - ')[1]
        sTitle = ('%s %s (%s)') % (sMovieTitle, sQual, sLang)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sPattern = '<li><a href="([^"]+)"><button class=".+?>([^<]+)<i>([^<]+)</i> <i class=".+?"></i></button></a></li>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showSeriesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour cette saison:[/COLOR]')

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = '<p>(.+?)<br /></p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<span>', '').replace('<b><i>', '').replace('</i></b>', '').replace('</span>', '')\
                         .replace('<br>', ' ').replace('<br />', '')
    except:
        pass

    # Mise à jour du titre
    sPattern = '<title>(?:Télecharger|)(.+?)-(.+?) (.+?) .+?</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sSaison = aResult[1][0][2]
        sMovieTitle = (aResult[1][0][0].replace('&amp;', '') + aResult[1][0][1] + ' ' + aResult[1][0][2])
        sMovieTitle = sMovieTitle.replace('Télécharger ', '').replace('TÃ©lÃ©charger', '')

    # on recherche d'abord la langue courante
    sPattern = '<i class="fa fa-folder-open"></i>\s*.+?<i>([^"]+)</i>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sLang = ''
    if aResult[1]:
        sLang = aResult[1][0].replace(' - ', '')

    sDisplayTitle = ('%s [%s]') % (sMovieTitle, sLang.replace('|', ''))

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    html = CutQual(sHtmlContent)
    # on regarde si dispo dans d'autres langues
    sPattern1 = '<a href="([^"]+)">.+?><i>([^"]+)</i></button></a><'
    aResult1 = oParser.parse(html, sPattern1)

    if aResult1[0] is True:
        total = len(aResult1[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult1[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN + aEntry[0]
            sLang = aEntry[1]
            sDisplayTitle = ('%s (%s)') % (sMovieTitle, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    html = CutSais(sHtmlContent)
    # on regarde si dispo d'autres saisons
    sPattern2 = '<a href="([^"]+)">.+?>([^"]+)</button></a><'
    aResult2 = oParser.parse(html, sPattern2)

    # Affichage du texte
    if aResult2[0] is True:
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres Saisons disponibles pour cette série:[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult2[1]:

            sUrl = URL_MAIN + aEntry[0]
            sTitle = '[COLOR skyblue]' + aEntry[1].split(' - ')[1] + '[/COLOR]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern = '<a rel="external nofollow" href="([^"]+)" target="_blank" class="link">\s*<.+?a>\s*</td>\s*.+?>(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle + ' [COLOR coral]' + aEntry[1] + '[/COLOR] '
            sUrl = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'recapchaByPass', sTitle, sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<p>.+?</i> - (.+?)<span class="pull-right">|<a rel="external nofollow" href="([^"]+).+?text-center.+?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        epNumber = 0
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                epNumber = aEntry[0]
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            else:
                sTitle = sMovieTitle + ' ' + epNumber
                sDisplayTitle = ("%s [COLOR coral]%s[/COLOR]") % (sTitle, aEntry[2])
                sUrl2 = aEntry[1]

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'recapchaByPass', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '</i> Autres langues/qualités disponibles</div>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''


def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '</i> Autres saisons disponibles</div>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''


def recapchaByPass():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    from resources.lib import librecaptcha
    test = librecaptcha.get_token(api_key="6Le7kWkUAAAAAFtvD7VOtoSjPMXd6JGdl2CMZPw_", site_url=sUrl,
                                  user_agent=UA, gui=False, debug=False)

    data = 'subform=unlock&g-recaptcha-response=' + test
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="(.+?)" rel="external nofollow">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:

        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
