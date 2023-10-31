# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re

from resources.lib.comaddon import dialog, addon, isMatrix, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil



SITE_IDENTIFIER = 'sitedarkibox'
SITE_NAME = '[COLOR dodgerblue]Compte DarkiBox[/COLOR]'
SITE_DESC = 'Fichiers sur compte DarkiBox'
NB_FILES = 100
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
API_URL_FILE = 'api/file/list?per_page=100'
API_URL_FOLDER = 'api/folder/list?files=0'

URL_MOVIE = (API_URL_FILE, 'showMedias')

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers = {'User-Agent': UA}

'''
        "sitedarkibox": {
            "label": "darkiBox",
            "active": "True",
            "url": "https://darkibox.com/"
        },
'''

def load():
    oGui = cGui()

    # Compte obligatoire
    if not cPremiumHandler('darkibox').getToken():
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Nécessite un compte DarkiBox' + '[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', '//')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addon().VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
        return

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE[0] + '&fld_id=0')
    oGui.addDir(SITE_IDENTIFIER, URL_MOVIE[1], 'Mes vidéos', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE[0] + '&fld_id=0')
    oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def opensetting():
    addon().openSettings()


def showSearch():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sPath = oInputParameterHandler.getValue('siteUrl')
    sType = oInputParameterHandler.getValue('sMovieTitle')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrlSearch = API_URL_FILE + '&title=' + sSearchText
        if sType:
            sUrlSearch += '&cat=' + sType

        if sType == 'film':
            showMedias(sUrlSearch)
        elif sType == 'serie':
            searchSeries(sPath, sSearchText)
        else:
            showFile(sPath, sUrlSearch)


def showFile(sPath='', sSearch=''):
    oGui = cGui()
    oUtil = cUtil()
    if sPath:
        fldId = int(sPath)
    else:
        fldId = 0
    if sSearch:
        siteUrl = sSearch
        if fldId == 0:
            fldId = -1
    else:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        if 'fld_id' in siteUrl:
            fldId = int(re.search('&fld_id=(\d+)', siteUrl).group(1))

    # token
    oPremiumHandler = cPremiumHandler('darkibox')
    sToken = oPremiumHandler.getToken()

    
    # pagination
    numPage = 1
    if '&page=' in siteUrl:
        numPage = int(re.search('&page=(\d+)', siteUrl).group(1))


    # menu de recherche
    if not sSearch and numPage == 1 :
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', fldId)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOutputParameterHandler)
        
        # les dossiers en premier, sur la première page seulement
        apiUrl = URL_MAIN + API_URL_FOLDER + '&key=%s' % sToken
        apiUrl += '&fld_id=%d' % fldId
    
        oRequestHandler = cRequestHandler(apiUrl)
        sHtmlContent = oRequestHandler.request()
        content = json.loads(sHtmlContent)
        if content['status'] != 200:
            dialog().VSinfo(content['msg'])
            oGui.setEndOfDirectory()
            return
        
        content = content['result']
        if not content:
            oGui.setEndOfDirectory()
            return
    
        if 'folders' in content:
            folders = sorted(content['folders'], key=lambda f: f['name'].upper())
            for folder in folders:
                sTitle = folder['name']
                folderdId = folder['fld_id']
                if not isMatrix():
                    sTitle = sTitle.encode('utf-8')
                    
                sTitle = oUtil.unescape(sTitle)
                sUrl = API_URL_FILE + '&fld_id=%d' % folderdId
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addDir(SITE_IDENTIFIER, 'showFile', sTitle, 'genres.png', oOutputParameterHandler)


    # les fichiers
    if sSearch:
        sUrl = sSearch
    else:
        sUrl = API_URL_FILE

    if fldId >=0:
        sUrl += '&fld_id=%d' % fldId
    sUrl = sUrl + '&page=%d' % numPage
    apiUrl = URL_MAIN + sUrl + '&key=%s' % sToken
    
    oRequestHandler = cRequestHandler(apiUrl)
    sHtmlContent = oRequestHandler.request()
    content = json.loads(sHtmlContent)
    if content['status'] != 200:
        dialog().VSinfo(content['msg'])
        oGui.setEndOfDirectory()
        return
    
    content = content['result']
    if not content:
        oGui.setEndOfDirectory()
        return

    nbFile = 0
    oHosterGui = cHosterGui()
    oHoster = oHosterGui.checkHoster('darkibox')

    for file in content['files']:
        sTitle = file['title']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')
            
        sTitle = oUtil.unescape(sTitle)

        # nécessite un débrideur
        sDisplayTitle = sTitle
        # if not file['canplay']:
        #     sDisplayTitle += '[COLOR violet] *[/COLOR]' 

        sHosterUrl = URL_MAIN + file['file_code']

        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sTitle)
        oHosterGui.showHoster(oGui, oHoster, sHosterUrl, file['thumbnail'])

        nbFile += 1

    # Next >>>
    if not sSearch and nbFile == NB_FILES:
        numPage += 1
        sUrl = API_URL_FILE
        sUrl += '&fld_id=%d' % fldId
        sUrl += '&page=%d' % numPage

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', 'Suite')
        oGui.addNext(SITE_IDENTIFIER, 'showFile', 'Page %d' % numPage, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMedias(sSearch = ''):

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    fldId = None
    if '&cat=' in siteUrl:
        sCat = re.search('&cat=(.+?)(&|$)', siteUrl).group(1)
    else:
        sCat = ''
    
    if sSearch:
        sSiteUrl = sSearch
        sCat = sMovieTitle
    else:
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')
        fldId = int(re.search('&fld_id=(\d+)', siteUrl).group(1))

    sFolderCat = sCat
    if sMovieTitle and not sCat:
        if 'FILM' in sMovieTitle or 'MOVIE' in sMovieTitle or 'DISNEY' in sMovieTitle or '3D' in sMovieTitle or '4K' in sMovieTitle or 'DOCUMENTAIRE' in sMovieTitle or 'DOCS' in sMovieTitle:
            sFolderCat = 'film'
        elif 'SERIE' in sMovieTitle or 'SÉRIE' in sMovieTitle or 'TVSHOW' in sMovieTitle:
            sFolderCat = 'serie'
        elif 'ANIMES' in sMovieTitle or 'ANIMÉS' in sMovieTitle or 'MANGA' in sMovieTitle or 'JAPAN' in sMovieTitle:
            sFolderCat = 'anime'
    isMovie = sFolderCat == 'film'
    isTvShow = sFolderCat == 'serie'
    isAnime = sFolderCat == 'anime'


    nbFile = 0
    numPage = 1
    if '&page=' in siteUrl:
        numPage = int(re.search('&page=(\d+)', siteUrl).group(1))

    oPremiumHandler = cPremiumHandler('darkibox')
    sToken = oPremiumHandler.getToken()

    # menu de recherche
    if not sSearch and numPage == 1 :
        if isMovie:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE[0])
            oOutputParameterHandler.addParameter('sMovieTitle', 'film')
            oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher (Films)', 'search.png', oOutputParameterHandler)

        if isTvShow:
            if 'sSeason' not in siteUrl:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', fldId)
                oOutputParameterHandler.addParameter('sMovieTitle', 'serie')
                oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher (Séries)', 'search.png', oOutputParameterHandler)

    
        # parcourir un dossier virtuel, séparateur ':'
        searchFolder = ''
        if sSiteUrl[-1:] == ':':
            idxFolder = sSiteUrl.rindex('/')
            searchFolder = sSiteUrl[idxFolder+1:-1]
            sSiteUrl = sSiteUrl[:idxFolder]
    
        apiUrl = URL_MAIN + API_URL_FOLDER + '&key=%s' % sToken
        if fldId:
            apiUrl += '&fld_id=%d' % fldId
    
        oRequestHandler = cRequestHandler(apiUrl)
        sHtmlContent = oRequestHandler.request()
        content = json.loads(sHtmlContent)
        if content['status'] != 200:
            dialog().VSinfo(content['msg'])
            oGui.setEndOfDirectory()
            return
    
        
        content = content['result']
        if not content:
            oGui.setEndOfDirectory()
            return
    
        if isTvShow or isAnime:
            nbFile = showSeries(oGui, content, searchFolder, numPage)
        # ajout des dossiers en premier, sur la première page seulement
        if not isTvShow and not isAnime and not sSearch and numPage == 1 and 'folders' in content:
            addFolders(oGui, content, searchFolder)

    # les fichiers
    if sSearch:
        sUrl = sSearch
    else:
        sUrl = API_URL_FILE
    if fldId:
        sUrl += '&fld_id=%d' % fldId
    if isMovie: 
        sUrl += '&page=%d' % numPage
    apiUrl = URL_MAIN + sUrl + '&key=%s' % sToken
    
    oRequestHandler = cRequestHandler(apiUrl)
    sHtmlContent = oRequestHandler.request()
    content = json.loads(sHtmlContent)
    if content['status'] != 200:
        dialog().VSinfo(content['msg'])
        oGui.setEndOfDirectory()
        return
    
    content = content['result']
    if not content:
        oGui.setEndOfDirectory()
        return

    if isTvShow or isAnime:
        sSeason = False
        if 'sSeason' in sSiteUrl:
            sSeason = sSiteUrl.split('sSeason=')[1]
        
        if 'files' in content and len(content['files'])>0 :
            nbFile = showEpisodes(oGui, sMovieTitle, content, sSiteUrl, sSeason)
        # else:
        #     nbFile = showSeries(oGui, content, searchFolder, numPage)
    elif isMovie:
        nbFile = showMovies(oGui, content)

    # Lien Suivant >>
    if not sSearch and nbFile == NB_FILES:
        numPage += 1
        sUrl = API_URL_FILE
        if fldId:
            sUrl += '&fld_id=%d' % fldId
        sUrl = sUrl + '&page=%d' % numPage
        sUrl = sUrl + '&cat=%s' % sCat

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', 'Suite')
        oGui.addNext(SITE_IDENTIFIER, 'showMedias', 'Page %d' % numPage, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def addFolders(oGui, content, searchFolder = None):
    oUtil = cUtil()

    # dossiers trier par ordre alpha
    folders = sorted(content['folders'], key=lambda f: f['name'].upper())

    fldId = ''

    # Sous-dossiers virtuels identifiés par les deux-points
    subFolders = set()
    oOutputParameterHandler = cOutputParameterHandler()

    for folder in folders:

        sTitle = folder['name']
        fldId = folder['fld_id']
        sTitle = oUtil.unescape(sTitle)

        if searchFolder and not sTitle.startswith(searchFolder):
            continue

        isSubFolder = False
        if sTitle.startswith('REP_') or sTitle.startswith('00_'):
            isSubFolder = True

        if isSubFolder and ':' in sTitle:
            subName, subFolder = sTitle.split(':')
            # if folderPath.endswith(subName):
            #     sTitle = subFolder.strip()
            # else:
            if searchFolder:
                if subName == searchFolder:
                    sTitle = subFolder
            else:
                if subName in subFolders:
                    continue
                subFolders.add(subName)
                sTitle = subName
# TODO                sFoldername = sFoldername.replace(subFolder, '')

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
            sCat = 'serie'
            sThumb = 'series.png'
        elif 'DOCUMENTAIRE' in sTitle.upper() or 'DOCS' in sTitle.upper():
            sCat = 'film'
            sThumb = 'doc.png'
        elif 'SPECTACLE' in sTitle.upper():
            sCat = 'film'
            sThumb = 'star.png'
        elif 'CONCERT' in sTitle.upper():
            sCat = 'film'
            sThumb = 'music.png'
        elif 'SPORT' in sTitle.upper():
            sCat = 'film'
            sThumb = 'sport.png'
        elif 'FILM' in sTitle.upper() or 'MOVIE' in sTitle.upper():
            sCat = 'film'
            sThumb = 'films.png'
        elif 'ANIMES' in sTitle.upper() or 'ANIMÉS' in sTitle.upper() or 'MANGA' in sTitle.upper() or 'JAPAN' in sTitle.upper():
            sCat = 'anime'
            sThumb = 'animes.png'
        else:
            sCat = None
            sThumb = 'genres.png'
        
#        sUrl = sFoldername
        sUrl = API_URL_FILE + '&fld_id=%d' % fldId
        if sCat:
            sUrl += '&cat=%s' % sCat
        

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMedias', sTitle, sThumb, oOutputParameterHandler)


def showMovies(oGui, content):
    oUtil = cUtil()
    nbFile = 0
    
    # ajout des fichiers
    for file in content['files']:
        sTitle = file['title']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')

        sTitle = oUtil.unescape(sTitle)
        sHosterUrl = URL_MAIN + file['file_code']

        if sTitle[-4] == '.':
            if sTitle[-4:] not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]
    
        # enlever les séries
        # sa, ep = searchEpisode(sTitle)
        # if sa or ep:
        #     return
    
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
       
        nbFile += 1
        
        sDisplayTitle = sMovieTitle
        if sRes:
            sDisplayTitle += ' [%s]' % sRes
        if sLang:
            sDisplayTitle += ' (%s)' % sLang

        # nécessite un débrideur
        # if not file['canplay']:
        #     sDisplayTitle += '[COLOR violet] *[/COLOR]' 
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sRes', sRes)
        oOutputParameterHandler.addParameter('sLang', sLang)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', file['thumbnail'], '', oOutputParameterHandler)

    return nbFile

def showSeries(oGui, content, searchFolder, numPage):
    oUtil = cUtil()

    # dossiers trier par ordre alpha
    folders = content['folders']
    if len(folders) == 0: return 0
     
    folders = sorted(folders, key=lambda f: f['name'].upper())

    numSeries = 0
    nbSeries = 0
    offset = (numPage-1) * NB_FILES

    # Sous-dossiers virtuels identifiés par les deux-points
    subFolders = set()
    oOutputParameterHandler = cOutputParameterHandler()

    for folder in folders:
        
        fldId = folder['fld_id']
        sTitle = folder['name']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')
        sTitle = oUtil.unescape(sTitle)
        
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
# TODO                    sFoldername = sFoldername.replace(subFolder, '')

        if sTitle.startswith('REP_'):
            sTitle=sTitle.replace('REP_', '')
        if sTitle.startswith('00_'):
            sTitle=sTitle.replace('00_', '')

        pos = len(sTitle)
        sRes, pos = getReso(sTitle, pos)
        sYear, pos = getYear(sTitle, pos)
        sTmdbId, pos = getIdTMDB(sTitle, pos)
        sTitle = sTitle[:pos]

        sUrl = API_URL_FILE + '&fld_id=%d' % fldId
        sUrl += '&cat=serie'
        sUrl += '&page=%d' % 0
        
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sRes', sRes)
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
                sMovieTitle = sTitle
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
            # elif sTitle.upper() == 'ANIMES' or sTitle.upper() == 'ANIMÉS' or 'MANGA' in sTitle.upper() or 'JAPAN' in sTitle.upper():
            #     oGui.addAnime(SITE_IDENTIFIER, 'showMedias', sTitle, '', '', '', oOutputParameterHandler)
            else:
                sMovieTitle = sTitle
                if sRes:
                    sMovieTitle += '[' + sRes + ']'
                oGui.addTV(SITE_IDENTIFIER, 'showMedias', sMovieTitle, '', '', '', oOutputParameterHandler)

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
            sTitle = file['title']
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
        sFileName = file['title']
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
        
        # nécessite un débrideur
        # if not file['canplay']:
        #     sDisplayTitle += '[COLOR violet] *[/COLOR]' 

        sHosterUrl = URL_MAIN + file['file_code']
        
        nbFile += 1
        oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'tv.png', file['thumbnail'], '', oOutputParameterHandler)
        
    return nbFile

    
# Recherche saisons et episodes
def searchEpisode(sTitle):
    sa = ep =''
    m = re.search('(^S| S|\.S|_S|\[S|saison|\s+|\.)(\s?|\.)(\d+)( *- *| *_ *|\s?|\.)(E|Ep|x|\wpisode|Épisode)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
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
            m = re.search('( S|\.S|_S|\[S|saison)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
            if m:
                sa = m.group(3)
                if int(sa) > 100:
                    sa = ''

    return sa, ep

# recherche d'une serie par son nom en parcourant tous les dossiers
def searchSeries(fldId, searchName):

    oGui = cGui()
    sToken = cPremiumHandler('darkibox').getToken()
    apiUrl = URL_MAIN + API_URL_FOLDER + '&key=%s' % sToken + '&fld_id=' + fldId
    
    # recherches des dossiers "series" à la racine
    oRequestHandler = cRequestHandler(apiUrl)
    sHtmlContent = oRequestHandler.request()
    content = json.loads(sHtmlContent)
    if content['status'] != 200:
        dialog().VSinfo(content['msg'])
        oGui.setEndOfDirectory()
        return

    content = content['result']
    if not content:
        oGui.setEndOfDirectory()
        return

    showSeries(oGui, content, searchName, 0)
    oGui.setEndOfDirectory()


                
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    oHoster = cHosterGui().checkHoster('darkibox')
    if oHoster:
        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
    oGui.setEndOfDirectory()


def getYear(sMovieTitle, pos):

    # d'abord entre parenthèse
    sPattern = ['\(([0-9]{4})\)']
    y, pos = _getTag(sMovieTitle, sPattern, pos)
    if y:
        return y, pos
    
    # sinon sans les parenthèses
    sPattern = ['[^\w]([0-9]{4})[^\w]']
    return _getTag(sMovieTitle, sPattern, pos)


def getLang(sMovieTitle, pos):
    sPattern = ['VFI', 'VFF', 'VFQ', 'SUBFRENCH', 'TRUEFRENCH', '.(FRENCH)', 'VF', 'VOSTFR', '[^\w](VOST)[^\w]', '[^\w](VO)[^\w]', 'QC', '[^\w](MULTI)[^\w]', 'FASTSUB']
    return _getTag(sMovieTitle, sPattern, pos)


def getReso(sMovieTitle, pos):
    
    sPattern = ['RES-(.+?)-RES']
    sRes, pos = _getTag(sMovieTitle, sPattern, pos)
    if not sRes:
        sPattern = ['HDCAM', '[^\w](CAM)[^\w]', '[^\w](R5)[^\w]', '.(3D)', '.(DVDSCR)', '.(TVRIP)', '.(FHD)', '.(HDLIGHT)', '.(4K)', '.(UHD)', '\d{3,4}P', '.(HDRIP)', '.(BDRIP)', '.(BRRIP)', '.(DVDRIP)', '.(HDTV)', '.(BLURAY)', '.(WEB-DL)', '.(WEBDL)', '.(WEBRIP)', '[^\w](WEB)[^\w]', '.(DVDRIP)']
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
            if p<pos and p > 3:
                pos = p
            return ret.upper(), pos
    return False, pos
