from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import xbmcgui
import xbmc

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'WatchVideo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'watchvideo'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self):
        sPattern = '(?://|\.)(watchvideo[0-9]?\.us)/(?:embed-)?([0-9a-zA-Z]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        
        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
   
        api_call = False
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
    
        #Dean Edwards Packer
        # sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        # aResult = oParser.parse(sHtmlContent, sPattern)
        
        # print "testttttttttttttttttttttttttttt"
        # test = "yaaaaaaaaaaaaaaaaaa"
        # xbmc.log ("lof: %s" % test)
        # print aResult
        
        
        
        # if (aResult[0] == True):
            # sUnpacked = cPacker().unpack(aResult[1][0])
            # sHtmlContent = sUnpacked
            
        sPattern = ',{file:"(.+?)",label:"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si au moins 1 url
            if (url):
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]

        #print api_call
        
        if (api_call):
            return True, api_call
            
        return False, False
