# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import dialog, xbmc, window
from datetime import datetime


SITE_IDENTIFIER = 'ePg'
SITE_NAME = 'epg'

d = datetime.now()
date = d.strftime("%d-%m-%Y")


class cePg:

    def view_epg(self, sTitle, sTime):
        text = self.get_epg(sTitle, sTime)
         
        if text:
            self.TextBoxes(sTitle, text)
        else:
            dialog().VSinfo('Impossible de trouver le guide tv')


    def get_epg(self, sTitle, sTime):
        oParser = cParser()
        
        # ce soir
        if sTime == 'direct':
            sUrl = 'http://playtv.fr/programmes-tv/en-direct/'
        elif sTime == 'soir':
            sUrl = 'http://playtv.fr/programmes-tv/' + date + '/20h-23h/'
        else:
            sUrl = 'http://playtv.fr/programmes-tv/' + date + '/20h-23h/'

        if 'Canal' in sTitle:
            sUrl += 'canal-plus/'
#         else:
#             sUrl += 'canalsat/'

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        text = ''
        if not sTitle:
            text = self.get_epg("CanalComplet", sTime)
        elif not "CanalComplet" in sTitle:
            sChannel = sTitle.replace('+', 'plus')

            try:
                sChannel = cUtil().CleanName(sChannel).replace(' ', '-')
            except:
                pass

            sHtmlContent = oParser.abParse(sHtmlContent, sChannel, '<!-- program -->')
            if not sChannel in sHtmlContent:
                return ''
        sPattern = 'href="\/chaine-tv\/(.+?)".+?<img.+?alt="(.+?)".+?|<span class="start" title="(.+?)">(.+?)</span>.+?<span class="program-gender small">.+?<span>(.+?)</span>.+?<a href=".+?" title=".+?">(.+?)</a>'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                # url
                if aEntry[0]:
                    text += "<" + aEntry[0] + ">\r\n"
                # chaine
                if aEntry[1]:
                    text += "[COLOR red]" + aEntry[1] + "[/COLOR]\r\n"
                # heure
                if aEntry[3]:
                    text += "[B]" + aEntry[3] + "[/B] -"
                # durée
                if aEntry[2]:
                    text += aEntry[2] + " : "
                # type
                if aEntry[4]:
                    text += "(" + aEntry[4] + ") "
                # title
                if aEntry[5]:
                    text += "     [COLOR khaki][UPPERCASE]" + aEntry[5] + "[/UPPERCASE][/COLOR] "
                # retour line
                text += "\r\n"

            return text
        return ''


    # EPG du programme en cours de la chaine
    def getChannelEpg(self, sChannel):
        
        oUtil = cUtil()
        oParser = cParser()

        info = {}
        info['title'] = ''
        info['year'] = ''
        info['duration'] = ''
        info['plot'] = ''
        info['media_type'] = ''
        info['cover_url'] = ''
        
        sChannel = sChannel.replace('+', 'plus')

        try:
            sChannel = oUtil.CleanName(sChannel)
        except:
            pass
            
        sChannel = sChannel.lower().replace(' ', '-')

        sUrl = 'https://playtv.fr/chaine-tv/en-direct/' + sChannel
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()


        sPattern = 'class="program-title"> *<a href="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sUrl = 'https://playtv.fr' + aResult[1][0]
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
          
            sPattern = '(<div class="program-img margin">.+?<img src="(.+?)".+?|)'+\
                'Genre du programme.+?<span>(.+?)</span>' + \
                '.+?"program-more-infos"'+ \
                '(.+?>Année</span> (.+?)</p>|)'+ \
                '(.+?Durée</span> <span>(.+?)</span>|)'+ \
                '.+?ProgrammeTitle-heading.+?title="(.+?)"' + \
                '.+?program-summary.+?<p>(.+?)</div>'
#             >1h40 / 35 minutes
#                 '.+?<span class="red">(.+?)<'+ \
    
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                aEntry = aResult[1][0]
                info['title'] = aEntry[7]
                info['year'] = aEntry[4]
                info['duration'] = aEntry[6]
                sDesc = aEntry[8].replace('<p>', '\r\n').replace('</p>', '')
                sDesc = oUtil.removeHtmlTags(sDesc)
                info['plot'] = sDesc
                info['media_type'] = aEntry[2]
                info['cover_url'] = aEntry[1]
        return info


    def TextBoxes(self, heading, anounce):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % 10147)
        # get window
        win = window(10147)
        # win.show()
        # give window time to initialize
        xbmc.sleep(100)
        # set heading
        win.getControl(1).setLabel(heading)
        win.getControl(5).setText(anounce)
        return


