#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
return False#au 18/03/2020
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.util import Unquote

import re

SITE_IDENTIFIER = 'disneyhd_tk'
SITE_NAME = 'Disney HD'
SITE_DESC = 'Disney HD: Tous les films Disney en streaming'

URL_MAIN = 'https://disneyhd.cf/'
URL_LISTE = URL_MAIN + '?page=liste.php'
ANIM_ENFANTS = ('http://', 'load')

FUNCTION_SEARCH = 'sHowResultSearch'
URL_SEARCH = ('', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = ('', FUNCTION_SEARCH)

sPattern1 = '<a href="([^"]+)".+?src="([^"]+)" alt.*?="(.+?)".*?>'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'

###################################################################################
#DECODE TORRENT : https://effbot.org/zone/bencode.htm
###################################################################################

def tokenize(text, match=re.compile("([idel])|(\d+):|(-?\d+)").match):
    i = 0
    while i < len(text):
        m = match(text, i)
        s = m.group(m.lastindex)
        i = m.end()
        if m.lastindex == 2:
            yield "s"
            yield text[i:i+int(s)]
            i = i + int(s)
        else:
            yield s

def decode_item(nextItem, token):
    if token == "i":
        # integer: "i" value "e"
        data = int(next())
        if next() != "e":
            raise ValueError
    elif token == "s":
        # string: "s" value (virtual tokens)
        data = next()
    elif token == "l" or token == "d":
        # container: "l" (or "d") values "e"
        data = []
        tok = next()
        while tok != "e":
            data.append(decode_item(nextItem, tok))
            tok = next()
        if token == "d":
            data = dict(zip(data[0::2], data[1::2]))
    else:
        raise ValueError
    return data

def decode(text):
    try:
        src = tokenize(text)
        data = decode_item(src.next, src.next())
        for token in src: # look for more tokens
            raise SyntaxError("trailing junk")
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("syntax error")
    return data

###################################################################################

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oOutputParameterHandler.addParameter('filtre', 'ajouts')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Ajouts récents', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oOutputParameterHandler.addParameter('filtre', 'populaires')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Populaires', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_LISTE)
    oOutputParameterHandler.addParameter('filtre', 'liste')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Liste des films', 'enfants.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sHowResultSearch(str(sSearchText))
        oGui.setEndOfDirectory()
        return

def sHowResultSearch(sSearch = ''):
    oGui = cGui()

    sSearch = Unquote(sSearch)

    oRequestHandler = cRequestHandler(URL_MAIN + 'movies_list.php')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a class="item" href="([^"]+)" title="([^"]+)"> *<img src="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            if sSearch.lower() not in sTitle.lower():
                continue

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN + aEntry[2]
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'enfants.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def order(sList, sIndex):
    #remet en ordre le résultat du parser par un index ici par le titre qui est en position 2
    #exemple: ('http://venom', 'sThumb', 'sTitle')
    #          aResult = order(aResult[1], 2)
    aResult = sorted(sList, key=lambda a:a[sIndex])
    #retourne au format du parser
    return True, aResult

def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if oInputParameterHandler.exist('filtre'):
        sFiltre = oInputParameterHandler.getValue('filtre')
    else:
        sFiltre = "none"

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'ajouts' in sFiltre:
        sHtmlContent = oParser.abParse(sHtmlContent, '</i> Derniers ajouts', '</section>')
        aResult = oParser.parse(sHtmlContent, sPattern1)
    elif 'populaires' in sFiltre:
        sHtmlContent = oParser.abParse(sHtmlContent, '</i> Les plus populaires', '</i> Visionnés en ce moment')
        aResult = oParser.parse(sHtmlContent, sPattern1)
    else:
        sHtmlContent = oParser.abParse(sHtmlContent, 'style', '</html>')
        aResult = oParser.parse(sHtmlContent, sPattern1)
        aResult = order(aResult[1], 2)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)


    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = aEntry[2].replace('streaming', '').replace(' 1080p', '').replace('_', ' ')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if aEntry[0].startswith('s-'):
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, 'enfants.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'enfants.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

#Non utilisé
def ShowList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    aResult = oParser.parse(sHtmlContent, '<li data-arr_pos="([0-9]+)">([^<]+)<')
    
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'enfants.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    #film
    if '<ol id="playlist">' in sHtmlContent:
        sPattern = '<li data-trackurl="([^"]+)">(.+?)<\/li>'
    elif 'data-ws=' in sHtmlContent:
        sPattern = 'data-ws="([^"]+)">(.+?)</span>'
    else:
        sPattern = 'class="qualiteversion" data-qualurl="([^"]+)">([^"]+)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            sFinalTitle = sMovieTitle + ' ' + aEntry[1]

            if '/mp4/' in sHosterUrl and not 'http' in sHosterUrl:
                sHosterUrl = 'http://disneyhd.tk%s' % sHosterUrl

            if '//goo.gl' in sHosterUrl:
                import urllib2
                try:
                    class NoRedirection(urllib2.HTTPErrorProcessor):
                        def http_response(self, request, response):
                            return response
                        https_response = http_response

                    opener = urllib2.build_opener(NoRedirection)
                    opener.addheaders.append (('User-Agent', UA))
                    opener.addheaders.append (('Connection', 'keep-alive'))

                    HttpReponse = opener.open(url8)
                    sHosterUrl = HttpReponse.headers['Location']
                    sHosterUrl = sHosterUrl.replace('https', 'http')
                except:
                    pass

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sFinalTitle)
                oHoster.setFileName(sFinalTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        #playlist-serie lien direct http pour le moment
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHosterUrl = aEntry[0]
                sTitle = aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        else:
            #Dernier essai avec les torrent
            aResult = oParser.parse(sHtmlContent, 'data-maglink="([^"]+)')
            if (aResult[0] == True):
                match = Unquote(aResult[1][0])
                
                folder = re.findall('ws=(https[^&]+)', match)[0] + '/'
                torrent = re.findall('xs=(https[^&]+)', match)[0]
                
                oRequestHandler2 = cRequestHandler(torrent)
                torrent = decode(oRequestHandler2.request())

                files = torrent['info']['files']
                name = torrent['info']['name']

                count = 0
                for i in files:
                    sHosterUrl = (folder + name + '/' + i['path'][0])
                    count = count + 1

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle + " " + name + "E" + str(count))
                        oHoster.setFileName(sMovieTitle + " " + name + "E" + str(count))
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            else:
                oGui.addText(SITE_IDENTIFIER)

    oGui.setEndOfDirectory()
