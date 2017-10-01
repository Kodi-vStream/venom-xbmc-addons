#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil,VSlog
import urllib2,urllib,re
import unicodedata


#Make random url
from random import choice
s = "azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN";
RandomKey = ''.join(choice(s) for i in range(32))


SITE_IDENTIFIER = 'mangacity_org'
SITE_NAME = 'I anime'
SITE_DESC = 'Animés en streaming'

URL_MAIN = 'http://www.ianimes.co/'

MOVIE_MOVIE = (URL_MAIN + 'films.php?liste=' + RandomKey , 'ShowAlpha')
MOVIE_GENRES = (URL_MAIN + 'films.php?liste=' + RandomKey , 'showGenres')

SERIE_SERIES = (URL_MAIN + 'series.php?liste=' + RandomKey , 'ShowAlpha')

ANIM_NEWS = (URL_MAIN + 'nouveautees.html', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes.php?liste=' + RandomKey, 'ShowAlpha')
ANIM_VFS = (URL_MAIN + 'listing_vf.php', 'ShowAlpha2')
ANIM_VOSTFRS = (URL_MAIN + 'listing_vostfr.php', 'ShowAlpha2')
ANIM_GENRES = (URL_MAIN + 'animes.php?liste=' + RandomKey , 'showGenres')

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def DecryptMangacity(chain):
    oParser = cParser()
    sPattern = '(.+?),\[(.+?)\],\[(.+?)\]\)'
    aResult2 = oParser.parse(chain, sPattern)
    d = ''

    if (aResult2[0] == True):

        a = aResult2[1][0][0]
        b = aResult2[1][0][1].replace('"','').split(',')
        c = aResult2[1][0][2].replace('"','').split(',')

        d = a
        for i in range(0, len(b)):
            d = d.replace( b[i], c[i])

        d = d.replace('%26', '&')
        d = d.replace('%3B', ';')

    return d

def FullUnescape(code):
    sPattern = '<script type="text\/javascript">document\.write\(unescape\(".+?"\)\);<\/script>'
    aResult = re.findall(sPattern,code)
    if aResult:
        return urllib.unquote(aResult[0])
    return code

def ICDecode(html):

    #if 'HTML/JavaScript Encoder' not in html:
    #    return html

    import math

    sPattern = 'language=javascript>c="([^"]+)";eval\(unescape\("([^"]+)"\)\);x\("([^"]+)"\);'
    aResult = re.findall(sPattern,html)

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
            d = d + "%"
        else:
            d = d + c[i];
        i = i + 1

    c = urllib.unquote(d)
    #Recuperation du tableau
    aResult = re.findall('t=Array\(([0-9,]+)\);',c)
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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'animes_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'animes_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    sPattern = '<center><a href="(.+?)" onmouseover="this.style.color.+?>(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sGenre = cUtil().unescape(aEntry[1]).decode("latin-1").encode("utf-8")
            Link = cUtil().unescape(aEntry[0])

            #sGenre = unicode(sGenre,'iso-8859-1')
            #sGenre = sGenre.encode('ascii', 'ignore').decode('ascii')

            sTitle = aEntry[1].decode("latin-1").encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + Link)
            oGui.addTV(SITE_IDENTIFIER, 'showMovies', sGenre, '', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def ShowAlpha2():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl2 = URL_MAIN + 'animes.php?liste=' + RandomKey

    sType = 'VF'
    if 'vostfr' in sUrl:
        sType = 'VOSTFR'

    #VSlog(sUrl2)

    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    oParser = cParser()
    sPattern = '<a href=.(listing_(?:vf|vostfr)\.php\?affichage=[^<>"]+?). class=.button black pastel light. alt="Voir la liste des animes en ' + sType + '"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        ShowAlpha( str(URL_MAIN) + aResult[1][0])

def ShowAlpha(url = None):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (url == None):
        sUrl = oInputParameterHandler.getValue('siteUrl')
    else :
        sUrl = url

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    sPattern = "<a href=.([^<>]+?). class=.button (?:red )*light.><headline6>(?:<font color=.black.>)*([A-Z#])(?:<\/font>)*<\/headline6><\/a>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sLetter = aEntry[1]
            Link = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + Link)
            oGui.addTV(SITE_IDENTIFIER, 'showMovies', 'Lettre [B][COLOR red]' + sLetter + '[/COLOR][/B]', '', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:

        #query_args = { 's': str(sSearch) }
        #data = urllib.urlencode(query_args)
        #headers = {'User-Agent' : 'Mozilla 5.10', 'Referer' : 'http://www.mangacity.org'}
        #url = URL_MAIN + 'result.php'
        #request = urllib2.Request(url,data,headers)
        #reponse = urllib2.urlopen(request)

        sSearch = urllib2.unquote(sSearch)
        sSearch = urllib.quote_plus(sSearch).upper() #passe en majuscule et remplace espace par +

        url = URL_MAIN + 'resultat+' + sSearch + '.html'

        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0','Referer' : URL_MAIN}
        request = urllib2.Request(url,None,headers)
        reponse = urllib2.urlopen(request)

        sHtmlContent = reponse.read()

        reponse.close()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        #sHtmlContent = DecryptMangacity(sHtmlContent)

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    if sHtmlContent.startswith('<script type="text/javascript">'):
        sHtmlContent = FullUnescape(sHtmlContent)

    sPattern = '<center><div style="background: url\(\'([^\'].+?)\'\); background-size.+?alt="(.+?)" title.+?<a href=["\']*(.+?)[\'"]* class=.button'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in list(set(aResult[1])):
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break

            sTitle = aEntry[1]
            #sTitle = unicode(sTitle, errors='replace')
            sTitle = unicode(sTitle,'iso-8859-1')
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')
            sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')

            sTitle = cUtil().unescape(sTitle)
            sTitle = sTitle.replace('[Streaming] - ','')

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            sPicture = aEntry[0]
            #sPicture = sPicture.encode('ascii', 'ignore').decode('ascii')
            #sPicture = sPicture.replace('[Streaming] - ','')
            sPicture = str(URL_MAIN) + str(sPicture)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sPicture)

            if '?manga=' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, sPicture, sPicture, 'animes.png', oOutputParameterHandler)
            elif '?serie=' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, sPicture, sPicture, 'series.png', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sPicture, sPicture, 'films.png', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        if sSearch:
            sNextPage = False
        else:
            sNextPage = __checkForNextPage(sHtmlContent,sUrl)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent,sUrl):
    oParser = cParser()

    sPattern ='class=.button red light. title=.Voir la page.+?<a href=.(.+?)(?:\'|") class=.button light.'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        sPattern = "<.table><center><center><a href='(.+?)' class='button light' title='Voir la page 1'>"
        aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return str(URL_MAIN) + str(aResult[1][0])

    return False

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    oParser = cParser()

    #On fait 2 passage pr accelerer le parsing regex
    # sPattern = '<div class="&#105;&#110;&#110;&#101;&#114;">(.+?)<footer id="footer">'
    # aResult = oParser.parse(sHtmlContent, sPattern)

    # sPattern = '<img src="(.+?).+? alt="&#101;&#112;&#105;&#115;&#111;&#100;&#101;&#115;".+?<a href="(.+?)" title="(.+?)"'
    # aResult = oParser.parse(aResult[1][0], sPattern)

    sPattern = 'class="button light" [^>]+"><headline11>(.+?)<\/headline11><\/a>|<a href="*([^"]+)"* title="([^"]+)"[^>]+style="*text-decoration:none;"*>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = unicode(aEntry[2],'iso-8859-1')
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')
            sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')

            sTitle = cUtil().unescape(sTitle)

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            sUrl2 = str(cUtil().unescape(aEntry[1]))

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oGui.addDir(SITE_IDENTIFIER, 'showEpisode', '[COLOR red]' + str(aEntry[0]) + '[/COLOR]', 'animes.png', oOutputParameterHandler)

            else:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sThumb, '', oOutputParameterHandler)
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def ExtractLink(html):
    final = ''

    oParser = cParser()

    sPattern = '(?i)src=(?:\'|")(.+?)(?:\'|")'
    aResult = re.findall(sPattern,html)
    loop = 0
    if aResult:
        for a in aResult:
            if 'adnetworkperformance' in a:
                continue
            final = a
            break

    sPattern = 'encodeURI\("(.+?)"\)'
    aResult = re.findall(sPattern,html)
    if aResult:
        final = aResult[0]

    sPattern = "'file': '(.+?)',"
    aResult = oParser.parse(html, sPattern)
    if aResult[0] == True:
        final = aResult[1][0]

    #nouveau codage
    if ';&#' in final:
        final = cUtil().unescape(final)

    if (not final.startswith( 'http' )) and (len(final) > 2) :
        final = URL_MAIN + final

    return final

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #VSlog(sUrl)
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    if 'HTML/JavaScript Encoder' in sHtmlContent:
        sHtmlContent = ICDecode(sHtmlContent)

    sHtmlContent = sHtmlContent.replace('<iframe src="http://www.promoliens.net','')
    sHtmlContent = sHtmlContent.replace("<iframe src='cache_vote.php",'')

    list_url = []
    oParser = cParser()

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
            if (not sHosterUrl.startswith( 'http' )) and (len(sHosterUrl) > 2) :
                sHosterUrl = URL_MAIN + sHosterUrl

            list_url.append(sHosterUrl)

    #2 eme methode
    sPattern = '<script>eval\(unescape\((.+?)\); eval\(unescape\((.+?)\);<\/script>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            #si url cryptee mangacity algo
            sHosterUrl = DecryptMangacity(aEntry[1])
            sHosterUrl = sHosterUrl.replace('\\','')
            list_url.append(sHosterUrl)

    #3 eme methode
    sPattern = 'document\.write\(unescape\("(%3c%.+?)"\)\);'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        VSlog("methode 3")
        for aEntry in aResult[1]:
            tmp = urllib.unquote(aEntry)

            sPattern2 = 'src=["\']([^"\']+)["\']'
            aResult = re.findall(sPattern2,tmp)
            if aResult:
                list_url.append(aResult[0])

    #VSlog(str(list_url))

    if len(list_url) > 0:
        total = len(list_url)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in list_url:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = aEntry

            #Dans le cas ou l'adresse n'est pas directe,on cherche a l'extraire
            if not (sHosterUrl[:4] == 'http'):
                sHosterUrl = ExtractLink(sHosterUrl)

            #Si aucun lien on arrete ici
            if not (sHosterUrl):
                continue

            #si openload code
            if 'openload2.php' in sHosterUrl:
                #on telecharge la page

                oRequestHandler = cRequestHandler(sHosterUrl )
                oRequestHandler.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
                sHtmlContent = oRequestHandler.request()
                #Et on remplace le code
                sHtmlContent = ICDecode(sHtmlContent)
                sHosterUrl = ExtractLink(sHtmlContent)

            #Passe par lien .asx ??
            sPattern = '(http:\/\/www.ianime[^\/\\]+\/[0-9a-zA-Z_-]+\.asx)'
            aResult = oParser.parse(sHosterUrl, sPattern)
            if aResult[0] :
                #on telecharge la page
                oRequestHandler = cRequestHandler(sHosterUrl )
                oRequestHandler.addHeaderEntry('Referer',sUrl)
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
                #Lien deja connu ?
                if '://tinyurl.com/h7c9sr7' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/h7c9sr7/','://vidwatch.me/')
                elif '://tinyurl.com/jxblgl5' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/jxblgl5/','://streamin.to/')
                elif '://tinyurl.com/q44uiep' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/q44uiep/','://openload.co/')
                elif '://tinyurl.com/jp3fg5x' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/jp3fg5x/','://allmyvideos.net/')
                elif '://tinyurl.com/kqhtvlv' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/kqhtvlv/','://openload.co/embed/')
                elif '://tinyurl.com/hymuk2f' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/hymuk2f/','://youwatch.org/')
                elif '://tinyurl.com/lr6ytvj' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/lr6ytvj/','://netu.tv/')
                elif '://tinyurl.com/kojastd' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/kojastd/','://www.rapidvideo.com/embed/')
                elif '://tinyurl.com/l3tjslm' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/l3tjslm/','://hqq.tv/player/')
                elif '://tinyurl.com/n34gtt7' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/n34gtt7/','://vidlox.tv/')
                elif '://tinyurl.com/kdo4xuk' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/kdo4xuk/','://watchers.to/')
                elif '://tinyurl.com/kjvlplm' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('://tinyurl.com/kjvlplm/','://streamango.com/')

                #On va chercher le vrai lien
                else:

                    VSlog('Decodage lien tinyurl : ' + str(sHosterUrl))

                    class NoRedirection(urllib2.HTTPErrorProcessor):
                        def http_response(self, request, response):
                            return response

                    headers9 = [('User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'),('Referer',URL_MAIN)]

                    opener = urllib2.build_opener(NoRedirection)
                    opener.addheaders = headers9
                    reponse = opener.open(sHosterUrl,None,5)

                    UrlRedirect = reponse.geturl()

                    if not(UrlRedirect == sHosterUrl):
                        sHosterUrl = UrlRedirect
                    elif 'Location' in reponse.headers:
                        sHosterUrl = reponse.headers['Location']

                    reponse.close()

            #test pr liens raccourcis
            if 'http://goo.gl' in sHosterUrl:
                try:
                    headers = {'User-Agent' : 'Mozilla 5.10','Host' : 'goo.gl', 'Connection' : 'keep-alive'}
                    request = urllib2.Request(sHosterUrl,None,headers)
                    reponse = urllib2.urlopen(request)
                    sHosterUrl = reponse.geturl()
                except:
                    pass

            #Potection visio.php
            if '/visio.php?' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl )
                oRequestHandler.addHeaderEntry('Referer',sUrl)
                sHtmlContent = oRequestHandler.request()

                sHtmlContent = ICDecode(sHtmlContent)

                sPattern = 'src=[\'"]([^\'"]+)[\'"]'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    sHosterUrl = aResult[1][0]

            #Derniere en date
            sPattern = "(http:\/\/www.ianime[^\/\\]+\/[^']+)"
            aResult = oParser.parse(sHosterUrl, sPattern)
            #VSlog(aResult)
            if aResult[0]:
                
                #VSlog(sHosterUrl)
                
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('Referer',sUrl)
                sHtmlContent = oRequestHandler.request()

                #fh = open('c:\\test.txt', "w")
                #fh.write(sHtmlContent)
                #fh.close()
                
                sHtmlContent = ICDecode(sHtmlContent)

                sHosterUrl = ExtractLink(sHtmlContent)
                #VSlog(sHosterUrl)
                if 'tinyurl' in sHosterUrl:
                    if '://tinyurl.com/kt3owzh' in sHosterUrl:
                        sHosterUrl = sHosterUrl.replace('://tinyurl.com/kt3owzh/','://estream.to/')
                        
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
