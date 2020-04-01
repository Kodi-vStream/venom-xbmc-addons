# To use it
#
#    Key = "a949abce37b369f11237d3c7a04c5721"
#    x = GKDecrypter(128,128)
#    sUrl = x.decrypt(EncodedLink.group(1), Key.decode("hex"), "ECB").split('\0')[0]
#
#        Key = "787I8fNAUERTrrbbT1nxg"
#        x = GKDecrypter(192,128)
#    sUrl = x.decrypt(EncodedLink, Key, "ECB").split('\0')[0]
#
#

import math

class GKDecrypter:
    def __init__(self, param1, param2):

        self.Rcon = [1,2,4,8,16,32,64,128,27,54,108,216,171,77,154,47,94,188,99,198,151,53,106,212,179,125,250,239,197,145]
        self.SBox = [99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,118,202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,183,253,147,38,54,63,247,204,52,165,229,241,113,216,49,21,4,199,35,195,24,150,5,154,7,18,128,226,235,39,178,117,9,131,44,26,27,110,90,160,82,59,214,179,41,227,47,132,83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,208,239,170,251,67,77,51,133,69,249,2,127,80,60,159,168,81,163,64,143,146,157,56,245,188,182,218,33,16,255,243,210,205,12,19,236,95,151,68,23,196,167,126,61,100,93,25,115,96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,224,50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,231,200,55,109,141,213,78,169,108,86,244,234,101,122,174,8,186,120,37,46,28,166,180,198,232,221,116,31,75,189,139,138,112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,158,225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,140,161,137,13,191,230,66,104,65,153,45,15,176,84,187,22]
        self.SBoxInverse = [82,9,106,213,48,54,165,56,191,64,163,158,129,243,215,251,124,227,57,130,155,47,255,135,52,142,67,68,196,222,233,203,84,123,148,50,166,194,35,61,238,76,149,11,66,250,195,78,8,46,161,102,40,217,36,178,118,91,162,73,109,139,209,37,114,248,246,100,134,104,152,22,212,164,92,204,93,101,182,146,108,112,72,80,253,237,185,218,94,21,70,87,167,141,157,132,144,216,171,0,140,188,211,10,247,228,88,5,184,179,69,6,208,44,30,143,202,63,15,2,193,175,189,3,1,19,138,107,58,145,17,65,79,103,220,234,151,242,207,206,240,180,230,115,150,172,116,34,231,173,53,133,226,249,55,232,28,117,223,110,71,241,26,113,29,41,197,137,111,183,98,14,170,24,190,27,252,86,62,75,198,210,121,32,154,219,192,254,120,205,90,244,31,221,168,51,136,7,199,49,177,18,16,89,39,128,236,95,96,81,127,169,25,181,74,13,45,229,122,159,147,201,156,239,160,224,59,77,174,42,245,176,200,235,187,60,131,83,153,97,23,43,4,126,186,119,214,38,225,105,20,99,85,33,12,125]
        self.keySize = param1
        self.blockSize = param2
        self.roundsArray = [0,0,0,0,[0,0,0,0,10,0,12,0,14],0,[0,0,0,0,12,0,12,0,14],0,[0,0,0,0,14,0,14,0,14]]
        self.shiftOffsets = [0,0,0,0,[0,1,2,3],0,[0,1,2,3],0,[0,1,3,4]]
        self.Nb = param2 / 32
        self.Nk = param1 / 32
        self.Nr = self.roundsArray[self.Nk][self.Nb]


    def decrypt(self,param1, param2, param3):
        _loc10_ = None
        _loc4_ = []
        _loc5_ = []
        _loc6_ = self.hexToChars(param1)#==48 characters
        _loc7_ = self.blockSize / 8
        _lo8st = self.strToChars(param2)
        _loc8_ = self.keyExpansion(_lo8st)
        _loc9_ = (len(_loc6_) / _loc7_) - 1

        while _loc9_ > 0:
            _loc5_ = self.decryption(_loc6_[_loc9_ * _loc7_:(_loc9_ + 1) * _loc7_],_loc8_)
            _loc4_ = _loc5_ + (_loc4_)
            _loc9_ -= 1
        _loc44 = self.decryption(_loc6_[0:int(_loc7_)],_loc8_)
        _loc4_ = _loc44+_loc4_
        _loc4_ = self.charsToStr(_loc4_)

        return _loc4_


    def MyInt(self, x):
        x = 0xffffffff & x
        if x > 0x7fffffff :
            return - ( ~(x - 1) & 0xffffffff )
        else : return x


    def keyExpansion(self, param1):
        _loc4_ = None
        _loc2_ = 0
        self.Nk = self.keySize / 32#=6, what if this was 5
        self.Nb = self.blockSize / 32
        _loc3_ = []
        self.Nr = self.roundsArray[self.Nk][self.Nb]# ==12, what if this was 10?
        _loc4_ = 0
        _loc3_ = [0]*(self.Nb * (self.Nr + 1))
        while _loc4_ < self.Nk:
            if (_loc4_)<len(param1)/4:
                _loc3_[_loc4_] = param1[4 * _loc4_] | param1[4 * _loc4_ + 1] << 8 | param1[4 * _loc4_ + 2] << 16 | param1[4 * _loc4_ + 3] << 24
            _loc4_ += 1
        _loc4_ = self.Nk
        while _loc4_ < self.Nb * (self.Nr + 1):
            _loc2_ = _loc3_[_loc4_ - 1]
            if(_loc4_ % self.Nk == 0):
                _loc2_ = (self.SBox[_loc2_ >> 8 & 255] | self.SBox[_loc2_ >> 16 & 255] << 8 | self.SBox[_loc2_ >> 24 & 255] << 16 | self.SBox[_loc2_ & 255] << 24) ^ self.Rcon[int(math.floor(_loc4_ / self.Nk))-1]
            else:
                if(self.Nk > 6 and _loc4_ % self.Nk == 4):
                    _loc2_ = self.SBox[_loc2_ >> 24 & 255] << 24 | self.SBox[_loc2_ >> 16 & 255] << 16 | self.SBox[_loc2_ >> 8 & 255] << 8 | self.SBox[_loc2_ & 255]
            _loc3_[_loc4_] = self.MyInt(_loc3_[_loc4_ - self.Nk] ^ _loc2_)
            _loc4_ += 1

        return _loc3_


    def hexToChars(self, param1):
        _loc2_ = []
        _loc3_ = 0
        if param1[0:1] == '0x':
            _loc3_ = 2

        while _loc3_ < len(param1):
            _loc2_.append(int(param1[_loc3_: _loc3_ + 2], 16))
            _loc3_ = _loc3_ + 2

        return _loc2_


    def strToChars(self, param1):
        _loc2_ = []
        _loc3_ = 0
        while(_loc3_ < len(param1)):
            _loc2_.append(ord(param1[_loc3_]))
            _loc3_+=1

        return _loc2_


    def charsToStr(self, param1):
        _loc2_ = ''
        _loc3_ = 0
        while(_loc3_ < len(param1)):
            _loc2_ = _loc2_ + chr(param1[_loc3_])
            _loc3_ += 1
        return _loc2_


    def packBytes(self, param1):
        _loc2_ = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        _loc3_ = 0
        while(_loc3_ < len(param1)):
            _loc2_[0][_loc3_ / 4] = param1[_loc3_]
            _loc2_[1][_loc3_ / 4] = param1[_loc3_ + 1]
            _loc2_[2][_loc3_ / 4] = param1[_loc3_ + 2]
            _loc2_[3][_loc3_ / 4] = param1[_loc3_ + 3]
            _loc3_ = _loc3_ + 4
        return _loc2_


    def unpackBytes(self, param1):
        _loc2_ = []
        _loc3_ = 0
        while(_loc3_ < len(param1[0])):
            _loc2_.append(param1[0][_loc3_])
            _loc2_.append(param1[1][_loc3_])
            _loc2_.append(param1[2][_loc3_])
            _loc2_.append(param1[3][_loc3_])
            _loc3_ += 1
        return _loc2_


    def InverseRound(self, param1, param2):
        _loc3_ = False
        _loc4_ = True

        self.addRoundKey(param1,param2)
        self.mixColumn(param1,'decrypt')
        self.shiftRow(param1,'decrypt')
        self.byteSub(param1,'decrypt')


    def FinalRound(self, param1, param2):
        self.byteSub(param1, 'encrypt')
        self.shiftRow(param1, 'encrypt')
        self.addRoundKey(param1, param2)


    def InverseFinalRound(self, param1, param2):
        self.addRoundKey(param1, param2)
        self.shiftRow(param1, 'decrypt')
        self.byteSub(param1, 'decrypt')


    def addRoundKey(self, param1, param2):
        _loc3_ = 0

        while(_loc3_ < self.Nb):
            param1[0][_loc3_] = param1[0][_loc3_] ^ param2[_loc3_] & 255
            param1[1][_loc3_] = param1[1][_loc3_] ^ param2[_loc3_] >> 8 & 255
            param1[2][_loc3_] = param1[2][_loc3_] ^ param2[_loc3_] >> 16 & 255
            param1[3][_loc3_] = param1[3][_loc3_] ^ param2[_loc3_] >> 24 & 255
            _loc3_ += 1


    def shiftRow(self, param1, param2):
        _loc4_ = True
        _loc5_ = False
        _loc3_ = 1

        while(_loc3_ < 4):
            if(param2 == 'encrypt'):
                param1[_loc3_] = self.cyclicShiftLeft(param1[_loc3_],self.shiftOffsets[self.Nb][_loc3_])
            else:
                param1[_loc3_] = self.cyclicShiftLeft(param1[_loc3_],self.Nb - self.shiftOffsets[self.Nb][_loc3_])

            _loc3_ += 1


    def cyclicShiftLeft(self, param1, param2):
        _loc3_ = param1[0: param2]
        param1 = param1[param2:]
        param1.extend(_loc3_)

        return param1


    def decryption(self, param1, param2):
        param1 = self.packBytes(param1)
        self.InverseFinalRound(param1,param2[self.Nb * self.Nr:])#nb*nr=42
        _loc3_ = self.Nr - 1
        while(_loc3_ > 0):
            self.InverseRound(param1,param2[(self.Nb * _loc3_):self.Nb * (_loc3_ + 1)])
            _loc3_-=1

        self.addRoundKey(param1,param2)
        reVal = self.unpackBytes(param1)

        return reVal


    def byteSub(self, param1, param2):
        _loc3_ = []
        _loc5_ = 0
        if(param2 == 'encrypt'):
            _loc3_ = self.SBox
        else:
            _loc3_ = self.SBoxInverse

        _loc4_ = 0

        while(_loc4_ < 4):
            _loc5_ = 0
            while(_loc5_ < self.Nb):
                param1[_loc4_][_loc5_] = _loc3_[param1[_loc4_][_loc5_]]
                _loc5_ += 1
            _loc4_ += 1


    def mixColumn(self, param1, param2):
        _loc4_ = 0
        _loc3_ = [0,0,0,0]
        _loc5_ = 0

        while(_loc5_ < self.Nb):
            _loc4_ = 0
            while(_loc4_ < 4):

                if(param2 == "encrypt"):
                    _loc3_[_loc4_] = self.mult_GF256(param1[_loc4_][_loc5_],2) ^ self.mult_GF256(param1[(_loc4_ + 1) % 4][_loc5_],3) ^ param1[(_loc4_ + 2) % 4][_loc5_] ^ param1[(_loc4_ + 3) % 4][_loc5_]
                else:
                    _loc3_[_loc4_] = self.mult_GF256(param1[_loc4_][_loc5_],14) ^ self.mult_GF256(param1[(_loc4_ + 1) % 4][_loc5_],11) ^ self.mult_GF256(param1[(_loc4_ + 2) % 4][_loc5_],13) ^ self.mult_GF256(param1[(_loc4_ + 3) % 4][_loc5_],9)
                _loc4_ += 1

            _loc4_ = 0
            while(_loc4_ < 4):
                param1[_loc4_][_loc5_] = _loc3_[_loc4_]
                _loc4_ += 1

            _loc5_ += 1


    def xtime(self, param1):
        param1 = param1 << 1
        if param1 & 256:
            return param1 ^ 283
        else:
            return param1


    def mult_GF256(self, param1, param2):
        _loc3_ = 0
        _loc4_ = 1

        while(_loc4_ < 256):
            if(param1 & _loc4_):
                _loc3_ = _loc3_ ^ param2
            _loc4_ = _loc4_ * 2
            param2 = self.xtime(param2)

        return _loc3_


def hexToChars(param1):
    _loc4_ = False
    _loc5_ = True
    _loc2_ = []
    _loc3_ = 0
    if param1[0:1] == '0x':
        _loc3_ = 2

    while _loc3_ < len(param1):
        _loc2_.append(int(param1[_loc3_: _loc3_ + 1], 16))
        _loc3_ = _loc3_ + 2

    return "".join(_loc2_)


def arrNametoString(param1):
    _loc4_ = True
    _loc5_ = False
    _loc2_ = ""
    param1.reverse()
    _loc3_ = 0
    while(_loc3_ < len(param1)):
        _loc2_ = _loc2_ + chr(param1[_loc3_])
        _loc3_ += 1

    return _loc2_


def decryptKey(param1):
    _local_2 = gledajfilmDecrypter(198, 128)
    _local_3 = [17536, 16512, 16524, 17420, 17544, 3144, 3204, 17416, 19532, 3080, 16456, 16460, 18572, 16396, 19468, 17408, 19464, 16524, 18508, 17420]
    _local_4 = bytearray()
    _local_5 = 0
    _local_6 = 0

    while _local_5 < len(_local_3):
        _local_6 = _local_3[_local_5]
        _local_6 = _local_6 >> 12
        _local_4.extend(bytes(_local_6))
        _local_5 += 1
    reVal = _local_2.decrypt(param1, str(_local_4), "ECB").split('\0')[0]

    return reVal
