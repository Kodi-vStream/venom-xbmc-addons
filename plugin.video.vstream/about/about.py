from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
import datetime

class cAboutGui:

    SITE_NAME = 'cAboutGui'

    URL_MAIN = 'http://mitglied.multimania.de/murphy/gapi/index.php'

    def show(self):
        oGui = cGui()
        '''oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('showStatistic')
        oGuiElement.setTitle('Statistik')
        oGui.addFolder(oGuiElement) '''

        '''oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('showInfo')
        oGuiElement.setTitle('Info')
        oGui.addFolder(oGuiElement)'''        

        oGui.setEndOfDirectory()

    def showStatistic(self):        
        oGui = cGui()
        self.__getDateItems(oGui, 2)
        oGui.setEndOfDirectory()

    def showInfo(self):
        oGui = cGui()
        self.__createDummyFolder(oGui, 'Info')
        oGui.setEndOfDirectory()

    def __getDateItems(self, oGui, iDays):
        sToday = datetime.date.today()

        for i in range(iDays):
            sDifference = datetime.timedelta(i)
            sDate = sToday - sDifference
            self.__createDateFolder(oGui, str(sDate))

    def __createDateFolder(self, oGui, sDate):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('showStatisticData')
        oGuiElement.setTitle(sDate)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sDate', sDate)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def showStatisticData(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        if (oInputParameterHandler.exist('sDate')):
            sDate = oInputParameterHandler.getValue('sDate')
            sTitle = 'Statistik fuer den ' + str(sDate)
            self.__createDummyFolder(oGui, sTitle)

            oRequest = cRequestHandler(self.URL_MAIN)
            oRequest.addParameters('date', sDate)
            sHtmlContent = oRequest.request()
            print sHtmlContent

            sPattern = 'totalCount="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                iTotalCount = aResult[1][0]
                sTitle = 'Tagesaufrufe: ' + str(iTotalCount)
                self.__createDummyFolder(oGui, sTitle)

            sPattern = '<plugin name="([^"]+)">(.*?)</plugin>'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            print aResult
            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    sTitle = 'Plugin: ' + str(aEntry[0]) + ' - ' + str(aEntry[1]) + ' Aufrufe'
                    self.__createDummyFolder(oGui, sTitle)

        oGui.setEndOfDirectory()

    def __createDummyFolder(self, oGui, sTitle):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('dummyFolder')
        oGuiElement.setTitle(sTitle)
        oGui.addFolder(oGuiElement)

    def dummyFolder(self):
        oGui = cGui()
        oGui.setEndOfDirectory()