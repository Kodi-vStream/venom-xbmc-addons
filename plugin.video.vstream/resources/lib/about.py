#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.

#sLibrary = xbmc.translatePath(cConfig().getAddonPath()).decode("utf-8")
#sys.path.append (sLibrary) 

from resources.lib.comaddon import addon, dialog, xbmc
from resources.lib.handler.requestHandler import cRequestHandler

import urllib
import xbmcvfs
import datetime, time

SITE_IDENTIFIER = 'about'
SITE_NAME = 'About'


class cAbout:       
            
    #retourne True si les 2 fichiers sont present mais pas avec les meme tailles
    def checksize(self, filepath,size):
        try:
            #f=open(xbmc.translatePath(filepath))
            #Content = file.read()
            #file.close()
            #len(Content)

            f = xbmcvfs.File(filepath)
            s = f.size()
            f.close()

            if s == size:
                #ok fichier existe et meme taille
                return False
            #fichier existe mais pas la meme taille 
            return True
        except:
            #fichier n'existe pas
            return False

        #au cas ou ....
        return False
        
    
    def getUpdate(self):
        addons = addon()
        service_time = addons.getSetting('service_time')
        
        #Si pas d'heure indique = premiere install
        if not (service_time):
            #On memorise la date d'aujourdhui
            addons.setSetting('service_time', str(datetime.datetime.now()))
            #Mais on force la maj avec une date a la con
            service_time = '2000-09-23 10:59:50.877000'
        
        if (service_time):
            #delay mise a jour            
            time_sleep = datetime.timedelta(hours=72)
            time_now = datetime.datetime.now()
            time_service = self.__strptime(service_time, "%Y-%m-%d %H:%M:%S.%f")
            #pour test
            #if (time_sleep):
            if (time_now - time_service > time_sleep):
                #test les fichier pour mise a jour
                #self.checkupdate()
                result = self.resultGit()        
                sDown = 0
                
                if result:
                    for i in result:
                        try: 
                            rootpath = self.getRootPath(i['path'])       
                            
                            if self.checksize(rootpath,i['size']):
                                sDown = sDown+1
                                break #Si on en trouve un, pas besoin de tester les autres.
                                
                        except:
                            VSlog('erreur : verification MAJ' )
                            return
                    
                    if (sDown != 0):
                        addons.setSetting('home_update', str('true')) 
                        addons.setSetting('service_time', str(datetime.datetime.now()))
                        dialog().VSinfo("Mise à jour disponible")   
                    else:
                        #cConfig().showInfo('vStream', 'Fichier a jour')
                        addons.setSetting('service_time', str(datetime.datetime.now()))
                        addons.setSetting('home_update', str('false'))

            else:
                VSlog('Prochaine verification de MAJ le : ' + str(time_sleep + time_service) )
                #Pas besoin de memoriser la date, a cause du cache kodi > pas fiable.
        return
      
    #bug python
    def __strptime(self, date, format):
        try:
            date = datetime.datetime.strptime(date, format)
        except TypeError:
            date = datetime.datetime(*(time.strptime(date, format)[0:6]))
        return date
        

    def getRootPath_old(self, folder):
        sMath = cConfig().getAddonPath().replace('plugin.video.vstream', '').decode("utf-8")
        
        sFolder = os.path.join(sMath , folder)
        
        # xbox hack        
        sFolder = sFolder.replace('\\', '/')
        return sFolder

    def getRootPath(self, folder):

        path = "special://home/addons"
        path = "/".join([path, folder]) 
        return path
    
    
    def resultGit(self):
        try:    import json
        except: import simplejson as json

        print test
        
        try: 
            sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/sites.json'
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            result = json.loads(sHtmlContent)
            
            sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/hosts.json'
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            result += json.loads(sHtmlContent)
            #filtre trash & _init
            result = filter(lambda x: x['name']!="trash", result)
            result = filter(lambda x: x['name']!="__init__.py", result)
        except:
            return False
        return result
    

  #plus utiliser depuis le 24/06/18
    def checkupdate(self):
                  
        #dialog = cConfig().showInfo("vStream", "Cherche les mises a jour")            
        result = self.resultGit()        
        sDown = 0
        
        if result:
            for i in result:
                try: 
                    rootpath = self.getRootPath(i['path'])
                    
                    if self.checksize(rootpath,i['size']):
                        sDown = sDown+1
                        break #Si on en trouve un, pas besoin de tester les autres.
                        
                except:
                    VSlog('Erreur durant verification MAJ' )
                    return
             
            if (sDown != 0):
                cConfig().setSetting('home_update', str('true')) 
                cConfig().setSetting('service_time', str(datetime.datetime.now()))
                dialog = cConfig().showInfo("vStream", "Mise à jour disponible")   
            else:
                #cConfig().showInfo('vStream', 'Fichier a jour')
                cConfig().setSetting('service_time', str(datetime.datetime.now()))
                cConfig().setSetting('home_update', str('false'))
            
        return

    def checkdownload(self):

        result = self.resultGit()

        total = len(result)
        progress_ = progress()
        progress_.VScreate('Update')

        addons = addon()
        site = []
        sdown = 0

        if result: 
            
            for i in result:
                progress_.VSupdate(progress_, total)

                rootpath = self.getRootPath(i['path'])
                
                if self.checksize(rootpath,i['size']):
                    try:
                        self.__download(i['download_url'], rootpath)
                        site.append("[COLOR green]"+i['name'].encode("utf-8")+"[/COLOR]")
                        sdown = sdown+1
                    except:
                        site.append("[COLOR red]"+i['name'].encode("utf-8")+"[/COLOR]")
                        sdown = sdown+1
                        pass

            progress_.VSclose(progress_)

            sContent = "Fichier mise à jour %s / %s \n %s" %  (sdown, total, site)
            
            addons.setSetting('service_time', str(datetime.datetime.now()))
            addons.setSetting('home_update', str('false'))
            
            fin = dialog().VSok(sContent)
            xbmc.executebuiltin("Container.Refresh")
        return
            
    def __download(self, WebUrl, RootUrl):
        inf = urllib.urlopen(WebUrl)
        f = xbmcvfs.File(RootUrl, 'w')
        #save it
        line = inf.read()         
        f.write(line)
        
        inf.close()
        f.close()

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
                self.win = window( self.WINDOW )
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
