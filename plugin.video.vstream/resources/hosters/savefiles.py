# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import sys
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
import re

# l'importation de cloudscraper
try:
    import cloudscraper
    _HAS_CLOUDSCRAPER = True
    _IMPORT_MSG = "OK : Module cloudscraper charge avec succes."
except Exception as e:
    _HAS_CLOUDSCRAPER = False
    _IMPORT_MSG = "ECHEC : " + str(e)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'savefiles', 'SaveFiles')

    def _getMediaLinkForGuest(self):
        log_file = None
        try:
            import __main__
            log_file = getattr(__main__, 'LINKFILE', None)
        except:
            pass

        def write_log(msg):
            if log_file:
                try:
                    with open(log_file, "a") as f:
                        f.write("\n[SF_DEBUG] " + str(msg) + "\n")
                except:
                    pass

        write_log("--- Debut du test SaveFiles ---")
        write_log("Statut initial import: " + _IMPORT_MSG)

        match = re.search(r'/(?:e|v)/([0-9a-zA-Z]+)', self._url)
        if not match:
            write_log("Erreur: Impossible d'extraire l'ID de l'URL: " + str(self._url))
            return False, False
            
        media_id = match.group(1)
        ref = self._url.split('/e/')[0] + '/' if '/e/' in self._url else self._url.split('/v/')[0] + '/'
        dl_url = ref + 'dl'

        post_data = {
            'op': 'embed',
            'file_code': media_id,
            'auto': '0',
            'referer': ''
        }

        player_html = ""

        if _HAS_CLOUDSCRAPER:
            write_log("Tentative d'execution via Cloudscraper...")
            try:
                scraper = cloudscraper.create_scraper(
                    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False},
                    delay=4
                )
                write_log("Scraper cree. Envoi de la requete POST sur: " + dl_url)
                
                response = scraper.post(dl_url, data=post_data, headers={"User-Agent": UA, "Referer": ref, "Origin": ref[:-1]}, timeout=15)
                player_html = response.text
                
                write_log("Reponse Cloudscraper recue. Code HTTP: " + str(response.status_code) + " | Taille HTML: " + str(len(player_html)))
            except Exception as e_cloud:
                write_log("Erreur CRASH pendant le POST Cloudscraper: " + str(e_cloud))
                player_html = ""
        else:
            write_log("Cloudscraper absent. Repli automatique sur le cRequestHandler natif...")
            try:
                oRequestHandler = cRequestHandler(dl_url)
                oRequestHandler.setRequestType(1)
                for key, value in post_data.items():
                    oRequestHandler.addParameters(key, value)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', ref)
                player_html = oRequestHandler.request()
                write_log("Reponse native recue. Taille HTML: " + str(len(player_html)))
            except Exception as e_native:
                write_log("Erreur CRASH pendant le POST natif: " + str(e_native))

        api_call = False
        sPattern = r'''sources:\s*\[(?:{\s*file\s*:)?\s*['"]([^'"]+)'''
        oParser = cParser()
        
        write_log("Lancement du regex pour trouver le lien final...")
        aResult = oParser.parse(player_html, sPattern)
        
        if aResult[0] is True:
            api_call = aResult[1][0] + '|User-Agent=' + UA + '&Referer=' + ref
            write_log("Succes ! Lien extrait: " + str(aResult[1][0]))
        else:
            write_log("Echec : Le pattern des sources n'a pas matche dans le HTML.")

        if api_call:
            return True, api_call

        return False, False
