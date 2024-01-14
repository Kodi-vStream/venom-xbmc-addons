# -*- coding: utf-8 -*-
#
# author : Djeman
# Updated by Shani-08 (https://github.com/Shani-08/ShaniXBMCWork2)
import re


class AADecoder(object):
    def __init__(self, aa_encoded_data):
        self.encoded_str = aa_encoded_data.replace('/*´∇｀*/', '')

        self.b = ["(c^_^o)", "(ﾟΘﾟ)", "((o^_^o) - (ﾟΘﾟ))", "(o^_^o)",
                  "(ﾟｰﾟ)", "((ﾟｰﾟ) + (ﾟΘﾟ))", "((o^_^o) +(o^_^o))", "((ﾟｰﾟ) + (o^_^o))",
                  "((ﾟｰﾟ) + (ﾟｰﾟ))", "((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "(ﾟДﾟ) .ﾟωﾟﾉ", "(ﾟДﾟ) .ﾟΘﾟﾉ",
                  "(ﾟДﾟ) ['c']", "(ﾟДﾟ) .ﾟｰﾟﾉ", "(ﾟДﾟ) .ﾟДﾟﾉ", "(ﾟДﾟ) [ﾟΘﾟ]"]

    def is_aaencoded(self):
        idx = self.encoded_str.find("ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //*´∇｀*/ ['_']; o=(ﾟｰﾟ)  =_=3; c=(ﾟΘﾟ) =(ﾟｰﾟ)-(ﾟｰﾟ); ")
        if idx == -1:
            return False

        if self.encoded_str.find("(ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_');", idx) == -1:
            return False

        return True

    def base_repr(self, number, base=2, padding=0):
        digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if base > len(digits):
            base = len(digits)

        num = abs(number)
        res = []
        while num:
            res.append(digits[num % base])
            num //= base
        if padding:
            res.append('0' * padding)
        if number < 0:
            res.append('-')
        return ''.join(reversed(res or '0'))

    def decode_char(self, enc_char, radix):
        end_char = "+ "
        str_char = ""
        while enc_char != '':
            found = False

            for i in range(len(self.b)):
                if enc_char.find(self.b[i]) == 0:
                    str_char += self.base_repr(i, radix)
                    enc_char = enc_char[len(self.b[i]):]
                    found = True
                    break

            if not found:
                for i in range(len(self.b)):
                    enc_char = enc_char.replace(self.b[i], str(i))

                startpos = 0
                findClose = True
                balance = 1
                result = []
                if enc_char.startswith('('):
                    l = 0

                    for t in enc_char[1:]:
                        l += 1
                        if findClose and t == ')':
                            balance -= 1
                            if balance == 0:
                                result += [enc_char[startpos:l+1]]
                                findClose = False
                                continue
                        elif not findClose and t == '(':
                            startpos = l
                            findClose = True
                            balance = 1
                            continue
                        elif t == '(':
                            balance += 1

                if result is None or len(result) == 0:
                    return ""
                else:

                    for r in result:
                        value = self.decode_digit(r, radix)
                        if value == "":
                            return ""
                        else:
                            str_char += value

                    return str_char

            enc_char = enc_char[len(end_char):]

        return str_char

    def decode_digit(self, enc_int, radix):

        # enc_int = enc_int.replace('(ﾟΘﾟ)', '1').replace('(ﾟｰﾟ)', '4').replace('(c^_^o)', '0').replace('(o^_^o)', '3')

        rr = '(\(.+?\)\))\+'
        rerr = enc_int.split('))+')
        v = ''

        # new mode
        if True:

            for c in rerr:

                if len(c) > 0:
                    if c.strip().endswith('+'):
                        c = c.strip()[:-1]

                    startbrackets = len(c)-len(c.replace('(', ''))
                    endbrackets = len(c)-len(c.replace(')', ''))

                    if startbrackets > endbrackets:
                        c += ')' * startbrackets-endbrackets

                    # fh = open('c:\\test.txt', "w")
                    # fh.write(c)
                    # fh.close()

                    c = c.replace('!+[]', '1')
                    c = c.replace('-~', '1+')
                    c = c.replace('[]', '0')

                    v += str(eval(c))

            return v

        # mode 0=+, 1=-
        mode = 0
        value = 0

        while enc_int != '':
            found = False
            for i in range(len(self.b)):
                if enc_int.find(self.b[i]) == 0:
                    if mode == 0:
                        value += i
                    else:
                        value -= i
                    enc_int = enc_int[len(self.b[i]):]
                    found = True
                    break

            if not found:
                return ""

            enc_int = re.sub('^\s+|\s+$', '', enc_int)
            if enc_int.find("+") == 0:
                mode = 0
            else:
                mode = 1

            enc_int = enc_int[1:]
            enc_int = re.sub('^\s+|\s+$', '', enc_int)

        return self.base_repr(value, radix)

    def decode(self):

        self.encoded_str = re.sub('^\s+|\s+$', '', self.encoded_str)

        # get data
        pattern = (r"\(ﾟДﾟ\)\[ﾟoﾟ\]\+ *(.+?)\(ﾟДﾟ\)\[ﾟoﾟ\]\)")
        result = re.search(pattern, self.encoded_str, re.DOTALL)
        if result is None:
            print("AADecoder: data not found")
            return False

        data = result.group(1)

        # hex decode string
        begin_char = "(ﾟДﾟ)[ﾟεﾟ]+"
        alt_char = "(oﾟｰﾟo)+ "

        out = ''

        while data != '':
            # Check new char
            if data.find(begin_char) != 0:
                print("AADecoder: data not found")
                return False

            data = data[len(begin_char):]

            # Find encoded char
            enc_char = ""
            if data.find(begin_char) == -1:
                enc_char = data
                data = ""
            else:
                enc_char = data[:data.find(begin_char)]
                data = data[len(enc_char):]

            radix = 8
            # Detect radix 16 for utf8 char
            if enc_char.find(alt_char) == 0:
                enc_char = enc_char[len(alt_char):]
                radix = 16

            str_char = self.decode_char(enc_char, radix)

            if str_char == "":
                print("no match:  ")
                print(data + "\nout = " + out + "\n")
                return False

            out += chr(int(str_char, radix))

        if out == "":
            print("no match: " + data)
            return False

        return out

# version 2 si l'autre fonctionne pas.
# https://github.com/alfa-addon/addon/blob/master/plugin.video.alfa/lib/aadecode.py
# ------------------------------------------------------------
# Modified by jsergio


def decodeAA(text):
    text = re.sub(r"\s+|/\*.*?\*/", "", text)
    data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
    chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]

    txt = ""
    for char in chars:
        char = char \
            .replace("(oﾟｰﾟo)", "u") \
            .replace("c", "0") \
            .replace("(ﾟДﾟ)['0']", "c") \
            .replace("ﾟΘﾟ", "1") \
            .replace("!+[]", "1") \
            .replace("-~", "1+") \
            .replace("o", "3") \
            .replace("_", "3") \
            .replace("ﾟｰﾟ", "4") \
            .replace("(+", "(")
        char = re.sub(r'\((\d)\)', r'\1', char)

        c = ""
        subchar = ""
        for v in char:
            c += v
            try:
                x = c
                subchar += str(eval(x))
                c = ""
            except:
                pass
        if subchar != '': txt += subchar + "|"
    txt = txt[:-1].replace('+', '')

    txt_result = "".join([chr(int(n, 8)) for n in txt.split('|')])

    return toStringCases(txt_result)


def toStringCases(txt_result):
    sum_base = ""
    m3 = False
    if ".toString(" in txt_result:
        if "+(" in txt_result:
            m3 = True
            try:
                sum_base = "+" + re.search(".toString...(\d+).", txt_result, re.DOTALL).groups(1)
            except:
                sum_base = ""
            txt_pre_temp = re.findall("..(\d),(\d+).", txt_result, re.DOTALL)
            txt_temp = [(n, b) for b, n in txt_pre_temp]
        else:
            txt_temp = re.findall('(\d+)\.0.\w+.([^\)]+).', txt_result, re.DOTALL)
        for numero, base in txt_temp:
            code = toString(int(numero), eval(base + sum_base))
            if m3:
                txt_result = re.sub(r'"|\+', '', txt_result.replace("(" + base + "," + numero + ")", code))
            else:
                txt_result = re.sub(r"'|\+", '', txt_result.replace(numero + ".0.toString(" + base + ")", code))
    return txt_result


def toString(number, base):
    string = "0123456789abcdefghijklmnopqrstuvwxyz"
    if number < base:
        return string[number]
    else:
        return toString(number // base, base) + string[number % base]
