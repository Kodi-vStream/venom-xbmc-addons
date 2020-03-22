#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress
import urllib2, urllib, re

#Je garde le nom kepliz pour pas perturber
SITE_IDENTIFIER = 'kepliz_com'
SITE_NAME = 'Kepliz'
SITE_DESC = 'Films en streaming'

# Source compatible avec les clones : toblek, bofiaz, nimvon
# mais pas compatible avec les clones, qui ont une redirection direct : sajbo, trozam, radego
URL_HOST = 'http://www.wonior.com/'
URL_MAIN = 'URL_MAIN'

#pour l'addon
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'index.php?option=com_content&view=category&id=29&Itemid=7', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_HD = (URL_MAIN, 'showMovies')

ANIM_NEWS = (URL_MAIN + 'index.php?option=com_content&view=category&id=2&Itemid=2', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'index.php?option=com_content&view=category&id=2&Itemid=19', 'showMovies')
DOC_NEWS = (URL_MAIN + 'index.php?option=com_content&view=category&id=26', 'showMovies')
SHOW_SHOWS = (URL_MAIN + 'index.php?option=com_content&view=category&id=3', 'showMovies')#Spectacle

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_MISC = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SHOW_SHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, SHOW_SHOWS[1], 'Spectacles', 'doc.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['A l\'affiche', URL_MAIN + 'index.php?option=com_content&view=category&id=29'] )
    liste.append( ['Action', URL_MAIN + 'index.php?option=com_content&view=category&id=1'] )
    liste.append( ['Animation', URL_MAIN + 'index.php?option=com_content&view=category&id=2'] )
    liste.append( ['Aventure', URL_MAIN + 'index.php?option=com_content&view=category&id=4'] )
    liste.append( ['Comédie', URL_MAIN + 'index.php?option=com_content&view=category&id=6'] )
    liste.append( ['Documentaires', URL_MAIN + 'index.php?option=com_content&view=category&id=26'] )
    liste.append( ['Drame', URL_MAIN + 'index.php?option=com_content&view=category&id=7'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'index.php?option=com_content&view=category&id=9'] )
    liste.append( ['Fantastique',URL_MAIN + 'index.php?option=com_content&view=category&id=8'] )
    liste.append( ['Policier', URL_MAIN + 'index.php?option=com_content&view=category&id=10'] )
    liste.append( ['Science Fiction', URL_MAIN + 'index.php?option=com_content&view=category&id=11'] )
    liste.append( ['Spectacle', URL_MAIN + 'index.php?option=com_content&view=category&id=3'] )
    liste.append( ['Thriller', URL_MAIN + 'index.php?option=com_content&view=category&id=12'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        #limite de caractere sinon bug de la recherche
        sSearch = sSearch[:20]
        sUrl = URL_MAIN + 'index.php?ordering=&searchphrase=all&option=com_search&searchword=' + sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    # En cas de recherche direct OU lors de la navigation dans les differentes pages de résultats d'une recherche
    if('searchword=' in sUrl) :
        sPattern = '<h4><a href="\/[0-9a-zA-Z]+\/(.+?)"  >(.+?)<'
    else:
        sPattern = '<span style="list-style-type:none;" >.+? href="\/[0-9a-zA-Z]+\/(.+?)">(.+?)<\/a>'
    
    #L'url change tres souvent donc faut la retrouver
    req = urllib2.Request(URL_HOST)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    sMainUrl = ''
    aResult = oParser.parse(data, '<a.+?href="(/*[0-9a-zA-Z]+)"')   #Compatible avec plusieurs clones

    if aResult[0]:
        #memorisation pour la suite
        sMainUrl = URL_HOST + aResult[1][0] + '/'
        #correction de l'url
        sUrl = sUrl.replace('URL_MAIN', sMainUrl)
    else:
        #Si ca marche pas, pas la peine de continuer
        return

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

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

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]
            sTitle = re.sub('<font color="#[0-9a-f]{6}" *><i>HD<\/i><\/font>', '[HD]', sTitle)

            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sMainUrl + sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sMainUrl + sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="\/[0-9a-zA-Z]+\/([^"]+)" title="Suivant">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('<br/>', '')#traitement de sDesc

    #Recuperation info film, com et image
    sThumb = ''
    sDesc = ''
    sPattern = '<p style="text-align: center;"><img src="([^"]+)".+?<p style="text-align: left;">(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sThumb = aResult[1][0][0]
        sDesc = cUtil().unescape(aResult[1][0][1])

    #Recuperation info lien du stream.
    sLink = None
    sPostUrl = None
    sHtmlContent = sHtmlContent.replace('\r', '')

    #Format classique
    sPattern = 'GRUDALpluginsphp\("player1",{link:"([^"]+)"}\);'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0]):
        sLink = aResult[1][0]
        sPattern = '\/plugins\/([0-9a-zA-Z]+)\/plugins\/GRUDALpluginsphp.js"><\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            sPostUrl = sMainUrl + 'plugins/' + aResult[1][0] + '/plugins/GRUDALpluginsphp.php'

        if ((sLink) and (sPostUrl)):

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sLink', sLink)
            oOutputParameterHandler.addParameter('sPostUrl', sPostUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)

            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #Format rare
    if not sLink:

        sPattern = '<iframe src= *(?:"|)([^<>"]+\/player\.php\?id=.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):

            sMovieTitle = sMovieTitle.replace(' [HD]', '')
            sLink = aResult[1][0]
            if sLink.startswith('/'):
                sLink = URL_HOST[:-1] + sLink

            oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sLink', sLink)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)

            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink2', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #news Format
    if not sLink:

        sPattern = '<iframe src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):

            sMovieTitle = sMovieTitle.replace(' [HD]', '')
            sLink = aResult[1][0]
            if sLink.startswith('/'):
                sLink = URL_HOST[:-1] + sLink

            oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sLink', sLink)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)

            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink3', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHostersLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sLink = oInputParameterHandler.getValue('sLink')
    sPostUrl = oInputParameterHandler.getValue('sPostUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
    headers = {'User-Agent': UA,
               'Host': 'ozporo.com',
               'Referer': sUrl,
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    post_data = {'link': sLink}

    req = urllib2.Request(sPostUrl, urllib.urlencode(post_data), headers)

    response = urllib2.urlopen(req)
    data = response.read()
    response.close()

    sPattern = '"link":"([^"]+?)","label":"([^"]+?)"'
    aResult = oParser.parse(data, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sLink = aEntry[0]
            sQual = aEntry[1]
            sTitle = sMovieTitle + ' [' + sQual + ']'

            sHosterUrl = sLink
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()

def showHostersLink2():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    # sUrl = oInputParameterHandler.getValue('siteUrl')
    sLink = oInputParameterHandler.getValue('sLink')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    headers = {'User-Agent': UA,
               #'Host': 'grudal.com',
               'Referer': sLink,
               'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
               'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
               'Range': 'bytes=0-'
               #'Accept-Encoding': 'gzip, deflate',
               #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
               }

    req = urllib2.Request(sLink)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()

    sPattern = '"file":"([^"]+)","type":"mp4","label":"([^"]+)"'
    aResult = oParser.parse(data, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sLink2 = aEntry[0].replace('\/', '/')
            sQual = aEntry[1]
            sTitle = sMovieTitle + ' [' + sQual + ']'

            #decodage des liens
            req = urllib2.Request(sLink2, None, headers)

            try:
                response = urllib2.urlopen(req)
                sLink2 = response.geturl()
                response.close()

                sHosterUrl = str(sLink2)
                oHoster = cHosterGui().getHoster('lien_direct')
                #data = response.read()

            except urllib2.URLError, e:
                sLink2 = e.geturl()
                sHosterUrl = sLink2
                oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()

def showHostersLink3():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    # sUrl = oInputParameterHandler.getValue('siteUrl')
    sLink = oInputParameterHandler.getValue('sLink')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    headers = {'User-Agent': UA,
               #'Host': 'grudal.com',
               'Referer': sLink,
               'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
               'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
               'Range': 'bytes=0-'
               #'Accept-Encoding': 'gzip, deflate',
               #'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
               }

    #VSlog(sLink)

    req = urllib2.Request(sLink)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()

    # Recherche du premier lien
    sPattern = 'href=["\'](http[^"\']+)["\']'
    aResult = oParser.parse(data, sPattern)

    #fh = open('c:\\test.txt', "w")
    #fh.write(data)
    #fh.close()

    # Si il existe, suivi du lien
    if ( aResult[0] == True ):
        # VSlog(aResult[1][0])
        # sLink = sLink.rsplit('/', 1)[0] # supprime la dernière partie de l'url de l'iframe
        # VSlog(sLink)
        # href = sLink + '/' + aResult[1][0] # concaténation du résultat avec le href trouvé via regex
        # VSlog(href)

        #VSlog(aResult[1][0])
        req = urllib2.Request(aResult[1][0], None, headers)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()

    #VSlog(data)

    sPattern = 'file:"(.+?)".+?label:"(.+?)"'
    aResult = oParser.parse(data, sPattern)


    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sLink2 = aEntry[0].replace('\/', '/')
            sQual = aEntry[1]
            sTitle = sMovieTitle.replace(' [HD]', '')
            sTitle = sTitle + '[' + sQual + '] '

            if (False):
                #decodage des liens
                req = urllib2.Request(sLink2, None, headers)

                try:
                    response = urllib2.urlopen(req)
                    sLink2 = response.geturl()
                    response.close()

                    sHosterUrl = str(sLink2)
                    oHoster = cHosterGui().getHoster('lien_direct')
                    #data = response.read()

                except urllib2.URLError, e:
                    sLink2 = e.geturl()
                    sHosterUrl = str(sLink2)
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
            elif "amazonaws.com" in sLink2:
                sHosterUrl = str(sLink2)
                oHoster = cHosterGui().getHoster('lien_direct')
            else:
                sHosterUrl = str(sLink2)
                oHoster = cHosterGui().checkHoster(sHosterUrl)

            #VSlog(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()
