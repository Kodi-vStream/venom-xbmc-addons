#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib
import urllib2


SITE_IDENTIFIER = 'filmenstreaminghd_com'
SITE_NAME = 'FilmEnStreamingHD'
SITE_DESC = 'Films, Séries & Animés en streaming'

URL_MAIN = 'http://www.filmenstreaminghd.com/'

MOVIE_MOVIE = (URL_MAIN + 'films', 'showMovies')
MOVIE_HD = (URL_MAIN + '1080p-films', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films-populaires', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_QLT = (True, 'showQlt')

SERIE_SERIES = (URL_MAIN + 'series-tv', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_ANNEES = (URL_MAIN + 'series-tv', 'showAnnees')

ANIM_ANIMS = (URL_MAIN +'animes', 'showMovies')
ANIM_GENRES = (True, 'showAnimeGenres')
ANIM_THEMES = (True, 'showAnimeThemes')
ANIM_ANNEES = (URL_MAIN + 'animes', 'showAnnees')

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'films_hd.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus Vus)', 'films_views.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_QLT[1], 'Films (Qualités)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_THEMES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_THEMES[1], 'Animés (Thèmes)', 'animes_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animés (Par Années)', 'animes.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(str(sSearchText))
        oGui.setEndOfDirectory()
        return

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN+ 'action'] )
    liste.append( ['Animation',URL_MAIN + 'animation'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure'] )
    liste.append( ['Biographie',URL_MAIN + 'biographie'] )
    liste.append( ['Comédie',URL_MAIN + 'comedie'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'comedie-dramatique'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'drame'] )
    liste.append( ['Épouvante Horreur',URL_MAIN + 'epouvante-horreur'] )
    liste.append( ['Familial',URL_MAIN + 'familial'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique'] )
    liste.append( ['Histoire',URL_MAIN + 'histoire'] )
    liste.append( ['Musical',URL_MAIN + 'musical'] )
    liste.append( ['Mystère',URL_MAIN + 'mystere'] )
    liste.append( ['Policier',URL_MAIN + 'policier-crime'] )
    liste.append( ['Romance',URL_MAIN + 'romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller'] )
    liste.append( ['Western',URL_MAIN + 'western'] )
    liste.append( ['Top IMDB',URL_MAIN + 'top-imdb'] )
    liste.append( ['IMDB 7 Plus',URL_MAIN + 'imdb-7-plus'] )
    
    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'action-series'] )    
    liste.append( ['Action-Aventure',URL_MAIN + 'action-adventure-series'] )
    liste.append( ['Animation',URL_MAIN + 'animation-series'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure-series'] )
    liste.append( ['Biographie',URL_MAIN + 'biographie-series'] )    
    liste.append( ['Comédie',URL_MAIN + 'comedie-series'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'comedie-dramatique-series'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire-series'] )
    liste.append( ['Drame',URL_MAIN + 'drame-series'] )
    liste.append( ['Épouvante Horreur',URL_MAIN + 'epouvante-horreur-series'] )
    liste.append( ['Familial',URL_MAIN + 'familial-series'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique-series'] )
    liste.append( ['Histoire',URL_MAIN + 'histoire-series'] )
    liste.append( ['Musical',URL_MAIN + 'musical-series'] )
    liste.append( ['Mystère',URL_MAIN + 'mystere-series'] )
    liste.append( ['Policier',URL_MAIN + 'policier-crime-series'] )
    liste.append( ['Romance',URL_MAIN + 'romance-series'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction-series'] )
    liste.append( ['Science Fiction - fantastique',URL_MAIN + 'science-Fiction-fantastique-series'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller-series'] )
    liste.append( ['Western',URL_MAIN + 'western-series'] )
    
    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimeGenres():
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'action-animes'] )    
    liste.append( ['Animation',URL_MAIN + 'animation-animes'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure-animes'] )
    liste.append( ['Biographie',URL_MAIN + 'biographie-animes'] )    
    liste.append( ['Comédie',URL_MAIN + 'comedie-animes'] )
    liste.append( ['Drame',URL_MAIN + 'drame-animes'] )
    liste.append( ['Épouvante Horreur',URL_MAIN + 'epouvante-horreur-animes'] )
    liste.append( ['Familial',URL_MAIN + 'familial-animes'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique-animes'] )
    liste.append( ['Histoire',URL_MAIN + 'histoire-animes'] )
    liste.append( ['Musical',URL_MAIN + 'musical-animes'] )
    liste.append( ['Mystère',URL_MAIN + 'mystere-animes'] )
    liste.append( ['Policier',URL_MAIN + 'policier-crime-animes'] )
    liste.append( ['Romance',URL_MAIN + 'romance-animes'] )
    liste.append( ['School Life',URL_MAIN + 'school-life-animes'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction-animes'] )
    liste.append( ['Seinen',URL_MAIN + 'seinen-animes'] )
    liste.append( ['Shôjo',URL_MAIN + 'shojo-animes'] )
    liste.append( ['Shônen',URL_MAIN + 'shonen-animes'] )
    liste.append( ['Slice of Life',URL_MAIN + 'slice-of-life-animes'] )
    liste.append( ['Surnaturel',URL_MAIN + 'surnaturel-animes'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller-animes'] )
    liste.append( ['Western',URL_MAIN + 'western-animes'] )
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'animes_genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def showAnimeThemes():
    oGui = cGui()
    
    liste = []
    liste.append( ['Aliens',URL_MAIN + 'aliens-animes-themes'] )    
    liste.append( ['Amitié',URL_MAIN + 'amitie-animes-themes'] )
    liste.append( ['Apprentissage',URL_MAIN + 'apprentissage-animes-themes'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux-animes-themes'] )    
    liste.append( ['Assassinat',URL_MAIN + 'assassinat-animes-themes'] )
    liste.append( ['Autre monde',URL_MAIN + 'autre-monde-animes-themes'] )
    liste.append( ['Baseball',URL_MAIN + 'baseball-animes-themes'] )
    liste.append( ['Combats',URL_MAIN + 'combats-animes-themes'] )
    liste.append( ['Démons',URL_MAIN + 'demons-animes-themes'] )
    liste.append( ['Détective',URL_MAIN + 'detective-animes-themes'] )
    liste.append( ['École',URL_MAIN + 'ecole-animes-themes'] )
    liste.append( ['Espace',URL_MAIN + 'espace-animes-themes'] )
    liste.append( ['Football',URL_MAIN + 'football-animes-themes'] )
    liste.append( ['Guerre',URL_MAIN + 'guerre-animes-themes'] )
    liste.append( ['Harem',URL_MAIN + 'harem-animes-themes'] )
    liste.append( ['Idols',URL_MAIN + 'idols-animes-themes'] )
    liste.append( ['Mafia',URL_MAIN + 'mafia-animes-themes'] )
    liste.append( ['Magie',URL_MAIN + 'magie-animes-themes'] )
    liste.append( ['Mechas',URL_MAIN + 'mechas-animes-themes'] )
    liste.append( ['Militaire',URL_MAIN + 'militaire-animes-themes'] )
    liste.append( ['Mode',URL_MAIN + 'mode-animes-themes'] )
    liste.append( ['Monstres',URL_MAIN + 'monstres-animes-themes'] )
    liste.append( ['Musique',URL_MAIN + 'musique-animes-themes'] )
    liste.append( ['Ninjas',URL_MAIN + 'ninjas-animes-themes'] )
    liste.append( ['Nourriture',URL_MAIN + 'nourriture-animes-themes'] )
    liste.append( ['One Piece',URL_MAIN + 'one-piece-animes-themes'] )
    liste.append( ['Parodie',URL_MAIN + 'parodie-animes-themes'] )
    liste.append( ['Politique',URL_MAIN + 'politique-animes-themes'] )
    liste.append( ['Quotidien',URL_MAIN + 'quotidien-animes-themes'] )
    liste.append( ['Robots',URL_MAIN + 'robots-animes-themes'] )
    liste.append( ['Sorcière',URL_MAIN + 'sorciere-animes-themes'] )
    liste.append( ['Sport',URL_MAIN + 'sport-animes-themes'] )
    liste.append( ['Super Pouvoirs',URL_MAIN + 'super-pouvoirs-animes-themes'] )
    liste.append( ['Super-héros',URL_MAIN + 'super-heros-animes-themes'] )
    liste.append( ['Vampires',URL_MAIN + 'vampires-animes-themes'] )
    liste.append( ['Vengeance',URL_MAIN + 'vengeance-animes-themes'] )
    liste.append( ['Voyage temporel',URL_MAIN + 'voyage-temporel-animes-themes'] )
    liste.append( ['Youkai',URL_MAIN + 'youkai-animes-themes'] )
    liste.append( ['Zombies',URL_MAIN + 'zombies-animes-themes'] )
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'animes_genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def showAnnees():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    if 'animes' in sUrl:
        code = '-animes'
    else:
        code = '-series'

    liste = []
    #liste.append( ['2017',URL_MAIN + '2017' + code] )
    liste.append( ['2016',URL_MAIN + '2016' + code] )
    liste.append( ['2015',URL_MAIN + '2015' + code] )
    liste.append( ['2014',URL_MAIN + '2014' + code] )
    liste.append( ['2013',URL_MAIN + '2013' + code] )
    liste.append( ['2012',URL_MAIN + '2012' + code] )
    liste.append( ['2011',URL_MAIN + '2011' + code] )
    liste.append( ['2010',URL_MAIN + '2010' + code] )
    liste.append( ['2009',URL_MAIN + '2009' + code] )
    liste.append( ['2008',URL_MAIN + '2008' + code] )
    liste.append( ['2007',URL_MAIN + '2007' + code] )
    liste.append( ['2006',URL_MAIN + '2006' + code] )
    liste.append( ['2005',URL_MAIN + '2005' + code] )
    liste.append( ['2004',URL_MAIN + '2004' + code] )
    liste.append( ['2003',URL_MAIN + '2003' + code] )    
    liste.append( ['2002',URL_MAIN + '2002' + code] )
    liste.append( ['2001',URL_MAIN + '2001' + code] )
    liste.append( ['2000',URL_MAIN + '2000' + code] )
    liste.append( ['1900-1999',URL_MAIN + '1900-1999' + code] )
               
    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showQlt():
    oGui = cGui()

    liste = []
    liste.append( ['1080p',URL_MAIN + '1080p-films'] )
    liste.append( ['720p',URL_MAIN + '720p-films'] )
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
    
        oRequestHandler = cRequestHandler(URL_MAIN + 'recherche/')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('query', sSearch)
        oRequestHandler.addParameters('submit=Valider', 'Valider')
        sHtmlContent = oRequestHandler.request()

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="film-k.+?<a href="([^<"]+)".+?<div class="kalite">([^<"]+).+?<img src="([^<"]+).+?<div class="baslik">([^<"]+).+?<div class="aciklama">([^<"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[3]
            if aEntry[1]:
                sTitle = sTitle + ' [' + aEntry[1]  + '] '
                
            sCom = aEntry[4].decode("utf-8")
            sCom = cUtil().unescape(sCom).encode("utf-8")
            sCom = cUtil().removeHtmlTags(sCom)
            sUrl2 = URL_MAIN  + aEntry[0]
            sThumb = URL_MAIN + aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            if 'series-tv' in sUrl or 'saison' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle,'series.png', sThumb, sCom, oOutputParameterHandler)
            elif 'animes' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle,'animes.png', sThumb, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, 'films.png', sThumb, sCom, oOutputParameterHandler)           
    
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            sUrl = re.sub('\/page-[0-9]','',sUrl)
            oOutputParameterHandler.addParameter('siteUrl', sUrl+'/'+sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<span class="pikon" style="background-image: url\(/sistem/inc/part_ikon/(.+?).png\);"></span>(.+?)<span|class="partsec.+?" id="([^"]+?)".+?</i>([^<]+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' + aEntry[3] +' [/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sPid', aEntry[2])
            
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER,  '[COLOR red]'+aEntry[0]+' - '+aEntry[1]+'[/COLOR]', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    
    sPattern = '<a class="sonraki-sayfa" href="(?:/.+?/|)(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<a class="partsec" id="([^"]+)".+?</span>([^<]+)<span'
    #sPattern='<div id="burayaclass".+?onclick="getirframe\(\'(.+?)\',\'(.+?)\'\)".+?<div class="col-md-4.+?<p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' + aEntry[1] +' [/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',  sUrl)
            oOutputParameterHandler.addParameter('sPid',  aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sPid = oInputParameterHandler.getValue('sPid')

    postdata = 'pid=' + sPid
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('pid', sPid)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<ifram[^<>]+? src=[\'"]([^\'"]+?)[\'"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl =  str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
