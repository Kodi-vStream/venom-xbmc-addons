from resources.lib.config import cConfig
#from traceback import print_exc
import urllib2
import xbmc
import xbmcgui
import xbmcvfs
import string
import re

class cDownload:
        
    def __createProcessDialog(self):
        oDialog = xbmcgui.DialogProgressBG()
        oDialog.create('Download')            
        self.__oDialog = oDialog

    def __createDownloadFilename(self, sTitle):
        sTitle = re.sub(' +',' ',sTitle) #Vire double espace
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in sTitle if c in valid_chars)
        filename = filename.replace(' .','.')
        #filename = filename.replace(' ','_') #pas besoin de ca, enfin pr moi en tout cas
        return filename

    def download(self, sUrl, sTitle):
        self.__processIsCanceled = False
        sTitle = self.__createTitle(sUrl, sTitle)
        self.__sTitle = self.__createDownloadFilename(sTitle)
        
        oGui = cConfig()
        self.__sTitle = oGui.showKeyBoard(self.__sTitle)
        if (self.__sTitle != False and len(self.__sTitle) > 0):

            #chemin de sauvegarde
            sPath2 = cConfig().getSetting('Download_Folder')

            dialog = xbmcgui.Dialog()
            sPath = dialog.browse(3, 'Downloadfolder', 'files', '', False, False , sPath2)
            
            if (sPath != ''):
                cConfig().setSetting('Download_Folder',sPath)
                
                sDownloadPath = xbmc.translatePath(sPath +  '%s' % (self.__sTitle, ))

                try:
                    cConfig().log("Telechargement " + str(sUrl))
                    self.__createProcessDialog()
                    self.__download(urllib2.urlopen(sUrl), sDownloadPath)   
                except:
                    #print_exc()
                    cConfig().showInfo('Telechargement impossible', self.__sTitle)
                    cConfig().log("Telechargement impossible")
                    pass
                    
                self.__oDialog.close()

    def __download(self, oUrlHandler, fpath):
        headers = oUrlHandler.info()
        
        iTotalSize = -1
        if "content-length" in headers:
            iTotalSize = int(headers["Content-Length"])

        chunk = 16 * 1024
        #f = open(fpath, "w")
        f = xbmcvfs.File(fpath, 'w')
        iCount = 0        
        while 1:
            iCount = iCount +1
            data = oUrlHandler.read(chunk)
            if not data: break
            f.write(data)
            self.__stateCallBackFunction(iCount, chunk, iTotalSize)
        oUrlHandler.close()
        f.close()
            

    def __createTitle(self, sUrl, sTitle):
        sTitle = re.sub('[\(\[].+?[\)\]]',' ', sTitle)
        
        
        aTitle = sTitle.rsplit('.')
        #Si deja extension
        if (len(aTitle) > 1):
            return sTitle
        
        #recherche d'une extension
        print sUrl
        sUrl = sUrl.lower()
        m = re.search('(flv|avi|mp4|mpg|mpeg)', sUrl)
        if m:
            sTitle = sTitle + '.' + m.group(0)
        else:
            sTitle = sTitle + '.flv' #Si quedale on en prend une au pif
            
        #aUrl = sUrl.rsplit('.')
        #if (len(aUrl) > 1):
        #    sSuffix = aUrl[-1]
        #    sTitle = sTitle + '.' + sSuffix
            
        return sTitle

    def __stateCallBackFunction(self, iCount, iBlocksize, iTotalSize):
        iPercent = int(float(iCount * iBlocksize * 100) / iTotalSize)
        self.__oDialog.update(iPercent, self.__sTitle, self.__formatFileSize(float(iCount * iBlocksize))+'/'+self.__formatFileSize(iTotalSize))

        if (self.__oDialog.isFinished()):
            self.__processIsCanceled = True
            self.__oDialog.close()
            
    
    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if (iBytes == 0):
            return '%.*f %s' % (2, 0, 'MB')
        
        return '%.*f %s' % (2, iBytes/(1024*1024.0) , 'MB')
