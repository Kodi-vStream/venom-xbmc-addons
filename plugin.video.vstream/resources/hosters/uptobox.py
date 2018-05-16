#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
from resources.lib.util import VSlog
import urllib2,urllib,xbmcgui,re,xbmc

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Uptobox'
        self.__sFileName = self.__sDisplayName
        self.oPremiumHandler = None
        self.stream = True

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR violet]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'uptobox'

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://uptobox.com/', '')
        self.__sUrl = self.__sUrl.replace('https://uptobox.com/', '')
        self.__sUrl = self.__sUrl.replace('iframe/', '')
        self.__sUrl = 'https://uptobox.com/' + str(self.__sUrl)
        
    def checkSubtitle(self,sHtmlContent):
        oParser = cParser()

        #On ne charge les sous titres uniquement si vostfr se trouve dans le titre.
        if re.search('<head\s*.+?>\s*<title>[^<>]+VOSTFR[^<>]*<\/title>',sHtmlContent,re.IGNORECASE):
        
            sPattern = '<track type=[\'"].+?[\'"] kind=[\'"]subtitles[\'"] src=[\'"]([^\'"]+).vtt[\'"] srclang=[\'"].+?[\'"] label=[\'"]([^\'"]+)[\'"]>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            if (aResult[0] == True):
                Files = []
                for aEntry in aResult[1]:
                    url = aEntry[0]
                    label = aEntry[1]
                    url = url + '.srt'
                    
                    if not url.startswith('http'):
                        url = 'http:' + url
                    if 'Forc' not in label:
                        Files.append(url)
                return Files

        return False

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        if (self.oPremiumHandler.isPremiumModeAvailable()):
            dialog3 = xbmcgui.Dialog()
            ret = dialog3.select('Choissisez votre mode de fonctionnement',['Passer en Streaming (via Uptostream)','Rester en direct (via Uptobox)'])

            #mode DL
            if ret == 1:
                self.stream = False
            #mode stream
            elif ret == 0:
                self.__sUrl = self.__sUrl.replace('uptobox.com/','uptostream.com/iframe/')
            else:
                return False
        
            cGui().showInfo('Resolve', self.__sDisplayName, 3)
            return self.__getMediaLinkByPremiumUser()
            
        else:
            VSlog('no premium')
            return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        self.stream = True
        self.__sUrl = self.__sUrl.replace('uptobox.com/','uptostream.com/iframe/')
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        SubTitle = ''
        SubTitle = self.checkSubtitle(sHtmlContent)
        
        if (self.stream):
            api_call = self.GetMedialinkStreaming(sHtmlContent)
        else:
            api_call = self.GetMedialinkDL(sHtmlContent)
            
        if api_call:
            if SubTitle:               
                return True, api_call,SubTitle
            else:
                return True, api_call
            
        cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
        return False, False
        
        
    def __getMediaLinkByPremiumUser(self):
        
        if not self.oPremiumHandler.Authentificate():
            return self.__getMediaLinkForGuest()

        else:
            sHtmlContent = self.oPremiumHandler.GetHtml(self.__sUrl)
            #compte gratuit ou erreur auth
            if 'you can wait' in sHtmlContent or 'time-remaining' in sHtmlContent:
                VSlog('no premium')
                return self.__getMediaLinkForGuest()
            else:    
                SubTitle = ''
                SubTitle = self.checkSubtitle(sHtmlContent)
        
                if (self.stream):
                    api_call = self.GetMedialinkStreaming(sHtmlContent)
                else:
                    api_call = self.GetMedialinkDL(sHtmlContent)
            
                if api_call:
                    if SubTitle:
                        return True, api_call,SubTitle
                    else:
                        return True, api_call

                cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
                return False, False
        
    def GetMedialinkDL(self,sHtmlContent):

        oParser = cParser()

        sPattern =  '<a href *=[\'"](?!http:\/\/uptostream.+)([^<>]+?)[\'"] *class=\'big-button-green-flat mt-4 mb-4\''
        aResult = oParser.parse(sHtmlContent, sPattern)
  
        if (aResult[0]):
            return urllib.quote(aResult[1][0], safe=":/")
        
        return False

    def GetMedialinkStreaming(self,sHtmlContent):

        oParser = cParser()
        sPattern =  'src":[\'"]([^<>\'"]+)[\'"],"type":[\'"][^\'"><]+?[\'"],"label":[\'"]([0-9]+p)[\'"].+?"lang":[\'"]([^\'"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        stream_url = ''
        
        if (aResult[0] == True):
            url=[]
            qua=[]
            
            for aEntry in aResult[1]:
                url.append(aEntry[0])
                tmp_qua = aEntry[1]
                if (aEntry[2]):
                    if 'unknow' not in aEntry[2]:
                        tmp_qua = tmp_qua + ' (' + aEntry[2] + ')'
                qua.append(tmp_qua)
                
            #Si une seule url
            if len(url) == 1:
                stream_url = url[0]
            #si plus de une
            elif len(url) > 1:
                #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    stream_url = url[ret]
                else:
                    return False
            else:
                return False
            
            stream_url = urllib.unquote(stream_url)
            
            if not stream_url.startswith('http'):
                stream_url = 'http:' + stream_url
                
            return stream_url
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
            return False
        
        return False
