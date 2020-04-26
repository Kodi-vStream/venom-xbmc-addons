# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.mino60.TmpName
import re
import unicodedata

from resources.lib.comaddon import progress
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Quote

SITE_IDENTIFIER = 'topimdb'
SITE_NAME = '[COLOR orange]Top 1000 IMDb[/COLOR]'
SITE_DESC = 'Base de donnees videos.'


URL_MAIN = 'https://www.imdb.com/'
POSTER_URL = 'https://ia.media-imdb.com/images/m/'
FANART_URL = 'https://ia.media-.imdb.com/images/m/'
# FANART_URL = 'https://image.tmdb.org/t/p/w780/'
# FANART_URL = 'https://image.tmdb.org/t/p/original/'

# URL_SEARCH = (URL_MAIN + '/find?ref_=nv_sr_fn&s=all&q=', 'showMovies')
# URL_SEARCH = (URL_MAIN + '/find?ref_=nv_sr_fn&q=&s=tt', 'showMovies')
# FUNCTION_SEARCH = 'showMovies'

MOVIE_WORLD = (URL_MAIN + 'search/title?groups=top_1000&sort=user_rating,desc&start=1', 'showMovies')
MOVIE_TOP250 = (URL_MAIN + 'search/title?count=100&groups=top_250', 'showMovies')
# MOVIE_TOP2021 = (URL_MAIN + 'search/title?year=2021,2021&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2020 = (URL_MAIN + 'search/title?year=2020,2020&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2019 = (URL_MAIN + 'search/title?year=2019,2019&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2018 = (URL_MAIN + 'search/title?year=2018,2018&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2017 = (URL_MAIN + 'search/title?year=2017,2017&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2016 = (URL_MAIN + 'search/title?year=2016,2016&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2015 = (URL_MAIN + 'search/title?year=2015,2015&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2014 = (URL_MAIN + 'search/title?year=2014,2014&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2013 = (URL_MAIN + 'search/title?year=2013,2013&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2012 = (URL_MAIN + 'search/title?year=2012,2012&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2011 = (URL_MAIN + 'search/title?year=2011,2011&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2010 = (URL_MAIN + 'search/title?year=2010,2010&title_type=feature&explore=languages', 'showMovies')


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


# def showSearch():
    # oGui = cGui()

    # sSearchText = oGui.showKeyBoard()
    # if (sSearchText != False):
        # sSearchText = cUtil().urlEncode(sSearchText)
        # sUrl = URL_MAIN + 'search/title?groups=top_1000&sort=user_rating,desc&start=%s' + sSearchText
        # sUrl = URL_SEARCH[0] + sSearchText

        # showMovies(sUrl)
        # oGui.setEndOfDirectory()
        # return


def load():
    oGui = cGui()

    # inutile
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_WORLD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_WORLD[1], 'Top Films Mondial', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP250[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP250[1], 'Top 250', 'films.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2021[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2021[1], 'Top Films 2021', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2020[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2020[1], 'Top Films 2020', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2019[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2019[1], 'Top Films 2019', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2018[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2018[1], 'Top Films 2018', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2017[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2017[1], 'Top Films 2017', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2016[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2016[1], 'Top Films 2016', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2015[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2015[1], 'Top Films 2015', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2014[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2014[1], 'Top Films 2014', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2013[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2013[1], 'Top Films 2013', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2012[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2012[1], 'Top Films 2012', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2011[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2011[1], 'Top Films 2011', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2010[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2010[1], 'Top Films 2010', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = '', page = 1):
    oGui = cGui()
    oParser = cParser()
    bGlobal_Search = False

    oInputParameterHandler = cInputParameterHandler()
    if sSearch:
        sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
    # if URL_SEARCH[0] in sSearch:
        # bGlobal_Search = True

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="lister-item-image.+?<img\salt="([^"]+)".+?loadlate="([^"]+)".+?class="lister-item-index.+?>([^<]+)</span>.+?class="lister-item-year.+?>([^<]+)</span.+?title="Users rated this(.+?)\s'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = unicode(aEntry[0], 'utf-8')  # converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')  # vire accent
            # sTitle = unescape(str(aEntry[1]))
            # sTitle = sTitle.encode( "utf-8")

            sTitle = ('%s %s %s [COLOR fuchsia]%s[/COLOR]') % (aEntry[2], aEntry[0], aEntry[3], aEntry[4])
            sMovieTitle=re.sub('(\[.*\])', '', sTitle)
            sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle)
            # sTitle2=re.sub('(.*)(\[.*\])','\\1 [COLOR orange]\\2[/COLOR]', sTitle)
            sThumb = aEntry[1].replace('UX67', 'UX328').replace('UY98', 'UY492').replace('67', '0').replace('98', '0')

            # sCom = unicode(aEntry[3], 'utf-8')#converti en unicode
            # sCom = unicodedata.normalize('NFD', sCom).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
            # sCom = unescape(sCom)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', ('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0]))
            # oOutputParameterHandler.addParameter('sThumb', str(aEntry[1]))
            # oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
            oOutputParameterHandler.addParameter('searchtext', showTitle(str(aEntry[0]), str('none')))
            oGui.addMovie('globalSearch', 'showSearch', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory('500')


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a\shref="([^"]+?)"class="lister-page-next'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = ('%s/%s') % (URL_MAIN, aResult[1][0])
        return sUrl

    return False


def showTitle(sMovieTitle, sUrl):

    sExtraTitle = ''
    # si c'est une serie
    if sUrl != 'none':
        sExtraTitle = sUrl.split('|')[1]
        sMovieTitle = sUrl.split('|')[0]

    # nettoyage du nom pr la recherche
    # print 'avant ' + sMovieTitle

    # ancien decodage
    sMovieTitle = unicode(sMovieTitle, 'utf-8')  # converti en unicode pour aider aux convertions
    sMovieTitle = unicodedata.normalize('NFD', sMovieTitle).encode('ascii', 'ignore').decode("unicode_escape")  # vire accent et '\'
    sMovieTitle = sMovieTitle.encode("utf-8").lower()  # on repasse en utf-8

    sMovieTitle = Quote(sMovieTitle)

    sMovieTitle = re.sub('\(.+?\)', ' ', sMovieTitle)  # vire les tags entre parentheses

    # modif venom si le titre comporte un - il doit le chercher
    sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle)  # vire les caracteres a la con qui peuvent trainer

    # sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)', ' ', sMovieTitle)  # vire les articles

    sMovieTitle = re.sub(' +', ' ', sMovieTitle)  # vire les espaces multiples et on laisse les espaces sans modifs car certains codent avec %20 d'autres avec +
    # print 'apres ' + sMovieTitle
    # modif ici
    if sExtraTitle:
        sMovieTitle = sMovieTitle.replace('%C3%A9', 'e').replace('%C3%A0', 'a')
        sMovieTitle = sMovieTitle + sExtraTitle
    else:
        sMovieTitle = sMovieTitle

    return sMovieTitle
