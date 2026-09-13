# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from datetime import datetime
import json
import time

from resources.lib.comaddon import siteManager, addon
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler


SITE_IDENTIFIER = 'rdlive'
SITE_NAME = 'RD Live'
SITE_DESC = 'Sport en direct'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_FLASHSCORE_API = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_flashcore')

SPORT_SPORTS = ('/', 'load')
SPORT_GENRES = (URL_FLASHSCORE_API + 'f_%s_0_1_en_1', 'showGenres')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'sport.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def get_sports_list():
    # Mapping officiel Flashscore sport_name -> sport_id
    flashscore_sports = {
        'Football': '1', 'Tennis': '2', 'Basketball': '3', 'Hockey': '4',
        'Am. football': '5', 'American Football': '5', 'Baseball': '6',
        'Handball': '7', 'Rugby Union': '8', 'Floorball': '9',
        'Bandy': '10', 'Futsal': '11', 'Volleyball': '12',
        'Cricket': '13', 'Darts': '14', 'Snooker': '15',
        'Boxing': '16', 'Beach volleyball': '17', 'Aussie rules': '18',
        'Rugby League': '19', 'Badminton': '21', 'Water polo': '22',
        'Golf': '23', 'Field hockey': '24', 'Table tennis': '25',
        'Beach soccer': '26', 'MMA': '28', 'Netball': '29',
        'Pesäpallo': '30', 'Motorsport': '31', 'Motor Sport': '31',
        'Cycling': '34', 'Horse racing': '35', 'eSports': '36',
        'Winter Sports': '37', 'Kabaddi': '42',
    }
    
    try:
        oRequestHandler = cRequestHandler(URL_MAIN + 'assets/sports-feed.json')
        sHtmlContent = oRequestHandler.request()
        data = json.loads(sHtmlContent)
        
        # Collecter tous les sports uniques
        unique_sports = {}  # Dict pour éviter les doublons: {nom_sport: sport_id}
        
        if isinstance(data, list):
            for event in data:
                if isinstance(event, dict) and 's' in event:
                    sport_name = event['s'].strip()
                    # Chercher l'ID correspondant dans le mapping Flashscore
                    if sport_name in flashscore_sports:
                        sport_id = flashscore_sports[sport_name]
                        if sport_name not in unique_sports:
                            unique_sports[sport_name] = sport_id
        
        # Convertir en liste de tuples triée
        sports = sorted([(name, sport_id) for name, sport_id in unique_sports.items()])
        
        # Retourner les sports trouvés
        return sports
    
    except Exception:
        # En cas d'erreur, retourner toute la liste
        return sorted([(name, sport_id) for name, sport_id in flashscore_sports.items()])


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    # Récupérer la liste dynamique des genres
    genres = get_sports_list()
    
    oOutputParameterHandler = cOutputParameterHandler()
    for title, sport_id in genres:
        sGenreUrl = sUrl % sport_id

        oOutputParameterHandler.addParameter('siteUrl', sGenreUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', title)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', title, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def get_api_match_ids(sSportName):
    """
    Récupère les IDs des matchs présents dans l'API rdaily.live pour le sport et la date du jour
    Retourne une liste d'IDs de matchs présents dans l'API
    """
    try:
        # Mapper le nom du sport au slug utilisé dans l'API (minuscules)
        sport_slug = sSportName.lower()
        
        # Récupérer la date du jour au format YYYY-MM-DD
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Appeler l'API rdaily.live
        api_url = URL_MAIN + 'api/v1/%s/%s' % (sport_slug, today)
        oRequestHandler = cRequestHandler(api_url)
        response = oRequestHandler.request()
        
        # Parser la réponse JSON
        data = json.loads(response)
        
        # Extraire les IDs des matchs (adapter selon la structure réelle de l'API)
        match_ids = []
        for match in data['items']:
            match_ids.append(match.get('match_id', '').replace('FS:', ''))
        return match_ids
    
    except Exception:
        # En cas d'erreur, retourner une liste vide (tous les matchs seront affichés)
        return []


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSportName = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    matches = parse_feed(sHtmlContent)
    
    # Récupérer les IDs des matchs présents dans l'API rdaily.live
    api_match_ids = get_api_match_ids(sSportName)
    
    # Filtrer les matchs pour ne garder que ceux présents dans l'API
    if api_match_ids:
        matches = [m for m in matches if m.get('AA', '') in api_match_ids]
    
    # Trier les matchs à venir par heure de début
    matches.sort(key=lambda m: int(m.get('AD', '0')))
    
    # meu pour recharger la liste
    sDecoColor = addon().getSetting('deco_color')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sSportName)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR %s]Recharger la liste[/COLOR]' % sDecoColor, 'Synchro.png', oOutputParameterHandler, 'Recharger la liste')
    
    # Afficher les matchs
    for match in matches:
        try:
            match_id = match.get('AA', '')  # AA = match ID
            
            # Construire le titre avec les noms des joueurs/équipes
            player1 = match.get('CX', '')       # CX = 1er joueur/équipe
            player2 = match.get('AF', '')       # AF = 2e joueur/équipe
            tournament = match.get('ZA', '')    # ZA = tournoi
            sDisplayTitle = '%s / %s' % (player1, player2)
            
            # Construire le statut
            status = int(match.get('AB', '0'))
            status_text = '[COLOR limegreen] - EN COURS[/COLOR]' if status == 2 else ''

            # Afficher le titre avec l'heure si disponible
            start_time = int(match.get('AD', '0'))
            if start_time > 0:
                dt = datetime.fromtimestamp(start_time)
                time_str = dt.strftime('%H:%M')
                sDisplayTitle = '%s - %s' % (time_str, sDisplayTitle)
            

            if tournament:
                sDisplayTitle += '[COLOR grey] [%s][/COLOR]' % tournament.split(',')[0]
            sDesc = sDisplayTitle
              
            if status_text:
                sDisplayTitle += status_text

            # Récupérer les logos des équipes (OA et OB)
            sThumb = 'sport.png'  # icône par défaut
            sIcon = match.get('OAJ', '')  # Logo tournoi
            if sIcon :
                sIcon = 'https://static.flashscore.com/res/image/data/' + sIcon

            oOutputParameterHandler.addParameter('siteUrl', match_id)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sDisplayTitle, sIcon, sIcon, sDesc, oOutputParameterHandler)
        
        except Exception:
            continue

    if not sSearch:
        oGui.setEndOfDirectory()


def showLive():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sIdUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    # sUrl contient le match_id
    sUrl = URL_MAIN + 'api/v1/match/FS:%s' % sIdUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    try:
        data = json.loads(sHtmlContent)
    except:
        oGui.setEndOfDirectory()
        return

    if 'error' in data:
        oGui.setEndOfDirectory()
        return

    # les infos provenant de l'API
    urlInfo = URL_FLASHSCORE_API + 'dc_1_' + sIdUrl
    oRequestHandler = cRequestHandler(urlInfo)
    sInfoContent = oRequestHandler.request()
    matches = formatData(sInfoContent)
    sThumb = matches.get('DEI', 'sport.png')
    oHoster = cHosterGui().checkHoster('.m3u8')
    
    # Afficher les URLs de streaming disponibles par chaine
    URL_LINK = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_link')
    for aEntry in data.get('custom_urls', []):
        sStreamUrl = aEntry.get('url', '')
        sStreamName = aEntry.get('name', sMovieTitle)

        if sStreamUrl:
            sHosterUrl = URL_LINK % sStreamUrl
            oHoster.setDisplayName(sStreamName)
            oHoster.setFileName(sStreamName)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def formatData(block, fields = {}):
    for item in block.split("¬"):
        if "÷" in item:
            key, value = item.split("÷", 1)
            fields[key] = value
    
    return fields

def parse_feed(data):
    """
    Parse le feed Flashscore et retourne les matchs pertinents :
    - Tous les matchs en cours (AB=2)
    - Les matchs à venir (AB=1) dans les 3 prochaines heures
    """
    all_matches = []
    fields = {}
    
    # Parser le feed avec les séparateurs ~ et ¬ et ÷
    for block in data.split("~"):
        fields = formatData(block, fields)
        
        if "AA" in fields:  # AA = match ID
            all_matches.append(fields)
            fields = {}
    
    # Filtrer et trier les matchs pertinents des 3 prochaines heures
    now = time.time()  # Heure actuelle en timestamp Unix
    window_hours = 3
    window_seconds = window_hours * 3600
    
    matches = []
    heure_start = now - window_seconds
    heure_end = now + window_seconds
    
    for match in all_matches:
        try:
            status = int(match.get('AB', '0'))  # AB = statut du match
            
            if status == 2:
                # Matchs en cours
                matches.append(match)
            
            elif status == 1:
                # Matchs à venir
                start_time = int(match.get('AD', '0'))  # AD = heure prévue (Unix timestamp)
                
                # Garder seulement les matchs qui commencent dans les 3 prochaines heures
                if start_time > heure_start and start_time <= heure_end:
                    matches.append(match)
        
        except (ValueError, TypeError):
            # Ignorer les entrées mal formatées
            continue
    
    # Retourner les matchs pertinents : en cours et les prochains
    return matches