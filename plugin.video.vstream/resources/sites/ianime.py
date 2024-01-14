# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import random
import re
import unicodedata

from resources.lib.comaddon import progress, VSlog, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Unquote, QuotePlus

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

# Make random url
s = 'azertyuiopqsdfghjklmwxcvbn0123456789AZERTYUIOPQSDFGHJKLMWXCVBN'
RandomKey = ''.join(random.choice(s) for i in range(32))


SITE_IDENTIFIER = 'ianime'
SITE_NAME = 'I anime'
SITE_DESC = 'Animés en streaming'

URL_MAIN = 'https://www.ianimes.org/'

MOVIE_MOVIE = (URL_MAIN + 'films.php?liste=' + RandomKey, 'ShowAlpha')
MOVIE_GENRES = (URL_MAIN, 'showGenresMovies')

SERIE_SERIES = (URL_MAIN + 'series.php?liste=' + RandomKey, 'ShowAlpha')

ANIM_NEWS = (URL_MAIN + 'nouveautees.html', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes.php?liste=' + RandomKey, 'ShowAlpha')
ANIM_VFS = (URL_MAIN + 'listing_vf.php', 'ShowAlpha2')
ANIM_VOSTFRS = (URL_MAIN + 'listing_vostfr.php', 'ShowAlpha2')
ANIM_GENRES = (URL_MAIN + 'categorie.php?watch=' + RandomKey, 'showGenres')
ANIM_DRAMA = (URL_MAIN + 'drama.php', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH_MOVIES = ('movies=', 'showMovies')
URL_SEARCH_SERIES = ('tvshow=', 'showMovies')
URL_SEARCH_ANIMS = ('anime=', 'showMovies')
URL_SEARCH = (URL_MAIN + 'resultat+', 'showMovies')


def RandomReferer():
    return URL_MAIN + ''.join(random.choice(s) for i in range(32)) + '.htm'


def DecryptMangacity(chain):
    oParser = cParser()
    sPattern = '(.+?),\[(.+?)\],\[(.+?)\]\)'
    aResult2 = oParser.parse(chain, sPattern)
    d = ''

    if (aResult2[0] == True):

        a = aResult2[1][0][0]
        b = aResult2[1][0][1].replace('"', '').split(',')
        c = aResult2[1][0][2].replace('"', '').split(',')

        d = a
        for i in range(0, len(b)):
            d = d.replace(b[i], c[i])

        d = d.replace('%26', '&')
        d = d.replace('%3B', ';')

    return d


def FullUnescape(code):
    sPattern = '<script type="text/javascript">document\.write\(unescape\(".+?"\)\);</script>'
    aResult = re.findall(sPattern, code)
    if aResult:
        return Unquote(aResult[0])
    return code


def ICDecode(html):

    # if 'HTML/JavaScript Encoder' not in html:
    #     return html

    import math

    sPattern = 'language=javascript>c="([^"]+)";eval\(unescape\("([^"]+)"\)\);x\("([^"]+)"\);'
    aResult = re.findall(sPattern, html)

    if not aResult:
        return html

    c = aResult[0][0]
    # a = aResult[0][1]
    x = aResult[0][2]

    # premier decodage
    d = ''
    i = 0
    while i < len(c):
        if (i % 3 == 0):
            d = d + '%'
        else:
            d = d + c[i]
        i = i + 1

    # Recuperation du tableau
    aResult = re.findall('t=Array\(([0-9,]+)\);', Unquote(d))
    if not aResult:
        return ''

    t = aResult[0].split(',')
    l = len(x)
    b = 1024
    i = p = s = w = 0
    j = math.ceil(float(l) / b)
    r = ''

    while j > 0:

        i = min(l, b)
        while i > 0:
            w |= int(t[ord(x[p]) - 48]) << s
            p = p + 1
            if s:
                r = r + chr(165 ^ w & 255)
                w >>= 8
                s = s - 2
            else:
                s = 6

            i = i - 1
            l = l - 1

        j = j - 1

    return str(r)

# ------------------------------------------------------------------------------------


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche animés', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_DRAMA[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_DRAMA[1], 'Animés (Drama)', 'dramas.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sUrl + sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenresMovies():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'categorie_action_page1.html'])
    liste.append(['Animation', URL_MAIN + 'categorie_animation_page1.html'])
    liste.append(['Aventure', URL_MAIN + 'categorie_aventure_page1.html'])
    liste.append(['Combat', URL_MAIN + 'categorie_combats_page1.html'])
    liste.append(['Comédie', URL_MAIN + 'categorie_comedie_page1.html'])
    liste.append(['Drame', URL_MAIN + 'categorie_drame_page1.html'])
    liste.append(['Espionnage', URL_MAIN + 'categorie_espionnage_page1.html'])
    liste.append(['Fantastique', URL_MAIN + 'categorie_fantastique_page1.html'])
    liste.append(['Guerre', URL_MAIN + 'categorie_guerre_page1.html'])
    liste.append(['Horreur', URL_MAIN + 'categorie_epouvante_page1.html'])
    liste.append(['Musical', URL_MAIN + 'categorie_musical_page1.html'])
    liste.append(['Péplum', URL_MAIN + 'categorie_peplum_page1.html'])
    liste.append(['Policier', URL_MAIN + 'categorie_policier_page1.html'])
    liste.append(['Romance', URL_MAIN + 'categorie_romance_page1.html'])
    liste.append(['Thriller', URL_MAIN + 'categorie_thriller_page1.html'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# Retrouve les genres en dynamique dans la page
def showGenres():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    sPattern = '<center><a href="(.+?)" onmouseover="this.style.color.+?>(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    genres = []
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            sTitle = str(cUtil().unescape(sTitle))
            # on filtre les genres
            if 'Ecchi' in sTitle:
                continue
            sUrl = URL_MAIN + aEntry[0]
            genres.append((sTitle, sUrl))

        # Trie des genres par ordre alphabétique
        genres = sorted(genres, key=lambda genre: genre[0])

        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle, sUrl in genres:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowAlpha2():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl2 = URL_MAIN + 'animes.php?liste=' + RandomKey

    sType = 'VF'
    if 'vostfr' in sUrl:
        sType = 'VOSTFR'

    oRequestHandler = cRequestHandler(sUrl2)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    oParser = cParser()
    sPattern = '<a href=.(listing_(?:vf|vostfr)\.php\?affichage=[^<>"]+?). class=.button black pastel light. alt="Voir la liste des animes en ' + sType + '"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        ShowAlpha(URL_MAIN + aResult[1][0])


def ShowAlpha(url=None):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (url == None):
        sUrl = oInputParameterHandler.getValue('siteUrl')
    else:
        sUrl = url

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    sPattern = "<a href=.([^<>]+?). class=.button (?:red )*light.><headline6>(?:<font color=.black.>)*([A-Z#])(?:</font>)*</headline6></a>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sLetter = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [B][COLOR red]' + sLetter + '[/COLOR][/B]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        typeSearch, sSearch = sSearch.split('=')
        sSearch = Unquote(sSearch)
        sSearch = cUtil().CleanName(sSearch)
        sSearch = QuotePlus(sSearch).upper()  # remplace espace par + et passe en majuscule

        sUrl = URL_SEARCH[0] + sSearch + '.html'

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = cutSearch(sHtmlContent, typeSearch)

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', RandomReferer())
        sHtmlContent = oRequestHandler.request()
        # sHtmlContent = DecryptMangacity(sHtmlContent)

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    if sSearch or 'categorie.php' in sUrl or 'categorie_' in sUrl or 'listing3.php?' in sUrl or 'drama.php' in sUrl:
        sPattern = '<center><div style="background: url\(\'([^\'].+?)\'\); background-size.+?alt="(.+?)" title.+?<a href=["\']*(.+?)[\'"]* class=.button'
    else:
        sPattern = '<center><div style="background: url\(\'([^\'].+?)\'\); background-size.+?<a href="([^"]+)".+?alt="(.+?)"'

    sHtmlContent = re.sub('<a\s*href=\"categorie.php\?watch=\"\s*class="genre\s*\"', '', sHtmlContent, re.DOTALL)

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        isPython3 = isMatrix()

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            if sSearch or 'categorie.php' in sUrl or 'categorie_' in sUrl or 'listing3.php?' in sUrl or 'drama.php' in sUrl:
                sTitle = aEntry[1]
                sUrl2 = aEntry[2]
            else:
                sTitle = str(aEntry[2])
                sUrl2 = aEntry[1]

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            # affichage de la langue
            sLang = ''
            if 'VF' in sTitle:
                sLang = 'VF'
            elif 'VOSTFR' in sTitle:
                sLang = 'VOSTFR'

            # affichage de la qualité -> NON, qualité fausse
            # sQual = ''
            # if 'DVDRIP' in sTitle:
                # sQual = 'DVDRIP'

            # Nettoyer le titre
            sTitle = sTitle.replace(' DVDRIP', '').replace('Visionnez ', '')
            sTitle = sTitle.replace('[Streaming] - ', '').replace('gratuitement maintenant', '')
            if ' - Episode' in sTitle:
                sTitle = sTitle.replace(' -', '')

            if not isPython3:
                sTitle = cUtil().CleanName(sTitle).capitalize()
            else:
                sTitle.capitalize()

            sDisplayTitle = ('%s (%s)') % (sTitle, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'drama.php' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'animes.png', sThumb, '', oOutputParameterHandler)
            elif '?manga=' in sUrl2:
                oGui.addAnime(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'animes.png', sThumb, '', oOutputParameterHandler)
            elif '?serie=' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            elif '?film=' in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:  # une seule page par recherche
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Suivant', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()

    sPattern = 'class=.button red light. title=.Voir la page.+?<a href=.(.+?)(?:\'|") class=.button light.'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        sPattern = "<.table><center><center><a href='(.+?)' class='button light' title='Voir la page 1'>"
        aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False


def showEpisode():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', RandomReferer())
    sHtmlContent = oRequestHandler.request()

    try:
        sDesc = oParser.parse(sHtmlContent, '</headline15>.+?<font style=.+?>([^"]+)</font')[1][0]
    except:
        sDesc = ""

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    sPattern = '<headline11>(.+?)</headline11></a>|href="*([^"]+)"* title="([^"]+)"[^>]+style="*text-decoration:none;"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        isPython3 = isMatrix()

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            if not isPython3:
                sTitle = unicode(aEntry[2], 'iso-8859-1')
                sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')
                sTitle = sTitle.encode('ascii', 'ignore').decode('ascii').replace(' VF', '').replace(' VOSTFR', '')
            else:
                sTitle = aEntry[2]

            sTitle = cUtil().unescape(sTitle)

            sUrl2 = cUtil().unescape(aEntry[1])
            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            else:
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def extractLink(html):
    # Fake link
    fake1 = 'https://www.youtube.com'
    fake2 = '/api.js'

    final = ''

    oParser = cParser()

    sPattern = '(?i)src=(?:\'|")(.+?)(?:\'|")'
    aResult = re.findall(sPattern, html, re.DOTALL)

    if aResult:
        for a in aResult:
            if ('adnetworkperformance' in a) or ('jquery' in a):
                continue
            if fake1 not in a and fake2 not in a:
                final = a
                break

    sPattern = 'encodeURI\("(.+?)"\)'
    aResult = re.findall(sPattern, html)
    if aResult:
        if fake1 not in aResult[0] and fake2 not in aResult[0]:
            final = aResult[0]

    sPattern = "'file': '(.+?)',"
    aResult = oParser.parse(html, sPattern)
    if aResult[0] is True:
        if fake1 not in aResult[1][0] and fake2 not in aResult[1][0]:
            final = aResult[1][0]

    # nouveau codage
    if ';&#' in final:
        final = cUtil().unescape(final)

    if (not final.startswith('http')) and (len(final) > 2):
        final = URL_MAIN + final

    return final.replace(' ', '').replace('\n', '')


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', RandomReferer())
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    sHtmlContent = sHtmlContent.replace('<iframe src="http://www.promoliens.net', '')
    sHtmlContent = sHtmlContent.replace("<iframe src='cache_vote.php", '')

    sPattern = '<iframe.+?src=\'([^<>"]+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)

    sText = 'Animés dispo gratuitement et légalement sur :'
    if 'animedigitalnetwork.fr' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]" + sText + "[/COLOR][COLOR coral] anime digital network[/COLOR]")
    elif 'crunchyroll.com' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]" + sText + "[/COLOR][COLOR coral] crunchyroll[/COLOR]")
    elif 'wakanim.tv' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]" + sText + "[/COLOR][COLOR coral] wakanim[/COLOR]")
    else:
        list_url = []

        # 1 er methode
        sPattern = '<div class="box"><iframe.+?src=[\'|"](.+?)[\'|"]'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                if re.match(".+?&#[0-9]+;", aEntry):  # directe mais codé html
                    sHosterUrl = cUtil().unescape(aEntry)

                else:  # directe en clair
                    sHosterUrl = str(aEntry)

                # Ces liens sont toujours des liens
                if (not sHosterUrl.startswith('http')) and (len(sHosterUrl) > 2):
                    sHosterUrl = URL_MAIN + sHosterUrl

                list_url.append(sHosterUrl)

        # 2 eme methode
        sPattern = '<script>eval\(unescape\((.+?)\); eval\(unescape\((.+?)\);</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                # si url cryptee mangacity algo
                sHosterUrl = DecryptMangacity(aEntry[1])
                sHosterUrl = sHosterUrl.replace('\\', '')
                list_url.append(sHosterUrl)

        # 3 eme methode
        sPattern = 'document\.write\(unescape\("(%3c%.+?)"\)\);'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                tmp = Unquote(aEntry)

                sPattern2 = 'src=["\']([^"\']+)["\']'
                aResult = re.findall(sPattern2, tmp)
                if aResult:
                    list_url.append(aResult[0])

        if len(list_url) > 0:
            for aEntry in list_url:

                sHosterUrl = aEntry

                # Dans le cas ou l'adresse n'est pas directe,on cherche a l'extraire
                if not sHosterUrl[:4] == 'http':
                    sHosterUrl = extractLink(sHosterUrl)

                # Si aucun lien on arrete ici
                if not sHosterUrl:
                    continue

                # si openload code
                if 'openload2.php' in sHosterUrl:
                    # on telecharge la page

                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent = oRequestHandler.request()
                    # Et on remplace le code
                    sHtmlContent = ICDecode(sHtmlContent)
                    sHosterUrl = extractLink(sHtmlContent)

                # Passe par lien .asx ??
                sPattern = '(https*:\/\/www.ianime[^\/\\]+\/[0-9a-zA-Z_-]+\.asx)'
                aResult = oParser.parse(sHosterUrl, sPattern)
                if aResult[0]:
                    # on telecharge la page
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent = oRequestHandler.request()

                    # Si c'est une redirection, on passe juste le vrai lien
                    if 'ianime' not in oRequestHandler.getRealUrl().split('/')[2]:
                        sHosterUrl = oRequestHandler.getRealUrl()
                    else:
                        # Sinon on remplace le code
                        html = ICDecode(sHtmlContent)
                        sHosterUrl = extractLink(html)

                # Passe par lien .vxm ??
                # sPattern = 'http:\/\/www.ianime[^\/\\]+\/([0-9a-zA-Z_-]+)\.vxm'
                # aResult = oParser.parse(sHosterUrl, sPattern)
                # if aResult[0] :
                # sHosterUrl = 'http://embed.nowvideo.sx/embed.php?v=' + aResult[1][0]

                # redirection tinyurl
                if 'tinyurl' in sHosterUrl:
                    sHosterUrl = GetTinyUrl(sHosterUrl)

                # test pr liens raccourcis
                if 'http://goo.gl' in sHosterUrl:
                    try:
                        oRequestHandler = cRequestHandler(sHosterUrl)
                        oRequestHandler.addHeaderEntry('User-Agent', "Mozilla 5.10")
                        oRequestHandler.addHeaderEntry('Host', "goo.gl")
                        oRequestHandler.addHeaderEntry('Connection', 'keep-alive')
                        sHtmlContent = oRequestHandler.request()
                        sHosterUrl = oRequestHandler.getRealUrl()

                    except:
                        pass

                # Potection visio.php
                if '/visio.php?' in sHosterUrl:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent = oRequestHandler.request()

                    sHtmlContent = ICDecode(sHtmlContent)

                    sPattern = 'src=[\'"]([^\'"]+)[\'"]'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0]:
                        sHosterUrl = aResult[1][0]

                # Derniere en date
                sPattern = "(https*:\/\/www.ianime[^\/\\]+\/[^']+)"
                aResult = oParser.parse(sHosterUrl, sPattern)
                if aResult[0]:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)

                    sHtmlContent = oRequestHandler.request()

                    sHtmlContent = ICDecode(sHtmlContent)

                    sHosterUrl2 = extractLink(sHtmlContent)

                    if 'intern_player.png' in sHosterUrl2 or 'intern_player2.png' in sHosterUrl2:
                        xx = str(random.randint(300, 350))  # 347
                        yy = str(random.randint(200, 255))  # 216

                        oRequestHandler = cRequestHandler(sHosterUrl)
                        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
                        # Add params
                        oRequestHandler.addParameters('submit.x', xx)
                        oRequestHandler.addParameters('submit.y', yy)

                        # look for hidden params
                        p1 = re.search(r'name="valeur" value="([^"]+)"', sHtmlContent)
                        if p1:
                            oRequestHandler.addParameters('valeur', p1.group(1))

                        # Set headers
                        oRequestHandler.addHeaderEntry('Referer', sUrl)
                        oRequestHandler.addHeaderEntry('User-Agent', UA)
                        sHtmlContent = oRequestHandler.request()

                        sHosterUrl2 = extractLink(sHtmlContent)

                    sHosterUrl = sHosterUrl2

                if 'tinyurl' in sHosterUrl:
                    sHosterUrl = GetTinyUrl(sHosterUrl)

                if '///' in sHosterUrl:
                    sHosterUrl = 'https://' + '/'.join(sHosterUrl.split('/')[5:])

                VSlog(sHosterUrl)

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


# -------------------------------------------------------------------------------------------
def GetTinyUrl(url):
    if 'tinyurl' not in url:
        return url

    # Lien deja connu ?
    if '://tinyurl.com/h7c9sr7' in url:
        url = url.replace('://tinyurl.com/h7c9sr7/', '://vidwatch.me/')
    elif '://tinyurl.com/jxblgl5' in url:
        url = url.replace('://tinyurl.com/jxblgl5/', '://streamin.to/')
    elif '://tinyurl.com/q44uiep' in url:
        url = url.replace('://tinyurl.com/q44uiep/', '://openload.co/')
    elif '://tinyurl.com/jp3fg5x' in url:
        url = url.replace('://tinyurl.com/jp3fg5x/', '://allmyvideos.net/')
    elif '://tinyurl.com/kqhtvlv' in url:
        url = url.replace('://tinyurl.com/kqhtvlv/', '://openload.co/embed/')
    elif '://tinyurl.com/lr6ytvj' in url:
        url = url.replace('://tinyurl.com/lr6ytvj/', '://netu.tv/')
    elif '://tinyurl.com/kojastd' in url:
        url = url.replace('://tinyurl.com/kojastd/', '://www.rapidvideo.com/embed/')
    elif '://tinyurl.com/l3tjslm' in url:
        url = url.replace('://tinyurl.com/l3tjslm/', '://hqq.tv/player/')
    elif '://tinyurl.com/n34gtt7' in url:
        url = url.replace('://tinyurl.com/n34gtt7/', '://vidlox.tv/')
    elif '://tinyurl.com/kdo4xuk' in url:
        url = url.replace('://tinyurl.com/kdo4xuk/', '://watchers.to/')
    elif '://tinyurl.com/kjvlplm' in url:
        url = url.replace('://tinyurl.com/kjvlplm/', '://streamango.com/')
    elif '://tinyurl.com/kt3owzh' in url:
        url = url.replace('://tinyurl.com/kt3owzh/', '://estream.to/')

    # On va chercher le vrai lien
    else:
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.disableRedirect()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request()

        UrlRedirect = oRequestHandler.getRealUrl()

        if not(UrlRedirect == url):
            url = UrlRedirect
        elif 'Location' in reponse.getResponseHeader():
            url = reponse.getResponseHeader()['Location']
    return url


def cutSearch(sHtmlContent, typeSearch):
    types = {'movies': 'Films et Animations',
             'tvshow': 'S&eacute;ries et Drama',
             'anime': 'Animes et Mangas'}
    sPattern = types.get(typeSearch) + '<.+?alt="separateur"(.+?)alt="separateur"'

    aResult = cParser().parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''
