import urllib

class cOutputParameterHandler:

    def __init__(self):
            self.__aParams = {}

    def addParameter(self, sParameterName, mParameterValue):
            self.__aParams[sParameterName] = urllib.unquote_plus(str(mParameterValue))

    def getParameterAsUri(self):
            if len(self.__aParams) > 0:
                    return urllib.urlencode(self.__aParams)
            return 'params=0'