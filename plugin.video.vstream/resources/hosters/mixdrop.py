# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import urllib.parse
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'mixdrop', 'Mixdrop')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        super(cHoster, self).setUrl(url.replace("/f/", "/e/"))

    # def setDisplayName(self, sDisplayName):
    #     # Suppression du mot "Mixdrop" et nettoyage des espaces
    #     clean = re.sub(r'\b[Mm]ixdrop\b', '', str(sDisplayName), flags=re.IGNORECASE)
    #     clean = re.sub(r'\s+', ' ', clean).strip()
    #
    #     # Reformatage du titre : "Titre (Année) - [1080p] Server T1 (EN)"
    #     if clean.startswith('[') and ' - ' in clean:
    #         parts = clean.split(' - ', 1)
    #         tags = parts[0].strip()
    #         title = parts[1].strip()
    #         clean = '{0} - {1}'.format(title, tags)
    #
    #     super(cHoster, self).setDisplayName(clean)

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        # 1. Requête initiale avec User-Agent synchronisé
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Cookie', 'hds2=1')
        sHtmlContent = oRequest.request()
        
        # Capture obligatoire de l'URL finale si Mixdrop a fait une redirection HTTP (301/302)
        try:
            real_url = oRequest.getRealUrl()
            if real_url:
                self._url = real_url
        except:
            pass

        # Gestion d'une éventuelle redirection JavaScript par propriété location
        r = oParser.parse(sHtmlContent, r'location\s*=\s*["\']([^"\']+)["\']')
        if r[0]:
            web_url = urllib.parse.urljoin(self._url, r[1][0])
            self._url = web_url
            oRequest = cRequestHandler(self._url)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Cookie', 'hds2=1')
            sHtmlContent = oRequest.request()
            try:
                real_url = oRequest.getRealUrl()
                if real_url:
                    self._url = real_url
            except:
                pass

        # Extraction et décryptage du packer JS
        sPattern = r'(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])

            # Recherche élargie du lien vidéo (wurl, surl ou vsr)
            sPattern = r'(?:vsr|wurl|surl)[^=]*=\s*"([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                # Nettoyage absolu des espaces et sauts de ligne
                clean_url = re.sub(r'\s+', '', aResult[1][0])

                if clean_url.startswith('//'):
                    api_call = 'https:' + clean_url
                elif not clean_url.startswith('http'):
                    api_call = 'https://' + clean_url
                else:
                    api_call = clean_url

            if api_call:
                # --- DÉTECTION AUTONOME DU DOMAINE ACTIF (Inspiré par Gujal00) ---
                active_domain = ''
                
                # A. Recherche prioritaire dans les balises canoniques ou OpenGraph du HTML
                r_domain = oParser.parse(sHtmlContent, r'(?:canonical|og:url)[^>]+(?:href|content)\s*=\s*["\']https?://([^/"\']+)')
                if r_domain[0]:
                    active_domain = r_domain[1][0]
                else:
                    # B. Recherche via le pattern regex complet des domaines Mixdrop dans le code
                    sPatternDomain = r'(?:mi*1*xdro*p\d*(?:jmk)?|md(?:3b0j6hj|bekjwqa|fx9dc8n|y48tn97|zsmutpcvykb)|mxdrop)\.(?:c[ho]m?|top?|bz|gl|club|click|vc|ag|pw|net|is|s[ibx]|nu|m[sy]|ps)'
                    match_domain = re.search(sPatternDomain, sHtmlContent, re.IGNORECASE)
                    if match_domain:
                        active_domain = match_domain.group(0)
                    else:
                        # C. Fallback ultime sur le netloc de l'URL finale après redirections
                        parsed_url = urllib.parse.urlparse(self._url)
                        active_domain = parsed_url.netloc

                origin_url = 'https://' + active_domain
                referer_url = origin_url + '/'

                # Construction du lien final avec en-têtes parfaitement synchronisés
                api_call = '{0}|Referer={1}&Origin={2}&User-Agent={3}'.format(
                    api_call, 
                    referer_url, 
                    origin_url, 
                    UA
                )
                
                return True, api_call

        return False, False