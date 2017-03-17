#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,xbmcgui,urllib,unicodedata

SITE_IDENTIFIER = 'streamay_bz'
SITE_NAME = 'Streamay.bz'
SITE_DESC = 'films en streaming'
URL_MAIN = 'http://streamay.bz/'

MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films/recents', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films?p=populaire', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films/', 'showGenre')

SERIE_SERIE = (URL_MAIN + 'series/alphabet', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series/', 'showGenre')

ANIM_ANIMS = (URL_MAIN + 'mangas', 'showMovies')

URL_SEARCH = ('', 'showResultSearch')
FUNCTION_SEARCH = 'showResultSearch'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films Les plus vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://parannee')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Années', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series Nouveautés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIE[1], 'Series Liste Complete', 'series.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Series Genre', 'genres.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animes', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showResultSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
        
def showNumBoard(sDefaultNum=''):
    dialog = xbmcgui.Dialog()
    numboard = dialog.numeric(0, 'Entrer une année ex: 2005', sDefaultNum)
    if numboard != None:
       return numboard
    return False
    
def selectAnn():
    oGui = cGui()
    newNum = showNumBoard()
    sUrl = 'http://streamay.bz/films/annee/' + newNum
    return sUrl

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    liste = []
    liste.append( ['Action',sUrl + 'genre/action'] )
    liste.append( ['Animation',sUrl + 'genre/animation'] )
    liste.append( ['Arts Martiaux',sUrl + 'genre/arts-martiaux'] )
    liste.append( ['Aventure',sUrl + 'genre/aventure'] )
    liste.append( ['Biopic',sUrl + 'genre/biopic'] )
    liste.append( ['Comedie',sUrl + 'genre/comedie'] )
    liste.append( ['Comedie Dramatique',sUrl + 'genre/comedie-dramatique'] )
    liste.append( ['Comedie Musicale',sUrl + 'genre/comedie-musicale'] )
    liste.append( ['Crime',sUrl + 'genre/crime'] )
    liste.append( ['Dessin Animé',sUrl + 'genre/dessin-anime'] )
    liste.append( ['Divers',sUrl + 'genre/divers'] )
    liste.append( ['Documentaire',sUrl + 'genre/documentaire'] )
    liste.append( ['Drame',sUrl + 'genre/drame'] )
    liste.append( ['Drama',sUrl + 'genre/drama'] )
    liste.append( ['Epouvante Horreur',sUrl + 'genre/epouvante-horreur'] ) 
    liste.append( ['Espionnage',sUrl + 'genre/espionnage'] )
    liste.append( ['Famille',sUrl + 'genre/famille'] )
    liste.append( ['Fantastique',sUrl + 'genre/fantastique'] )  
    liste.append( ['Guerre',sUrl + 'genre/guerre'] )
    liste.append( ['Historique',sUrl + 'genre/historique'] )
    liste.append( ['Horreur',sUrl + 'genre/horreur'] )
    liste.append( ['Judiciaire',sUrl + 'genre/judiciaire'] )
    liste.append( ['Médical',sUrl + 'genre/medical'] )
    liste.append( ['Musical',sUrl + 'genre/musical'] )
    liste.append( ['Policier',sUrl + 'genre/policier'] )
    liste.append( ['Peplum',sUrl + 'genre/peplum'] )
    liste.append( ['Romance',sUrl + 'genre/romance'] )
    liste.append( ['Science Fiction',sUrl + 'genre/science-fiction'] )
    liste.append( ['Soap',sUrl + 'genre/soap'] )
    liste.append( ['Spectacle',sUrl + 'genre/spectacle'] )
    liste.append( ['Sport Event',sUrl + 'genre/sport-event'] )
    liste.append( ['Thriller',sUrl + 'genre/thriller'] )
    liste.append( ['Western',sUrl + 'genre/western'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showResultSearch(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    post_data = {'k' : sSearch}
    data = urllib.urlencode(post_data)
    
    oRequest = cRequestHandler('http://streamay.bz/search')
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent',UA)
    oRequest.addParametersLine(data)
        
    sHtmlContent = oRequest.request()

    sHtmlContent = unicode(sHtmlContent,'utf-8')
    sHtmlContent = unicodedata.normalize('NFD', sHtmlContent).encode('ascii', 'ignore').decode("unicode_escape")
    sHtmlContent = sHtmlContent.encode("utf-8")
    sHtmlContent = sHtmlContent.replace("\n","")
    sHtmlContent = re.sub('"img":"([^"]+)","synopsis":"([^"]+)"','"synopsis":"\g<2>","img":"\g<1>"',sHtmlContent) #pattern en ordre img et syn inversé parfois


    sPattern = '{"result":{"id":".+?","title":"([^"]+)",.+?(?:"story"|"synopsis"):"(.+?)",*.+?(?:"img"|"banner"):"([^"]+)",.+?,"url":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sTitle = aEntry[0]
            sTitle = cUtil().removeHtmlTags(sTitle)
            sSyn = aEntry[1]
            sUrl = aEntry[3] 
            sThumb = URL_MAIN + 'cdn/img/' + aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            elif 'mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showAnime', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sSyn, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()
        
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oParser = cParser()
    
    if 'parannee' in sUrl:
        sUrl = selectAnn()
    else:
        sUrl = sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" class="mv">.+?<img src="([^"]+)" alt="">.+?<span>([^<>]+)<\/span>.+?<\/span>(.+?)<\/p>'
 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[2].decode("utf-8")
            sTitle = cUtil().unescape(sTitle).encode("utf-8")
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sSyn = aEntry[3].decode("utf-8")
            sSyn = cUtil().unescape(sSyn).encode("utf-8")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            elif 'mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showAnime', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sSyn, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^"]+)" rel="next">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
   
    sPattern = '<a class="head an choseSaison">(.+?)<\/a>|<a class="item" href="([^"]+)">.+?<span class="epitoto">(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
               sSaison = aEntry[0]
               oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + sSaison + '[/COLOR]') 
            else:
                sUrl = aEntry[1]
                sTitle = sMovieTitle + aEntry[2].replace('Regarder','')
                sDisplayTitle = cUtil().DecoTitle(sTitle)   
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
    oGui.setEndOfDirectory()
        

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" data-streamer="([^"]+)" data-v-on=".+?" data-id="([^"]+)"> <i style=".+?"></i> <span>(.+?)</span></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if 'stfr' in aEntry[1]:
                sLang = 'Vostfr'
            else:
                sLang = 'Vf'
                
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)   
            sHost = aEntry[3]    
            #sTitle = '[COLOR coral]' + sLang + '[/COLOR]' + ' ' + sDisplayTitle + ' ' + '[COLOR coral]>> ' + sHost + '[/COLOR]'
            sTitle = '%s [%s] [COLOR coral]%s[/COLOR]' %(sDisplayTitle, sLang, sHost)
            if 'serie' in sUrl:
                sUrlv = URL_MAIN + 'streamerSerie/' + aEntry[2] + '/' + aEntry[1]
            else:    
                sUrlv = URL_MAIN + 'streamer/' + aEntry[2] + '/' + aEntry[1]
                
            aTitle = sMovieTitle
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlv)
            oOutputParameterHandler.addParameter('sMovieTitle', aTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'GetLink', sTitle, '', sThumbnail, '', oOutputParameterHandler)     
    
        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
    
def GetLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'code":"([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl
                
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)  
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
    
def showAnime():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="chooseEpisodeManga" data-id="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sUrl2 = URL_MAIN + 'read/mepisodes/' + aResult[1][0]
        oRequestHandler = cRequestHandler(sUrl2)
        sHtmlContent = oRequestHandler.request()
        sPattern = '{"episodeNumber":"([^"]+)","id":"([^"]+)","manga_id":"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            total = len(aResult[1])
            dialog = cConfig().createDialog(SITE_NAME)
            for aEntry in aResult[1]:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                   break
                   
                sTitle = sMovieTitle + 'episode' + ' ' + aEntry[0]
                sDisplayTitle = cUtil().DecoTitle(sTitle)   
                sUrl3 = URL_MAIN + 'read/mepisode/' + aEntry[2] + '/' + aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl3)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oOutputParameterHandler.addParameter('sMangaid', aEntry[2])
                oOutputParameterHandler.addParameter('sEp', aEntry[0])
                oGui.addMovie(SITE_IDENTIFIER, 'showAnimeHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)     
    
            cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
    
def showAnimeHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sMangaid = oInputParameterHandler.getValue('sMangaid')
    sEp = oInputParameterHandler.getValue('sEp')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '{.+?"views":".+?",|"([^"]+)":"([^"]+)"|,"published":".+?".+}'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if aEntry[0]:
                if 'stfr' in aEntry[0]:
                    sLang = '[' + 'Vostfr' + ']'
                else:
                    sLang = '[' + 'Vf' + ']'
                
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)   
                sHost = aEntry[0].replace('_vostfr','')    
                sTitle = '[COLOR coral]' + sLang + '[/COLOR]' + ' ' + sDisplayTitle + ' ' + '[COLOR coral]>> ' + sHost + '[/COLOR]'
                sUrl = URL_MAIN + 'streamerMEpisode/' + sEp + '/' + sMangaid + '/' + aEntry[0] 
                aTitle = sMovieTitle
            
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', aTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addMovie(SITE_IDENTIFIER, 'GetLink', sTitle, '', sThumbnail, '', oOutputParameterHandler)     
    
        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
