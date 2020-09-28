import re, zlib

from resources.lib.config import GestionCookie
from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import cRequestHandler

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

class Stormwall(object):
    def __init__(self):
        self.cE = ''
        self.cK = ''
        self.cN = ''
        self.cO = ''
        self._0xbd1168 = "0123456789qwertyuiopasdfghjklzxcvbnm:?!"
        self.a = []
        self.b = {}

    def parseInt(self, sin):
        return int(''.join([c for c in re.split(r'[,.]',str(sin))[0] if c.isdigit()])) if re.match(r'\d+', str(sin), re.M) and not callable(sin) else None

    def func3(self, _0x32d742, _0x69aeb7):
        _0x5db4b0 = len(self.a) - 1
        _0x239b12 = ""
        _0x2b4227 = 0
        for _0x2b4227 in range(len(_0x69aeb7)):
            _0x44dcfd = _0x69aeb7[_0x2b4227];
            if not _0x44dcfd in self.b:
                _0x239b12 = _0x239b12 + _0x44dcfd
            else:
                _0x52a03d = self.b[_0x44dcfd] + _0x32d742
                if _0x52a03d > _0x5db4b0:
                  _0x52a03d = _0x52a03d - _0x5db4b0 - 1
                else:
                    if _0x52a03d < 0:
                        _0x52a03d = _0x5db4b0 + _0x52a03d + 1
                _0x239b12 = _0x239b12 + self.a[_0x52a03d];

        return _0x239b12

    def func5(self, _0x106033, _0x205fd6):
        _0x31b1ca = len(self.a) - 1
        _0x530eb7 = self.parseInt(_0x106033)
        _0x20559e = ""
        _0x1314ae = 0
        for _0x1314ae in range(len(_0x205fd6)):
            _0x1c696a = "" + _0x205fd6[_0x1314ae]
            _0x20559e = _0x20559e + self.func3(_0x530eb7 * -1, _0x1c696a)
            _0x530eb7 = _0x530eb7 + 1
            if _0x530eb7 > _0x31b1ca:
              _0x530eb7 = 0

        return _0x20559e

    def main(self, url, content):
        self.cE = re.search('const cE = "([^"]+)"', str(content)).group(1)
        self.cK = re.search('const cK = ([0-9]+)', str(content)).group(1)
        self.cN = re.search('const cN = "([^"]+)"', str(content)).group(1)
        self.cO = re.search('const cO = "([^"]+)"', str(content)).group(1)

        self.a = []
        self.b = {}

        for i in range(len(self._0xbd1168)):
           self.a.append(self._0xbd1168[i])
           self.b[self._0xbd1168[i]] = i


        _0x3b45bc = self.func5(self.cK, self.cE)

        GestionCookie().SaveCookie(url.split('/')[2], self.cN + "=" + _0x3b45bc + self.cO)
        VSlog ('cookie : '+ self.cN + "=" + _0x3b45bc)

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate, br')
        oRequestHandler.addHeaderEntry('Referer', url)
        oRequestHandler.addHeaderEntry('Cookie', self.cN + "=" + _0x3b45bc + self.cO)
        sHtmlContent = oRequestHandler.request()

        return sHtmlContent
