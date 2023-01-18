# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re
import xbmc
import xbmcgui

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError
    from urllib.parse import urlencode

from resources.lib.comaddon import progress, VSlog, dialog, addon, isMatrix, siteManager
from resources.lib.config import GestionCookie
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler, MPencode
from resources.lib.parser import cParser
from resources.lib.util import Quote



SITE_IDENTIFIER = 'siteuptobox'
SITE_NAME = '[COLOR dodgerblue]Compte UpToBox[/COLOR]'
SITE_DESC = 'Fichiers sur compte UpToBox'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
NB_FILES = 100
BURL = URL_MAIN + '?op=my_files'
API_URL = 'https://uptobox.com/api/user/files?token=none&orderBy=file_date_inserted&dir=desc'
URL_MOVIE = ('&path=//', 'showMedias')

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers = {'User-Agent': UA}


def load():
    oGui = cGui()
    addons = addon()

    # Même avec un token, on verifies les identifiants
    if (addons.getSetting('hoster_uptobox_username') == '') or (addons.getSetting('hoster_uptobox_password') == '') or not cPremiumHandler('uptobox').getToken():
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Nécessite un Compte Uptobox Premium ou Gratuit' + '[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', '//')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addon().VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
        return

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, URL_MOVIE[1], 'Mes vidéos', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def opensetting():
    addon().openSettings()


def showSearch(path = '//'):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sPath = oInputParameterHandler.getValue('siteUrl')
    sType = oInputParameterHandler.getValue('sMovieTitle')

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrlSearch = ''
        if sType:
            sUrlSearch += '&type=' + sType
        if sPath:
            sUrlSearch += '&path=' + sPath
        else:
            sUrlSearch += '&path=//'
        sUrlSearch += '&searchField=file_name&search=' + sSearchText
        
        if sType == 'serie':
            searchSeries(sSearchText)
        else:
            showMedias(sUrlSearch, sType)


def showFile(sSearch=''):

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    offset = 0
    limit = NB_FILES
    if 'offset=' not in sUrl:
        sUrl = '&offset=0' + sUrl
    else:
        offset = int(re.search('&offset=(\d+)', sUrl).group(1))

    if 'limit=' not in sUrl:
        sUrl = '&limit=%d' % NB_FILES + sUrl
    else:
        limit = int(re.search('&limit=(\d+)', sUrl).group(1))

    # Page courante
    numPage = offset//limit

    oPremiumHandler = cPremiumHandler('uptobox')
    sToken = oPremiumHandler.getToken()

    oRequestHandler = cRequestHandler(API_URL.replace('none', sToken) + sUrl)
    sHtmlContent = oRequestHandler.request()
    content = json.loads(sHtmlContent)
    if ('success' in content and content['success'] == False) or content['statusCode'] != 0:
        dialog().VSinfo(content['data'])
        oGui.setEndOfDirectory()
        return
    
    content = content['data']
    path = content['path'].upper()
    if not content:
        oGui.setEndOfDirectory()
        return

    # menu de recherche
    oOutputParameterHandler = cOutputParameterHandler()
    if path == '//' and not sSearch:
        oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE[0])
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOutputParameterHandler)


    total = len(content)
    sPath = getpath(content)
    
    # les dossiers en premier, sur la première page seulement
    if not sSearch and numPage == 0 and 'folders' in content:
        folders = sorted(content['folders'], key=lambda f: f['fld_name'].upper())
        sFoldername = ''
        for folder in folders:
            sTitle = folder['name']
            sFoldername = folder['fld_name']
            if not isMatrix():
                sTitle = sTitle.encode('utf-8')
                sFoldername = sFoldername.encode('utf-8')
            sUrl = '&path=' + Quote(sFoldername).replace('//', '%2F%2F')
    
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showFile', sTitle, 'genres.png', oOutputParameterHandler)

    # les fichiers
    nbFile = 0
    oHosterGui = cHosterGui()
    oHoster = oHosterGui.getHoster('uptobox')

    for file in content['files']:
        sTitle = file['file_name']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')

        sHosterUrl = URL_MAIN + file['file_code']

        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sTitle)
        oHosterGui.showHoster(oGui, oHoster, sHosterUrl, '')
            
        nbFile += 1

    # Next >>>
    if not sSearch and nbFile == NB_FILES:
        sPath = getpath(content)
        nextPage = numPage + 1
        offset = nextPage * NB_FILES
        siteUrl = '&offset=%d&limit=%d&path=%s' % (offset, limit, sPath) 

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', 'sMovieTitle')
        oGui.addNext(SITE_IDENTIFIER, 'showFile', 'Page %d' % (nextPage+1), oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMedias(sSearch = '', sType = None):

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    if sSearch:
        sSiteUrl = sSearch
    else:
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    
    oPremiumHandler = cPremiumHandler('uptobox')
    sToken = oPremiumHandler.getToken()

    # parcourir un dossier virtuel, séparateur ':'
    searchFolder = ''
    if sSiteUrl[-1:] == ':':
        idxFolder = sSiteUrl.rindex('/')
        searchFolder = sSiteUrl[idxFolder+1:-1]
        sSiteUrl = sSiteUrl[:idxFolder]

    offset = 0
    limit = NB_FILES
    if 'offset=' not in sSiteUrl:
        sSiteUrl = '&offset=0' + sSiteUrl
    else:
        offset = int(re.search('&offset=(\d+)', sSiteUrl).group(1))

    if 'limit=' not in sSiteUrl:
        sSiteUrl = '&limit=%d' % NB_FILES + sSiteUrl
    else:
        limit = int(re.search('&limit=(\d+)', sSiteUrl).group(1))

    # Page courante
    numPage = offset//limit

    oRequestHandler = cRequestHandler(API_URL.replace('none', sToken) + sSiteUrl)
    sHtmlContent = oRequestHandler.request()
    content = json.loads(sHtmlContent)
    
    if ('success' in content and content['success'] == False) or content['statusCode'] != 0:
        dialog().VSinfo(content['data'])
        oGui.setEndOfDirectory()
        return
    
    content = content['data']
    if not content:
        oGui.setEndOfDirectory()
        return

    isMovie = isTvShow = isSeason = False
    path = content['path'].upper()
    if not isMatrix():
        path = path.encode('utf-8')
    isMovie = 'FILM' in path or 'MOVIE' in path or 'DISNEY' in path or '3D' in path or '4K' in path or 'DOCUMENTAIRE' in path or 'DOCS' in path
    isTvShow = 'SERIE' in path or 'SÉRIE' in path or 'TVSHOW' in path
    isAnime = '/ANIMES' in path or '/ANIMÉS' in path or 'MANGA' in path or 'JAPAN' in path

    # Rechercher Film
    if path == '//' and not sSearch:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', path)
        oOutputParameterHandler.addParameter('sMovieTitle', 'film')
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher (Films)', 'search.png', oOutputParameterHandler)

    # Rechercher Séries
    if path == '//' and not sSearch:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', path)
        oOutputParameterHandler.addParameter('sMovieTitle', 'serie')
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher (Séries)', 'search.png', oOutputParameterHandler)

    if sSearch and sType == 'film':
        isMovie = True

    # ajout des dossiers en premier, sur la première page seulement
    if not isTvShow and not isAnime and not sSearch and numPage == 0 and 'folders' in content:
        addFolders(oGui, content, searchFolder)

    nbFile = 0
    if isTvShow or isAnime:
        sSeason = False
        if 'sSeason' in sSiteUrl:
            sSeason = sSiteUrl.split('sSeason=')[1]
        
        if len(content['files'])>0 :
            nbFile = showEpisodes(oGui, sMovieTitle, content, sSiteUrl, sSeason)
        else:
            nbFile = showSeries(oGui, content, searchFolder, numPage)
    elif isMovie:
        nbFile = showMovies(oGui, content, sType)
    else:
        for file in content['files']:
            sTitle = file['file_name']
            sHosterUrl = URL_MAIN + file['file_code']
            showMovie(oGui, sTitle, sHosterUrl, 'film')

    # Lien Suivant >>
    if not sSearch and nbFile == NB_FILES:
        sPath = getpath(content)
        nextPage = numPage + 1
        offset = nextPage * NB_FILES
        siteUrl = '&offset=%d&limit=%d&path=%s' % (offset, limit, sPath) 

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oGui.addNext(SITE_IDENTIFIER, 'showMedias', 'Page %d' % (nextPage+1), oOutputParameterHandler)

    oGui.setEndOfDirectory()


def addFolders(oGui, content, searchFolder = None):

    # dossiers trier par ordre alpha
    folders = sorted(content['folders'], key=lambda f: f['fld_name'].upper())

    sFoldername = ''

    # Sous-dossiers virtuels identifiés par les deux-points
    subFolders = set()
    oOutputParameterHandler = cOutputParameterHandler()

    for folder in folders:

        sTitle = folder['name']
        sFoldername = folder['fld_name']
        folderPath = folder['path']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')
            sFoldername = sFoldername.encode('utf-8')
            folderPath = folderPath.encode('utf-8')

        if searchFolder and not sTitle.startswith(searchFolder):
            continue

        isSubFolder = False
        if sTitle.startswith('REP_') or sTitle.startswith('00_'):
            isSubFolder = True

        if isSubFolder and ':' in sTitle:
            subName, subFolder = sTitle.split(':')
            if folderPath.endswith(subName):
                sTitle = subFolder.strip()
            else:
                if searchFolder:
                    if subName == searchFolder:
                        sTitle = subFolder
                else:
                    if subName in subFolders:
                        continue
                    subFolders.add(subName)
                    sTitle = subName
                    sFoldername = sFoldername.replace(subFolder, '')

        if sTitle.startswith('REP_'):
            sTitle=sTitle.replace('REP_', '')
        if sTitle.startswith('00_'):
            sTitle=sTitle.replace('00_', '')
        
        # format du genre "REP_:"
        if not sTitle:
            return addFolders(oGui, content, subName)           
            
        if sTitle.startswith('RES-') and sTitle.endswith('-RES'):
            sTitle=sTitle.replace('RES-', '[').replace('-RES', ']')

        if 'SERIE' in sTitle.upper() or 'SÉRIE' in sTitle.upper() or 'TVSHOW' in sTitle.upper():
            sThumb = 'series.png'
        elif 'DOCUMENTAIRE' in sTitle.upper() or 'DOCS' in sTitle.upper():
            sThumb = 'doc.png'
        elif 'SPECTACLE' in sTitle.upper():
            sThumb = 'star.png'
        elif 'CONCERT' in sTitle.upper():
            sThumb = 'music.png'
        elif 'SPORT' in sTitle.upper():
            sThumb = 'sport.png'
        elif 'FILM' in sTitle.upper() or 'MOVIE' in sTitle.upper():
            sThumb = 'films.png'
        elif 'ANIMES' in sTitle.upper() or 'ANIMÉS' in sTitle.upper() or 'MANGA' in sTitle.upper() or 'JAPAN' in sTitle.upper():
            sThumb = 'animes.png'
        else:
            sThumb = 'genres.png'
        
        sUrl = '&path=' + Quote(sFoldername).replace('//', '%2F%2F')
        

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMedias', sTitle, sThumb, oOutputParameterHandler)


def showMovies(oGui, content, sType = None):
    
    numFile = 0
    
    # ajout des fichiers
    for file in content['files']:
        sTitle = file['file_name']
        sHosterUrl = URL_MAIN + file['file_code']
        showMovie(oGui, sTitle, sHosterUrl, sType)
        numFile += 1

    return numFile


def showMovie(oGui, sTitle, sHosterUrl, sType = None):
    # seulement les formats vidéo (ou sans extensions)
    if sTitle[-4] == '.':
        if sTitle[-4:] not in '.mkv.avi.mp4.m4v.iso':
            return
        # enlever l'extension
        sTitle = sTitle[:-4]

    # enlever les séries
    if sType == 'film':
        sa, ep = searchEpisode(sTitle)
        if sa or ep:
            return

    if not isMatrix():
        sTitle = sTitle.encode('utf-8')
        
    # recherche des métadonnées
    sMovieTitle = sTitle 
    pos = len(sMovieTitle)
    sYear, pos = getYear(sMovieTitle, pos)
    sRes, pos = getReso(sMovieTitle, pos)
    sTmdbId, pos = getIdTMDB(sMovieTitle, pos)
    sLang, pos = getLang(sMovieTitle, pos)

    sMovieTitle = sMovieTitle[:pos].replace('.', ' ').replace('_', ' ').strip()

    # un peu de nettoyage
    if not 'customer' in sMovieTitle.lower():
        sMovieTitle = re.sub('(?i)' + re.escape('custom'), '', sMovieTitle)
   
    
    sTitle = sMovieTitle
    if sRes:
        sMovieTitle += ' [%s]' % sRes
    if sLang:
        sMovieTitle += ' (%s)' % sLang
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sYear', sYear)
    oOutputParameterHandler.addParameter('sRes', sRes)
    oOutputParameterHandler.addParameter('sLang', sLang)
    oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', '', '', oOutputParameterHandler)


def showSeries(oGui, content, searchFolder, numPage):

    # dossiers trier par ordre alpha
    folders = content['folders']
    if len(folders) == 0: return 0
     
    folders = sorted(folders, key=lambda f: f['fld_name'].upper())

    sMovieTitle = content['currentFolder']['name'] if 'name' in content['currentFolder'] else 'Rechercher'
    if not isMatrix():
        sMovieTitle  = sMovieTitle.encode('utf-8')

    numSeries = 0
    nbSeries = 0
    offset = numPage * NB_FILES

    # Sous-dossiers virtuels identifiés par les deux-points
    subFolders = set()
    oOutputParameterHandler = cOutputParameterHandler()

    for folder in folders:
        
        sTitle = folder['name']
        sFoldername = folder['fld_name']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')
            sFoldername = sFoldername.encode('utf-8')
        
        # if searchFolder and not sTitle.startswith(searchFolder):
        if searchFolder and searchFolder.upper() not in sTitle.upper():
            continue

        if 'REP_' in sTitle:
            addFolders(oGui, content, sTitle.split(':')[0])
            continue
        
        numSeries += 1
        if numSeries <= offset:
            continue

        # dossier
        isSubFolder = False
        if sTitle.startswith('REP_') or sTitle.startswith('00_'):
            isSubFolder = True

        if isSubFolder and ':' in sTitle:
            subName, subFolder = sTitle.split(':')
            if folder['path'].endswith(subName):
                sTitle = subFolder.strip()
            else:
                if searchFolder:
                    if subName == searchFolder:
                        sTitle = subFolder
                else:
                    if subName in subFolders:
                        continue
                    subFolders.add(subName)
                    sTitle = subName
                    sFoldername = sFoldername.replace(subFolder, '')

        if sTitle.startswith('REP_'):
            sTitle=sTitle.replace('REP_', '')
        if sTitle.startswith('00_'):
            sTitle=sTitle.replace('00_', '')

        pos = len(sTitle)
        
        sYear, pos = getYear(sTitle, pos)
        sTmdbId, pos = getIdTMDB(sTitle, pos)
        sTitle = sTitle[:pos]

        sUrl = '&path=' + Quote(sFoldername).replace('//', '%2F%2F')
        
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        
        if isSubFolder:   # dossier
            oGui.addDir(SITE_IDENTIFIER, 'showMedias', sTitle, 'genres.png', oOutputParameterHandler)
        else:           # série
            saison = None
            if 'SAISON' in sTitle.upper() or 'SEASON' in sTitle.upper():
                saison = re.search('(\d+)', sTitle)
                if saison:
                    saison = int(saison.group(1))
            if not saison:
                saison = re.search('S(\d+)', sTitle)
                if saison:
                    saison = int(saison.group(1))
            if saison:
                pos = len(sMovieTitle)
                sYear, pos = getYear(sMovieTitle, pos)
                sTmdbId, pos = getIdTMDB(sMovieTitle, pos)
                sMovieTitle = sMovieTitle[:pos]
                
                sUrl += '&sSeason=%d' % saison
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

                oGui.addSeason(SITE_IDENTIFIER, 'showMedias', sMovieTitle + ' ' + sTitle, '', '', '', oOutputParameterHandler)
            elif sMovieTitle.upper() == 'ANIMES' or sMovieTitle.upper() == 'ANIMÉS' or 'MANGA' in sMovieTitle.upper() or 'JAPAN' in sMovieTitle.upper():
                oGui.addAnime(SITE_IDENTIFIER, 'showMedias', sTitle, '', '', '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showMedias', sTitle, '', '', '', oOutputParameterHandler)

        nbSeries += 1
        if nbSeries == NB_FILES:
            break
            
    return nbSeries


def showEpisodes(oGui, sMovieTitle, content, sSiteUrl, sSeason):

    if not sSeason:
        nbFile = 0
        saisons = set()
        
        # Recherche des saisons
        for file in content['files']:
            nbFile += 1
            sTitle = file['file_name']
            if not isMatrix():
                sTitle = sTitle.encode('utf-8')
                
            # Recherche saisons et episodes
            sa, ep = searchEpisode(sTitle)
            if sa:
                saisons.add(int(sa))
    
        # plusieurs saisons, on les découpe
        if len(saisons) > 0:
            oOutputParameterHandler = cOutputParameterHandler()
            for saison in saisons:
                sUrl = sSiteUrl + '&sSeason=%d' % saison
                sTitle = 'Saison %d ' % saison + sMovieTitle
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addSeason(SITE_IDENTIFIER, 'showMedias', sTitle, '', '', '', oOutputParameterHandler)
            return nbFile
    
    
    pos = len(sMovieTitle)
    sYear, pos = getYear(sMovieTitle, pos)
    sMovieTitle = sMovieTitle[:pos]
    
    # ajout des fichiers
    nbFile = 0
    oOutputParameterHandler = cOutputParameterHandler()
    for file in content['files']:
        sFileName = file['file_name']
        if not isMatrix():
            sFileName = sFileName.encode('utf-8')
            
        # Recherche saisons et episodes
        sa, ep = searchEpisode(sFileName)
        if sSeason:
            if sa:
                if int(sa) != int(sSeason):
                    continue
            else:
                sa = sSeason
        
        if ep:
            sTitle = 'E' + ep + ' ' + sMovieTitle
            if sa:
                sTitle = 'S' + sa + sTitle
        
        pos = len(sFileName)
        sRes, pos = getReso(sFileName, pos)
        sLang, pos = getLang(sFileName, pos)
        
        if not ep:
            sTitle = sFileName[:pos]
            
        sDisplayTitle = sTitle
        if sRes:
            sDisplayTitle += '[%s]' % sRes
        if sLang:
            sDisplayTitle += '(%s)' % sLang
        
        sHosterUrl = URL_MAIN + file['file_code']
        
        nbFile += 1
        oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', '', '', oOutputParameterHandler)
        
    return nbFile

    
# Recherche saisons et episodes
def searchEpisode(sTitle):
    sa = ep =''
    m = re.search('( S|\.S|\[S|saison|\s+|\.)(\s?|\.)(\d+)( *- *|\s?|\.)(E|Ep|x|\wpisode|Épisode)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
    if m:
        sa = m.group(3)
        if int(sa) <100:
            ep = m.group(7)
        else:
            sa = ''
    else:  # Juste l'épisode
        m = re.search('(^|\s|\.)(E|Ep|\wpisode)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
        if m:
            ep = m.group(4)
        else:  # juste la saison
            m = re.search('( S|\.S|\[S|saison)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
            if m:
                sa = m.group(3)
                if int(sa) > 100:
                    sa = ''

    return sa, ep

# recherche d'une serie par son nom en parcourant tous les dossiers
def searchSeries(searchName):

    oGui = cGui()
    sToken = cPremiumHandler('uptobox').getToken()
    sUrl = API_URL.replace('none', sToken) + '&offset=0&limit=20&path='

    # recherches des dossiers "series" à la racine
    oRequestHandler = cRequestHandler(sUrl + '//')
    sHtmlContent = oRequestHandler.request()
    content = json.loads(sHtmlContent)
    content = content['data']
    if content:
        folders = content['folders']
        for folder in folders:
            path = folder['fld_name'].upper()
            if not isMatrix():
                path = path.encode('utf-8')
            isTvShow = 'SERIE' in path or 'SÉRIE' in path or 'TVSHOW' in path
            if isTvShow:
                searchSerie(oGui, sUrl, path, searchName)

    oGui.setEndOfDirectory()
    return


def searchSerie(oGui, sUrl, path, searchName):
    oRequestHandler = cRequestHandler(sUrl + path)
    sHtmlContent = oRequestHandler.request()
    content = json.loads(sHtmlContent)
    content = content['data']
    if content:
        showSeries(oGui, content, searchName, 0)
        folders = content['folders']
        
        # recherche dans les sous-dossiers qui ne sont pas des séries
        for folder in folders:
            subFolderName = folder['name'].upper()
            if subFolderName.startswith('REP_') or subFolderName.startswith('00_'): 
                path = folder['fld_name'].upper()
                searchSerie(oGui, sUrl, path, searchName)

                
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
    oGui.setEndOfDirectory()


def getYear(sMovieTitle, pos):
    sPattern = ['[^\w]([0-9]{4})[^\w]']
    return _getTag(sMovieTitle, sPattern, pos)


def getLang(sMovieTitle, pos):
    sPattern = ['VFI', 'VFF', 'VFQ', 'SUBFRENCH', 'TRUEFRENCH', '.(FRENCH)', 'VF', 'VOSTFR', '[^\w](VOST)[^\w]', '[^\w](VO)[^\w]', 'QC', '[^\w](MULTI)[^\w]', 'FASTSUB']
    return _getTag(sMovieTitle, sPattern, pos)


def getReso(sMovieTitle, pos):
    sPattern = ['HDCAM', '[^\w](CAM)[^\w]', '[^\w](R5)[^\w]', '.(3D)', '.(DVDSCR)', '.(TVRIP)', '.(FHD)', '.(HDLIGHT)', '\d{3,4}P', '.(4K)', '.(UHD)', '.(BDRIP)', '.(BRRIP)', '.(DVDRIP)', '.(HDTV)', '.(BLURAY)', '.(WEB-DL)', '.(WEBRIP)', '[^\w](WEB)[^\w]', '.(DVDRIP)']
    sRes, pos = _getTag(sMovieTitle, sPattern, pos)
    if sRes:
        sRes = sRes.replace('2160P', '4K')
    return sRes, pos


def getIdTMDB(sMovieTitle, pos):
    sPattern = ['TM(\d+)TM']
    return _getTag(sMovieTitle, sPattern, pos)


def _getTag(sMovieTitle, tags, pos):
    for t in tags:
        aResult = re.search(t, sMovieTitle, re.IGNORECASE)
        if aResult:
            l = len(aResult.groups())
            ret = aResult.group(l)
            if not ret and l > 1:
                ret = aResult.group(l-1)
            p = sMovieTitle.index(aResult.group(0))
            if p<pos:
                pos = p
            return ret.upper(), pos
    return False, pos


def getpath(content):
    for x in content:
        if x == 'path':
            sPath = Quote(content[x].encode('utf-8')).replace('//', '%2F%2F')
            return sPath


def AddmyAccount():
    upToMyAccount()


def upToMyAccount():
    addons = addon()

    # on n'utilise pas le token car il se prete, il faut fournir les identifiants pour ajouter à son compte
    if (addons.getSetting('hoster_uptobox_username') == '') and (addons.getSetting('hoster_uptobox_password') == ''):
        return

    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
    sMovieTitle = oInputParameterHandler.getValue('sTitle')

    oPremiumHandler = cPremiumHandler('uptobox')
    sHtmlContent = oPremiumHandler.GetHtml(URL_MAIN)
    cookies = GestionCookie().Readcookie('uptobox')

    aResult = re.search('<form id="fileupload" action="([^"]+)"', sHtmlContent, re.DOTALL)
    if aResult:
        
        upUrl = aResult.group(1).replace('upload?', 'remote?')

        if upUrl.startswith('//'):
            upUrl = 'https:' + upUrl

        fields = {'urls': '["' + sMediaUrl + '"]'}
        mpartdata = list(MPencode(fields))

        if isMatrix():
            mpartdata[1] = mpartdata[1].encode("utf-8")

        req = urllib2.Request(upUrl, mpartdata[1], headers)
        req.add_header('Content-Type', mpartdata[0].replace(',', ';'))
        req.add_header('Cookie', cookies)
        req.add_header('Content-Length', len(mpartdata[1]))

        # pénible ce dialog auth
        xbmc.executebuiltin('Dialog.Close(all,true)')

        try:
            rep = urllib2.urlopen(req)
            xbmcgui.Dialog().notification('Demande envoyée', 'Vous pouvez faire autre chose.', xbmcgui.NOTIFICATION_INFO, 3000, False)
        except UrlError as e:
            xbmcgui.Dialog().notification('Demande rejetée', 'Essayez de nouveau.', xbmcgui.NOTIFICATION_INFO, 3000, False)
            VSlog(str(e))
            return ''

        sHtmlContent = rep.read()
        rep.close()

        sPattern = '{"id":.+?,(?:"size":|"progress":)([0-9]+)'
        aResult = cParser().parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            xbmcgui.Dialog().notification('Uptobox', 'Fichier ajouté - %s' % sMovieTitle, xbmcgui.NOTIFICATION_INFO, 2000, False)
        else:
            # pénible ce dialog auth
            xbmc.executebuiltin('Dialog.Close(all,true)')
            xbmcgui.Dialog().notification('Uptobox', 'Fichier introuvable', xbmcgui.NOTIFICATION_INFO, 2000, False)
    else:
        # pénible ce dialog auth
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmcgui.Dialog().notification('Uptobox', "Impossible d'ajouter le fichier", xbmcgui.NOTIFICATION_ERROR, 2000, False)

