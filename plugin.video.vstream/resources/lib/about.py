#-*- coding: utf-8 -*-
#Venom.
from config import cConfig

import urllib, urllib2
import xbmc, xbmcgui, xbmcaddon
import sys, time, os
import hashlib, md5

SITE_IDENTIFIER = 'about'
SITE_NAME = 'About'

class cAbout:

    def __init__(self):
        self.main(sys.argv[1])
        #self.__sFunctionName = ''

    def get_remote_md5_sum(self, url, max_file_size=100*1024*1024):
        remote = urllib2.urlopen(url)
        hash = hashlib.md5()
     
        total_read = 0
        while True:
            data = remote.read(4096)
            total_read += 4096
     
            if not data or total_read > max_file_size:
                break
     
            hash.update(data)
     
        return hash.hexdigest()
      

    def main(self, env):
    
        sUrl = 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/plugin.video.vstream/changelog.txt'
        

        if (env == 'changelog'):
            oRequest =  urllib2.Request(sUrl)
            oResponse = urllib2.urlopen(oRequest)
            sContent = oResponse.read()
            self.TextBoxes('vStream Changelog', sContent)
            return

        if (env == 'about'):
            sContent = ' Auteur: LordVenom\n Version & Repository: https://github.com/LordVenom/venom-xbmc-addons/releases\n Question & Support: https://github.com/LordVenom/venom-xbmc-addons/issues \n Question & Support: Twitter @lordvenom57\n'
            self.TextBoxes('vStream Information', sContent)
            return

        else :

            stats_in = self.get_remote_md5_sum(sUrl) 

            stats_out = cConfig().getSetting('date_update')


            if (stats_out != stats_in):
                oRequest =  urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)
                sContent = oResponse.read()
                self.TextBoxes('Changelog', sContent)
                cConfig().setSetting('date_update', str(stats_in))
                return
        return

    def TextBoxes(self, heading, anounce):
        class TextBox():
            # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()

            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                    f = open(anounce)
                    text = f.read()
                except: text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()

cAbout()