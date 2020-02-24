#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog

from urllib import unquote
import re

SITE_IDENTIFIER = 'disneyhd_tk'
SITE_NAME = 'Disney HD'
SITE_DESC = 'Disney HD: Tous les films Disney en streaming'

URL_MAIN = 'https://disneyhd.cf/'
URL_LISTE = URL_MAIN + '?page=liste.php'
ANIM_ENFANTS = ('http://', 'load')

#URL_SEARCH = ('', 'sHowResultSearch')
#URL_SEARCH_MOVIES = ('', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

sPattern1 = '<a href="([^"]+)".+?src="([^"]+)" alt.*?="(.+?)".*?>'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'

#**********************************************************
#
#  From https://github.com/Celend/bencode 
#

__data = bytes()
__s = 0
__l = 0
__enc = False


def Torrent_decode(x = None, enc=False):
    """param:
    1. bytes, the bytes will be decode.
    2. str or list, when can not decode with utf-8 charset will try using this charset decoding. 
return:
    object, unable decoding data will return bytes.
    """
    global __data, __s, __l, __enc;
    if enc != False:
        __enc = enc;
    if type(x) != bytes and x != None:
        raise TypeError("To decode the data type must be bytes.")
    elif x != None:
        __s = 0
        __l = 0
        __data = x
        __l = len(__data);
    #dict
    if __data[__s] == 100:
        __s += 1;
        d = {}
        while __s < __l-1:
            if __data[__s] not in range(48, 58):
                break;
                #raise RuntimeError("the dict key must be str.");
            key = Torrent_decode()
            value = Torrent_decode()
            d.update({key:value})
        __s += 1
        return d
    #int
    elif __data[__s] == 105:
        temp = __s + 1
        key = ''
        while __data[temp] in range(48, 58):
            key += str(__data[temp]-48)
            temp += 1
        __s += len(key) + 2
        return int(key);
    #string
    elif __data[__s] in range(48, 58):
        temp = __s;
        key  = ''
        while __data[temp] in range(48, 58):
            key += str(__data[temp]-48);
            temp += 1
        temp += 1
        key = __data[temp:temp+int(key)];
        __s = len(key)+temp;
        if type(__enc) == list:
            for ii in __enc:
                try:
                    return key.decode(ii);
                except:
                    continue
        else:
            try:
                return key.decode('utf-8');
            except:
                try:
                    return key.decode(__enc);
                except:
                    return key
    #list
    elif __data[__s] == 108:
        li = [];
        __s += 1;
        while __s < __l:
            if __data[__s] == 101:
                __s += 1
                break
            li.append(Torrent_decode())
        return li

#************************************************************************

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

    oRequestHandler = cRequestHandler(URL_MAIN + 'movies_list.php')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a class="item" href="([^"]+)" title="([^"]+)"> *<img src="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN + aEntry[2]
            sTitle = aEntry[1]

            if sSearch.lower() not in sTitle.lower():
                continue

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
    
    VSlog(sUrl)

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
    
    VSlog(sUrl)

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
                match = unquote(aResult[1][0])
                
                folder = re.findall('ws=(https[^&]+)', match)[0] + '/'
                torrent = re.findall('xs=(https[^&]+)', match)[0]
                
                oRequestHandler2 = cRequestHandler(torrent)
                torrent_data = oRequestHandler2.request()

                torrent = decode(torrent_data)
                
                VSlog(torrent)

                files = torrent['info']['files']
                name = torrent['info']['name']

                #for i in files:
                #    print (folder + name + '/' + i['path'][0])
            #Bon c'est mort
            else:
                oGui.addText(SITE_IDENTIFIER)

    oGui.setEndOfDirectory()
