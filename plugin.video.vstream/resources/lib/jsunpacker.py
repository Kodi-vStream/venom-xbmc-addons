
import re

class cJsUnpacker:

    def unpackByString(self, sJavascript):
        aSplit = sJavascript.split(";',")
        p = str(aSplit[0])

        aSplit = aSplit[1].split(",")
        a = int(aSplit[0])
        c = int(aSplit[1])
        k = aSplit[2].split(".")[0].replace("'", '').split('|')
        e = ''
        d = ''
       
        sUnpacked = str(self.__unpack(p, a, c, k, e, d))
        return sUnpacked.replace('\\', '')

    def __unpack(self, p, a, c, k, e, d):
        while (c > 1):
            c = c -1
            if (k[c]):               
                p = re.sub('\\b' + str(self.__itoa(c, a)) +'\\b', k[c], p)
        return p

    def __itoa(self, num, radix):
        result = ""
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result