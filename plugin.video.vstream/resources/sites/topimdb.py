# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import unicodedata

from resources.lib.comaddon import progress
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Quote

try:
    xrange
except NameError:
    xrange = range

SITE_IDENTIFIER = 'topimdb'
SITE_NAME = '[COLOR orange]Top 1000 IMDb[/COLOR]'
SITE_DESC = 'Base de donnees videos.'

URL_MAIN = 'https://www.imdb.com/'
POSTER_URL = 'https://ia.media-imdb.com/images/m/'
FANART_URL = 'https://ia.media-.imdb.com/images/m/'

MOVIE_WORLD = (URL_MAIN + 'search/title?groups=top_1000&sort=user_rating,desc&start=1', 'showMovies')
MOVIE_TOP250 = (URL_MAIN + 'search/title?count=100&groups=top_250', 'showMovies')
MOVIE_ANNEES = (True, 'showMovieYears')


def unescape(text):
    try:  # python 2
        import htmlentitydefs
    except ImportError:  # Python 3
        import html.entities as htmlentitydefs

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


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_WORLD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_WORLD[1], 'Top Films Mondial', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP250[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP250[1], 'Top 250', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Top (Par Années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    import datetime
    now = datetime.datetime.now()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(xrange(1903, int(now.year))):
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'search/title?year=' + str(i) + ',' + str(i) + '&title_type=feature&explore=languages')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(i), 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    # bGlobal_Search = False

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

    sPattern = 'img alt="([^"]+).+?loadlate="([^"]+).+?primary">([^<]+).+?unbold">([^<]+).+?(?:|rated this(.+?)\s.+?)muted">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # sTitle = unicode(aEntry[0], 'utf-8')  # converti en unicode
            # sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')  # vire accent
            # sTitle = unescape(str(aEntry[1]))
            # sTitle = sTitle.encode( "utf-8")

            sTitle = ('%s %s [COLOR fuchsia]%s[/COLOR]') % (aEntry[2], aEntry[0], aEntry[4])
            sThumb = aEntry[1].replace('UX67', 'UX328').replace('UY98', 'UY492').replace('67', '0').replace('98', '0')
            sYear = re.search('([0-9]{4})', aEntry[3]).group(1)
            sDesc = aEntry[5]

            oOutputParameterHandler.addParameter('siteUrl', 'none')
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('searchtext', showTitle(str(aEntry[0]), str('none')))
            oGui.addMovie('globalSearch', 'showSearch', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Suivant', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory('500')


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+?)"class="lister-page-next'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        sUrl = ('%s/%s') % (URL_MAIN, aResult[1][0])
        return sUrl

    return False


def showTitle(sMovieTitle, sUrl):

    sExtraTitle = ''
    # si c'est une série
    if sUrl != 'none':
        sExtraTitle = sUrl.split('|')[1]
        sMovieTitle = sUrl.split('|')[0]

    try:
        # ancien décodage
        sMovieTitle = unicode(sMovieTitle, 'utf-8')  # converti en unicode pour aider aux conversions
        sMovieTitle = unicodedata.normalize('NFD', sMovieTitle).encode('ascii', 'ignore').decode("unicode_escape")  # vire accent et '\'
        sMovieTitle = sMovieTitle.encode("utf-8").lower()  # on repasse en utf-8
    except:
        sMovieTitle = sMovieTitle.lower()

    sMovieTitle = Quote(sMovieTitle)
    sMovieTitle = re.sub('\(.+?\)', ' ', sMovieTitle)  # vire les tags entre parentheses

    # modif venom si le titre comporte un - il doit le chercher
    sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle)  # vire les caracteres a la con qui peuvent trainer
    # sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)', ' ', sMovieTitle)  # vire les articles

    # vire les espaces multiples et on laisse les espaces sans modifs car certains codent avec %20 d'autres avec +
    sMovieTitle = re.sub(' +', ' ', sMovieTitle)
    # modif ici
    if sExtraTitle:
        sMovieTitle = sMovieTitle.replace('%C3%A9', 'e').replace('%C3%A0', 'a')
        sMovieTitle = sMovieTitle + sExtraTitle
    else:
        sMovieTitle = sMovieTitle

    return sMovieTitle
