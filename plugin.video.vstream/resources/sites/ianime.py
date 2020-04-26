#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Unquote, QuotePlus
from resources.lib.comaddon import progress, VSlog
import urllib2, re
import unicodedata, random

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

#Make random url
s = 'azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN'
RandomKey = ''.join(random.choice(s) for i in range(32))


SITE_IDENTIFIER = 'ianime'
SITE_NAME = 'I anime'
SITE_DESC = 'Animés en streaming'

URL_MAIN = 'https://www.ianimes.org/'

MOVIE_MOVIE = (URL_MAIN + 'films.php?liste=' + RandomKey, 'ShowAlpha')
MOVIE_GENRES = (URL_MAIN , 'showGenresMovies')

SERIE_SERIES = (URL_MAIN + 'series.php?liste=' + RandomKey, 'ShowAlpha')

ANIM_NEWS = (URL_MAIN + 'nouveautees.html', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes.php?liste=' + RandomKey, 'ShowAlpha')
ANIM_VFS = (URL_MAIN + 'listing_vf.php', 'ShowAlpha2')
ANIM_VOSTFRS = (URL_MAIN + 'listing_vostfr.php', 'ShowAlpha2')
ANIM_GENRES = (URL_MAIN + 'categorie.php?watch=' + RandomKey, 'showGenres')

URL_SEARCH_SERIES = ('', 'showMovies')
URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

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
            d = d.replace( b[i], c[i])

        d = d.replace('%26', '&')
        d = d.replace('%3B', ';')

    return d

def FullUnescape(code):
    sPattern = '<script type="text\/javascript">document\.write\(unescape\(".+?"\)\);<\/script>'
    aResult = re.findall(sPattern, code)
    if aResult:
        return Unquote(aResult[0])
    return code

def ICDecode(html):

    #if 'HTML/JavaScript Encoder' not in html:
    #    return html

    import math

    sPattern = 'language=javascript>c="([^"]+)";eval\(unescape\("([^"]+)"\)\);x\("([^"]+)"\);'
    aResult = re.findall(sPattern, html)

    if not aResult:
        return html

    c = aResult[0][0]
    a = aResult[0][1]
    x = aResult[0][2]

    #premier decodage
    d = ''
    i = 0
    while i < len(c):
        if (i%3==0):
            d = d + '%'
        else:
            d = d + c[i];
        i = i + 1

    c = Unquote(d)
    #Recuperation du tableau
    aResult = re.findall('t=Array\(([0-9,]+)\);', c)
    if not aResult:
        return ''
    t = aResult[0].split(',')

    l = len(x)
    b = 1024
    i = j = r = p = 0
    s = 0
    w = 0

    j = math.ceil(float(l) / b)
    r = ''
    while j > 0:

        i = min(l, b)
        while i > 0:
            w |= int(t[ord(x[p]) - 48]) << s
            p = p + 1
            if (s):
                r = r + chr(165 ^ w & 255)
                w >>= 8
                s = s - 2
            else:
                s = 6

            i = i - 1
            l = l - 1

        j = j - 1

    return str(r)

#------------------------------------------------------------------------------------


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenresMovies(): #affiche les genres
    oGui = cGui()

    # Categories et liens associés
    liste = []
    liste.append( ['Action', URL_MAIN + 'categorie_action_page1.html'] )
    liste.append( ['Animation', URL_MAIN + 'categorie_animation_page1.html'] )
    liste.append( ['Aventure', URL_MAIN + 'categorie_aventure_page1.html'] )
    liste.append( ['Combat', URL_MAIN + 'categorie_combats_page1.html'] )
    liste.append( ['Comédie', URL_MAIN + 'categorie_comedie_page1.html'] )
    liste.append( ['Drame', URL_MAIN + 'categorie_drame_page1.html'] )
    liste.append( ['Espionnage', URL_MAIN + 'categorie_espionnage_page1.html'] )
    liste.append( ['Fantastique', URL_MAIN + 'categorie_fantastique_page1.html'] )
    liste.append( ['Guerre', URL_MAIN + 'categorie_guerre_page1.html'] )
    liste.append( ['Horreur', URL_MAIN + 'categorie_epouvante_page1.html'] )
    liste.append( ['Musical', URL_MAIN + 'categorie_musical_page1.html'] )
    liste.append( ['Péplum', URL_MAIN + 'categorie_peplum_page1.html'] )
    liste.append( ['Policier', URL_MAIN + 'categorie_policier_page1.html'] )
    liste.append( ['Romance', URL_MAIN + 'categorie_romance_page1.html'] )
    liste.append( ['Thriller', URL_MAIN + 'categorie_thriller_page1.html'] )
    
    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
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
            sTitle = str(cUtil().unescape(sTitle).encode("utf-8"))
            sUrl = URL_MAIN + aEntry[0]
            genres.append((sTitle, sUrl))

        # Trie des genres par ordre alphabétique
        genres = sorted(genres, key=lambda genre: genre[0])
        
        for sTitle,sUrl in genres:
            oOutputParameterHandler = cOutputParameterHandler()
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

def ShowAlpha(url = None):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (url == None):
        sUrl = oInputParameterHandler.getValue('siteUrl')
    else :
        sUrl = url

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    sPattern = "<a href=.([^<>]+?). class=.button (?:red )*light.><headline6>(?:<font color=.black.>)*([A-Z#])(?:<\/font>)*<\/headline6><\/a>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sLetter = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [B][COLOR red]' + sLetter + '[/COLOR][/B]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:

        #query_args = { 's': str(sSearch) }
        #data = urllib.urlencode(query_args)
        #headers = {'User-Agent' : 'Mozilla 5.10', 'Referer' : 'URL_MAIN'}
        #url = URL_MAIN + 'result.php'
        #request = urllib2.Request(url, data, headers)
        #reponse = urllib2.urlopen(request)

        sSearch = Unquote(sSearch)
        sSearch = QuotePlus(sSearch).upper() #remplace espace par + et passe en majuscule

        url = URL_MAIN + 'resultat+' + sSearch + '.html'

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        #sHtmlContent = DecryptMangacity(sHtmlContent)

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    if sSearch or 'categorie.php' in sUrl or 'categorie_' in sUrl or 'listing3.php?' in sUrl:
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

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break


            sThumb = aEntry[0]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            if sSearch or 'categorie.php' in sUrl or 'categorie_' in sUrl or 'listing3.php?' in sUrl:
                sTitle = aEntry[1]
                sUrl2 = aEntry[2]
            else:
                sTitle = str(aEntry[2])
                sUrl2 = aEntry[1]

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            #affichage de la langue
            sLang = ''
            if 'VF' in sTitle:
                sLang = 'VF'
            elif 'VOSTFR' in sTitle:
                sLang = 'VOSTFR'

            # affichage de la qualité -> NON, qualité fausse
#             sQual = ''
#             if 'DVDRIP' in sTitle:
#                 sQual = 'DVDRIP'

            # Nettoyer le titre
            sTitle = sTitle.replace(' DVDRIP', '')
            sTitle = sTitle.replace('Visionnez ', '').replace('[Streaming] - ', '').replace('gratuitement maintenant','')
            if ' - Episode' in sTitle:
                sTitle = sTitle.replace(' -', '')
            sTitle = cUtil().CleanName(sTitle).capitalize()

            sDisplayTitle = ('%s (%s)') % (sTitle, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '?manga=' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'animes.png', sThumb, '', oOutputParameterHandler)
            elif '?serie=' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            elif '?film=' in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if not sSearch: # une seule page par recherche
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()

    sPattern ='class=.button red light. title=.Voir la page.+?<a href=.(.+?)(?:\'|") class=.button light.'
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
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    #On fait 2 passage pr accelerer le parsing regex
    # sPattern = '<div class="&#105;&#110;&#110;&#101;&#114;">(.+?)<footer id="footer">'
    # aResult = oParser.parse(sHtmlContent, sPattern)

    # sPattern = '<img src="(.+?).+? alt="&#101;&#112;&#105;&#115;&#111;&#100;&#101;&#115;".+?<a href="(.+?)" title="(.+?)"'
    # aResult = oParser.parse(aResult[1][0], sPattern)

    sPattern = '<headline11>(.+?)<\/headline11><\/a>|<a href="*([^"]+)"* title="([^"]+)"[^>]+style="*text-decoration:none;"*>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = unicode(aEntry[2], 'iso-8859-1')
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')
            sTitle = sTitle.encode('ascii', 'ignore').decode('ascii').replace(' VF', '').replace(' VOSTFR', '')

            sTitle = cUtil().unescape(sTitle)

            sUrl2 = cUtil().unescape(aEntry[1])
            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            else:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def ExtractLink(html):
    #Fake link
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
            if fake1 not in a and fake2 not in a :
                final = a
                break

    sPattern = 'encodeURI\("(.+?)"\)'
    aResult = re.findall(sPattern, html)
    if aResult:
        if fake1 not in aResult[0] and fake2 not in aResult[0]:
            final = aResult[0]

    sPattern = "'file': '(.+?)',"
    aResult = oParser.parse(html, sPattern)
    if aResult[0] == True:
        if fake1 not in aResult[1][0] and fake2 not in aResult[1][0]:
            final = aResult[1][0]

    #nouveau codage
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
    sHtmlContent = oRequestHandler.request()

    #VSlog(sUrl)


    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    sHtmlContent = sHtmlContent.replace('<iframe src="http://www.promoliens.net', '')
    sHtmlContent = sHtmlContent.replace("<iframe src='cache_vote.php", '')

    list_url = []

    #1 er methode
    sPattern = '<div class="box"><iframe.+?src=[\'|"](.+?)[\'|"]'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if re.match(".+?&#[0-9]+;", aEntry):#directe mais codé html
                sHosterUrl = cUtil().unescape(aEntry)

            else:#directe en clair
                sHosterUrl = str(aEntry)

            #Ces liens sont tjours des liens
            if (not sHosterUrl.startswith('http')) and (len(sHosterUrl) > 2):
                sHosterUrl = URL_MAIN + sHosterUrl

            list_url.append(sHosterUrl)

    #2 eme methode
    sPattern = '<script>eval\(unescape\((.+?)\); eval\(unescape\((.+?)\);<\/script>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            #si url cryptee mangacity algo
            sHosterUrl = DecryptMangacity(aEntry[1])
            sHosterUrl = sHosterUrl.replace('\\', '')
            list_url.append(sHosterUrl)

    #3 eme methode
    sPattern = 'document\.write\(unescape\("(%3c%.+?)"\)\);'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        #VSlog("methode 3")
        for aEntry in aResult[1]:
            tmp = Unquote(aEntry)

            sPattern2 = 'src=["\']([^"\']+)["\']'
            aResult = re.findall(sPattern2, tmp)
            if aResult:
                list_url.append(aResult[0])

    #VSlog(str(list_url))

    if len(list_url) > 0:
        for aEntry in list_url:

            sHosterUrl = aEntry

            #Dans le cas ou l'adresse n'est pas directe,on cherche a l'extraire
            if not sHosterUrl[:4] == 'http':
                sHosterUrl = ExtractLink(sHosterUrl)

            #Si aucun lien on arrete ici
            if not sHosterUrl:
                continue

            #si openload code
            if 'openload2.php' in sHosterUrl:
                #on telecharge la page

                oRequestHandler = cRequestHandler(sHosterUrl )
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent = oRequestHandler.request()
                #Et on remplace le code
                sHtmlContent = ICDecode(sHtmlContent)
                sHosterUrl = ExtractLink(sHtmlContent)

            #Passe par lien .asx ??
            sPattern = '(https*:\/\/www.ianime[^\/\\]+\/[0-9a-zA-Z_-]+\.asx)'
            aResult = oParser.parse(sHosterUrl, sPattern)
            if aResult[0] :
                #on telecharge la page
                oRequestHandler = cRequestHandler(sHosterUrl )
                oRequestHandler.addHeaderEntry('Referer', sUrl)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent = oRequestHandler.request()

                #Si c'est une redirection, on passe juste le vrai lien
                if ('ianime' not in oRequestHandler.getRealUrl().split('/')[2]):
                    sHosterUrl = oRequestHandler.getRealUrl()
                else:
                    #Sinon on remplace le code
                    html = ICDecode(sHtmlContent)
                    sHosterUrl = ExtractLink(html)

            #Passe par lien .vxm ??
            #sPattern = 'http:\/\/www.ianime[^\/\\]+\/([0-9a-zA-Z_-]+)\.vxm'
            #aResult = oParser.parse(sHosterUrl, sPattern)
            #if aResult[0] :
            #    sHosterUrl = 'http://embed.nowvideo.sx/embed.php?v=' + aResult[1][0]

            #redirection tinyurl
            if 'tinyurl' in sHosterUrl:
                sHosterUrl = GetTinyUrl(sHosterUrl)


            #test pr liens raccourcis
            if 'http://goo.gl' in sHosterUrl:
                try:
                    headers = {'User-Agent' : 'Mozilla 5.10', 'Host' : 'goo.gl', 'Connection' : 'keep-alive'}
                    request = urllib2.Request(sHosterUrl, None, headers)
                    reponse = urllib2.urlopen(request)
                    sHosterUrl = reponse.geturl()
                except:
                    pass

            #Potection visio.php
            if '/visio.php?' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl )
                oRequestHandler.addHeaderEntry('Referer', sUrl)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent = oRequestHandler.request()

                sHtmlContent = ICDecode(sHtmlContent)

                sPattern = 'src=[\'"]([^\'"]+)[\'"]'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    sHosterUrl = aResult[1][0]

            #Derniere en date
            sPattern = "(https*:\/\/www.ianime[^\/\\]+\/[^']+)"
            aResult = oParser.parse(sHosterUrl, sPattern)
            if aResult[0]:

                VSlog('>>' + sHosterUrl)

                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('Referer', sUrl)
                oRequestHandler.addHeaderEntry('User-Agent', UA)

                sHtmlContent = oRequestHandler.request()

                sHtmlContent = ICDecode(sHtmlContent)

                sHosterUrl2 = ExtractLink(sHtmlContent)


                if 'intern_player.png' in sHosterUrl2 or 'intern_player2.png' in sHosterUrl2:
                    #VSlog('Fausse image : ' + sHosterUrl)

                    xx = str(random.randint(300, 350))#347
                    yy = str(random.randint(200, 255))#216

                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
                    #Add params
                    oRequestHandler.addParameters('submit.x', xx)
                    oRequestHandler.addParameters('submit.y', yy)

                    #look for hidden params
                    p1 = re.search(r'name="valeur" value="([^"]+)"', sHtmlContent)
                    if p1:
                        #VSlog('Hidden param')
                        oRequestHandler.addParameters('valeur', p1.group(1))

                    #Set headers
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent = oRequestHandler.request()

                    #VSlog("Img decode " + sHtmlContent)

                    sHosterUrl2 = ExtractLink(sHtmlContent)

                sHosterUrl = sHosterUrl2

            if 'tinyurl' in sHosterUrl:
                sHosterUrl = GetTinyUrl(sHosterUrl)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()



#-------------------------------------------------------------------------------------------
def GetTinyUrl(url):
    if not 'tinyurl' in url:
        return url

    #Lien deja connu ?
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

    #On va chercher le vrai lien
    else:

        #VSlog('Decodage lien tinyurl : ' + str(url))

        class NoRedirection(urllib2.HTTPErrorProcessor):
            def http_response(self, request, response):
                return response
            https_response = http_response

        headers9 = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'), ('Referer', URL_MAIN)]

        opener = urllib2.build_opener(NoRedirection)
        opener.addheaders = headers9
        reponse = opener.open(url, None, 5)

        UrlRedirect = reponse.geturl()

        if not(UrlRedirect == url):
            url = UrlRedirect
        elif 'Location' in reponse.headers:
            url = reponse.headers['Location']

        reponse.close()

    return url
