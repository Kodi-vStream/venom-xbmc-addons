#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,xbmcgui,urllib,unicodedata

SITE_IDENTIFIER = 'streamay_bz'
SITE_NAME = 'Streamay'
SITE_DESC = 'Films/ Séries & Mangas en streaming'
URL_MAIN = 'https://streamay.bz/'

MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films/recents', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films?p=populaire', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (URL_MAIN + 'films/annee/', 'showMovies')
MOVIE_PAYS = (True, 'showPays')

SERIE_SERIES = (URL_MAIN + 'series/alphabet', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

ANIM_ANIMS = (URL_MAIN + 'mangas', 'showMovies')
ANIM_GENRES = (True, 'showAnimGenres')

URL_SEARCH = ('', 'showResultSearch')
FUNCTION_SEARCH = 'showResultSearch'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'films_views.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Par Pays)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'series_genres.png', oOutputParameterHandler)
    
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
    sUrl = MOVIE_ANNEES[0] + newNum
    return sUrl

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'films/genre/action'] )
    liste.append( ['Animation',URL_MAIN + 'films/genre/animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'films/genre/arts-martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'films/genre/aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'films/genre/biopic'] )
    liste.append( ['Comédie',URL_MAIN + 'films/genre/comedie'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'films/genre/comedie-dramatique'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'films/genre/comedie-musicale'] )
    liste.append( ['Crime',URL_MAIN + 'films/genre/crime'] )
    liste.append( ['Dessin Animé',URL_MAIN + 'films/genre/dessin-anime'] )
    liste.append( ['Divers',URL_MAIN + 'films/genre/divers'] )
    liste.append( ['Documentaire',URL_MAIN + 'films/genre/documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'films/genre/drame'] )
    liste.append( ['Drama',URL_MAIN + 'films/genre/drama'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'films/genre/epouvante-horreur'] )
    liste.append( ['Espionnage',URL_MAIN + 'films/genre/espionnage'] )
    liste.append( ['Famille',URL_MAIN + 'films/genre/famille'] )
    liste.append( ['Fantastique',URL_MAIN + 'films/genre/fantastique'] )  
    liste.append( ['Guerre',URL_MAIN + 'films/genre/guerre'] )
    liste.append( ['Historique',URL_MAIN + 'films/genre/historique'] )
    liste.append( ['Horreur',URL_MAIN + 'films/genre/horreur'] )
    liste.append( ['Judiciaire',URL_MAIN + 'films/genre/judiciaire'] )
    liste.append( ['Musical',URL_MAIN + 'films/genre/musical'] )
    liste.append( ['Policier',URL_MAIN + 'films/genre/policier'] )
    liste.append( ['Péplum',URL_MAIN + 'films/genre/peplum'] )
    liste.append( ['Romance',URL_MAIN + 'films/genre/romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'films/genre/science-fiction'] )
    liste.append( ['Spectacle',URL_MAIN + 'films/genre/spectacle'] )
    liste.append( ['Sport Event',URL_MAIN + 'films/genre/sport-event'] )
    liste.append( ['Thriller',URL_MAIN + 'films/genre/thriller'] )
    liste.append( ['Western',URL_MAIN + 'films/genre/western'] )

    for sTitle,sUrl in liste:
	
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'series/genre/action'] )
    liste.append( ['Animation',URL_MAIN + 'series/genre/animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'series/genre/arts-martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'series/genre/aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'series/genre/biopic'] )
    liste.append( ['Classique',URL_MAIN + 'series/genre/classique'] )
    liste.append( ['Comédie',URL_MAIN + 'series/genre/comedie'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'series/genre/comedie-dramatique'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'series/genre/comedie-musicale'] )
    liste.append( ['Dessin Animé',URL_MAIN + 'series/genre/dessin-anime'] )
    liste.append( ['Divers',URL_MAIN + 'series/genre/divers'] )
    liste.append( ['Drame',URL_MAIN + 'series/genre/drame'] )
    liste.append( ['Drama',URL_MAIN + 'series/genre/drama'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'series/genre/epouvante-horreur'] )
    liste.append( ['Espionnage',URL_MAIN + 'series/genre/espionnage'] )
    liste.append( ['Famille',URL_MAIN + 'series/genre/famille'] )
    liste.append( ['Fantastique',URL_MAIN + 'series/genre/fantastique'] )  
    liste.append( ['Guerre',URL_MAIN + 'series/genre/guerre'] )
    liste.append( ['Historique',URL_MAIN + 'series/genre/historique'] )
    liste.append( ['Judiciaire',URL_MAIN + 'series/genre/judiciaire'] )
    liste.append( ['Médical',URL_MAIN + 'series/genre/medical'] )
    liste.append( ['Musical',URL_MAIN + 'series/genre/musical'] )
    liste.append( ['Péplum',URL_MAIN + 'series/genre/peplum'] )
    liste.append( ['Policier',URL_MAIN + 'series/genre/policier'] )
    liste.append( ['Romance',URL_MAIN + 'series/genre/romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'series/genre/science-fiction'] )
    liste.append( ['Soap',URL_MAIN + 'series/genre/soap'] )
    liste.append( ['Sport Event',URL_MAIN + 'series/genre/sport-event'] )
    liste.append( ['Thriller',URL_MAIN + 'series/genre/thriller'] )
    liste.append( ['Western',URL_MAIN + 'series/genre/western'] )

    for sTitle,sUrl in liste:
	
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimGenres():
    oGui = cGui()
	
    liste = []
    liste.append( ['Action',URL_MAIN + 'mangas/genre/action'] )
    liste.append( ['Amour & Amitié',URL_MAIN + 'mangas/genre/amour-amitie'] )
    liste.append( ['Animation',URL_MAIN + 'mangas/genre/animation'] )
    liste.append( ['Aventure',URL_MAIN + 'mangas/genre/aventure'] )
    liste.append( ['Calligraphie',URL_MAIN + 'mangas/genre/calligraphie'] )
    liste.append( ['Chanbara',URL_MAIN + 'mangas/genre/chanbara'] )
    liste.append( ['Combat & Arts Martiaux',URL_MAIN + 'mangas/genre/combat-arts-martiaux'] )
    liste.append( ['Comédie',URL_MAIN + 'mangas/genre/comedie'] )
    liste.append( ['Comédie romantique',URL_MAIN + 'mangas/genre/comedie-romantique'] )
    liste.append( ['Course automobile',URL_MAIN + 'mangas/genre/course-automobile'] )
    liste.append( ['Crime',URL_MAIN + 'mangas/genre/crime'] )
    liste.append( ['Cuisine',URL_MAIN + 'mangas/genre/cuisine'] )
    liste.append( ['Cyber & Mecha',URL_MAIN + 'mangas/genre/cyber-mecha'] )
    liste.append( ['Cyberpunk',URL_MAIN + 'mangas/genre/cyberpunk'] )
    liste.append( ['Dance',URL_MAIN + 'mangas/genre/dance'] )
    liste.append( ['Drame',URL_MAIN + 'mangas/genre/drame'] )
    liste.append( ['Ecchi',URL_MAIN + 'mangas/genre/ecchi'] )
    liste.append( ['Ecole',URL_MAIN + 'mangas/genre/ecole'] )
    liste.append( ['Ecologie',URL_MAIN + 'mangas/genre/ecologie'] )
    liste.append( ['Enigme & Policier',URL_MAIN + 'mangas/genre/enigme-policier'] )
    liste.append( ['Espace & Sci-Fiction',URL_MAIN + 'mangas/genre/espace-sci-fiction'] )
    liste.append( ['Fantastique',URL_MAIN + 'mangas/genre/fantastique'] )  
    liste.append( ['Fantastique & Mythe',URL_MAIN + 'mangas/genre/fantastique-mythe'] )  
    liste.append( ['Fantasy',URL_MAIN + 'mangas/genre/fantasy'] )  
    liste.append( ['Fashion',URL_MAIN + 'mangas/genre/fasion'] )  
    liste.append( ['Football',URL_MAIN + 'mangas/genre/football'] )  
    liste.append( ['Gangster',URL_MAIN + 'mangas/genre/gangster'] )  
    liste.append( ['Gastronomie',URL_MAIN + 'mangas/genre/gastronomie'] )  
    liste.append( ['Hip-Hop',URL_MAIN + 'mangas/genre/hip-hop'] )  
    liste.append( ['Histoire de famille',URL_MAIN + 'mangas/genre/histoire-de-famille'] )  
    liste.append( ['Historique',URL_MAIN + 'mangas/genre/historique'] )  
    liste.append( ['Horreur',URL_MAIN + 'mangas/genre/horreur'] )  
    liste.append( ['Jeu',URL_MAIN + 'mangas/genre/jeu'] )  
    liste.append( ['Lycée',URL_MAIN + 'mangas/genre/lycee'] )  
    liste.append( ['Mafia',URL_MAIN + 'mangas/genre/mafia'] )  
    liste.append( ['Magical girl',URL_MAIN + 'mangas/genre/magical-girl'] )  
    liste.append( ['Magie',URL_MAIN + 'mangas/genre/magie'] )  
    liste.append( ['Mecha',URL_MAIN + 'mangas/genre/mecha'] )  
    liste.append( ['Musique',URL_MAIN + 'mangas/genre/musique'] )  
    liste.append( ['Mystère',URL_MAIN + 'mangas/genre/mystere'] )
    liste.append( ['Nekketsu',URL_MAIN + 'mangas/genre/nekketsu'] )
    liste.append( ['Ninja',URL_MAIN + 'mangas/genre/ninja'] )
    liste.append( ['Parodie',URL_MAIN + 'mangas/genre/parodie'] )
    liste.append( ['Policier',URL_MAIN + 'mangas/genre/policier'] )
    liste.append( ['Psycologique',URL_MAIN + 'mangas/genre/psycologique'] )
    liste.append( ['Réflexion',URL_MAIN + 'mangas/genre/reflexion'] )
    liste.append( ['Romance',URL_MAIN + 'mangas/genre/romance'] )
    liste.append( ['Samourai',URL_MAIN + 'mangas/genre/samourai'] )
    liste.append( ['School Life',URL_MAIN + 'mangas/genre/school-life'] )
    liste.append( ['Science Fiction',URL_MAIN + 'mangas/genre/science-fiction'] )
    liste.append( ['Seinen',URL_MAIN + 'mangas/genre/seinen'] )
    liste.append( ['Shojo',URL_MAIN + 'mangas/genre/shojo'] )
    liste.append( ['Shonen',URL_MAIN + 'mangas/genre/shonen'] )
    liste.append( ['Slapstick',URL_MAIN + 'mangas/genre/slapstick'] )
    liste.append( ['Slice of Life',URL_MAIN + 'mangas/genre/slice-of-life'] )
    liste.append( ['Sport',URL_MAIN + 'mangas/genre/sport'] )
    liste.append( ['Super pouvoir',URL_MAIN + 'mangas/genre/super-pouvoir'] )
    liste.append( ['Surnature',URL_MAIN + 'mangas/genre/surnature'] )
    liste.append( ['Surnaturel',URL_MAIN + 'mangas/genre/surnaturel'] )
    liste.append( ['Suspense',URL_MAIN + 'mangas/genre/suspense'] )
    liste.append( ['Thriller',URL_MAIN + 'mangas/genre/thriller'] )
    liste.append( ['Tragédie',URL_MAIN + 'mangas/genre/tragedie'] )
    liste.append( ['Vampire',URL_MAIN + 'mangas/genre/vampire'] )
    liste.append( ['Vengeance',URL_MAIN + 'mangas/genre/vengeance'] )
    liste.append( ['Vie de tous les jours',URL_MAIN + 'mangas/genre/vie-de-tous-les-jours'] )
    liste.append( ['Western',URL_MAIN + 'mangas/genre/western'] )
    liste.append( ['Yuri',URL_MAIN + 'mangas/genre/yuri'] )
	
    for sTitle,sUrl in liste:
	
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showPays():
    oGui = cGui()
    
    liste = []
    liste.append( ['Algérien',URL_MAIN + 'films/origine/algerien'] )
    liste.append( ['Allemand',URL_MAIN + 'films/origine/allemand'] )
    liste.append( ['Américain',URL_MAIN + 'films/origine/americain'] )
    liste.append( ['Belge',URL_MAIN + 'films/origine/belge'] )
    liste.append( ['Britanique',URL_MAIN + 'films/origine/britannique'] )
    liste.append( ['Canadien',URL_MAIN + 'films/origine/canadien'] )
    liste.append( ['Espagnol',URL_MAIN + 'films/origine/espagnol'] )
    liste.append( ['Francais',URL_MAIN + 'films/origine/francais'] )
    liste.append( ['Italien',URL_MAIN + 'films/origine/italien'] )
    liste.append( ['Japonnais',URL_MAIN + 'films/origine/japonnais'] )
    liste.append( ['Marocains',URL_MAIN + 'films/origine/marocains'] )
    liste.append( ['Néerlandais',URL_MAIN + 'films/origine/neerlandais'] )
    liste.append( ['Norvegien',URL_MAIN + 'films/origine/norvegien'] )
    liste.append( ['Russe',URL_MAIN + 'films/origine/russe'] )
    
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
    
    oRequest = cRequestHandler(URL_MAIN + 'search')
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

    if '/annee/' in sUrl:
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
