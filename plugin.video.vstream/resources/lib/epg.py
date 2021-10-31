# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.comaddon import dialog, isMatrix
from datetime import datetime

import xml.etree.ElementTree as ET
import requests
import re
import unicodedata

SITE_IDENTIFIER = 'ePg'
SITE_NAME = 'epg'

class cePg:

    def view_epg(self, sTitle, sTime,text=None):
        if text == None:
            text = self.getEpg(sTitle, sTime)
         
        if text:
            self.TextBoxes(sTitle, text)
        else:
            dialog().VSinfo('Impossible de trouver le guide tv')


    def getEpg(self, sTitle, sTime, noTextBox=False):
        #Si noTextBox == True, ca veux dire que l'appel viens d'une source.
        #Dans ce cas la, on normalise les noms pour faciliter la detection.
        sUrl = "https://xmltv.ch/xmltv/xmltv-complet_1jour.xml"

        # dialog().VSinfo("Chargement du guide TV")

        d = datetime.now()
        if 'soir' in sTime:
            date = d.strftime("%Y%m%d210000")
        else:
            date = d.strftime("%Y%m%d%H%M%S")

        r = requests.get(sUrl, stream=True)

        xmltv_l = self.read_programmes(r, date)

        tree = ET.fromstring(b''.join(xmltv_l))

        programmes = []

        text = ""
        channelList = {}
        for child in tree.findall('channel'):
            channelList.update({child.get('id'):child.find('display-name').text})

        for elem in tree.findall('programme'):
            if elem.get('start'):
                formatTime = self.parse_date_tz(elem.get('start').split(' ')[0], elem.get('stop').split(' ')[0])
                channelId = elem.get("channel")
                if not isinstance(channelId, str):
                    channelId = channelId.decode('utf-8')
                channel = channelList[channelId]
                if noTextBox:
                    channel = self._clean_name(channel)
                text += "[COLOR red]" + channel + "[/COLOR]\r\n"                  
                text += "[B]" + formatTime + "[/B]\r\n"
                text += "[COLOR khaki][UPPERCASE]" + elem.find('title').text + "[/UPPERCASE][/COLOR]\r\n"
                if elem.find('category') is not None:    
                    text += "(" +  elem.find('category').text + ") \r\n"
                if elem.find('desc') is not None:
                    text +=  elem.find('desc').text
            text += "\r\n"
            
            
        if not isMatrix():
            text = text.encode('utf8')
        return text


    def parse_date_tz(self, dateStart, dateEnd):
        #Convert 20211019163600  to 2021-10-19 16:36
        formatTime = dateStart[8:10] + ":" + dateStart[10:12] + "-" +  dateEnd[8:10] + ":" + dateEnd[10:12] + " " + dateStart[6:8] + "-" + dateStart[4:6] + "-" + dateStart[:4]  
        return formatTime

    def TextBoxes(self, heading, anounce):
        from resources.lib.comaddon import window, xbmc

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

    #Code de catchup tv and more.
    #https://github.com/Catch-up-TV-and-More/plugin.video.catchuptvandmore/blob/dev/resources/lib/xmltv.py
    def read_programmes(self, r, date):
        xmltv_l = []
        take_line = True
        for line in r.iter_lines():
            # Match the beginning of a program
            if b'<programme ' in line:
                try:
                    start = int(re.search(b'start="(.+?) ', line).group(1))  # UTC start time
                except Exception:
                    take_line = False
                    continue

                try:
                    stop = int(re.search(b'stop="(.+?) ', line).group(1))  # UTC stop time
                except Exception:
                    stop = 50000000000000

                if int(date) >= start and int(date) <= stop:
                    pass
                else:
                    take_line = False
                    continue

            # Keep this line if needed
            if take_line:
                xmltv_l.append(line)

            # Match the end of a program
            if b'</programme>' in line:
                take_line = True
        return xmltv_l

    def getChannelEpg(self, EPG, channelName):

        if not EPG:
            return ''

        try:
            searchName = self._clean_name(channelName).replace('+',"\\+")
            sDesc = re.search("\[COLOR red\]" + searchName + "\[\/COLOR\](.+?)\[COLOR red", EPG, re.MULTILINE|re.DOTALL).group(1)
        except Exception as e:
            sDesc = ''
        return sDesc


    def _clean_name(self, name):
        # vire accent
        try:
            if isinstance(name, str):
                name = unicode(name, 'utf-8')
            name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('unicode_escape')
            if not isMatrix():
                name = name.encode('utf-8')  # on repasse en utf-8
        except Exception as e:
            pass

        name = name.replace(' +',"+").lower().strip()
        return name
