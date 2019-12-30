import urllib

class cOutputParameterHandler:

    def __init__(self):
        self.__aParams = {}

    def addParameter(self, sParameterName, mParameterValue):
        if not mParameterValue:
            return
 
        self.__aParams[sParameterName] = urllib.unquote(str(mParameterValue))

    def getParameterAsUri(self):
        if len(self.__aParams) > 0:
            return urllib.urlencode(self.__aParams)

        return 'params=0'

    def getValue(self, sParamName):
        if (self.exist(sParamName)):
            sParamValue = self.__aParams[sParamName]
            return urllib.unquote(sParamValue)

        return False

    def exist(self, sParamName):
        if sParamName in self.__aParams:
            return sParamName