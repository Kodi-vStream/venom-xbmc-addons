import urllib

class cOutputParameterHandler:

    def __init__(self):
        self.__aParams = {}

    def addParameter(self, sParameterName, mParameterValue):
        if not mParameterValue:
            return
        #test du 20/10
        #self.__aParams[sParameterName] = urllib.unquote_plus(str(mParameterValue))
        self.__aParams[sParameterName] = urllib.unquote(str(mParameterValue))

    def getParameterAsUri(self):
        if len(self.__aParams) > 0:
                return urllib.urlencode(self.__aParams)
        return 'params=0'
    
    def getValue(self, sParamName):
        if (self.exist(sParamName)):
                sParamValue = self.__aParams[sParamName]
                #test du 20/10
                #return urllib.unquote_plus(sParamValue)
                return urllib.unquote(sParamValue)
        return False
            
    def exist(self, sParamName):
        return self.__aParams.has_key(sParamName)
