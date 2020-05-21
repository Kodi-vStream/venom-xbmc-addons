# -*- coding: utf-8 -*-
#
# *********************************************************************************************************************
# TinyJSParser https://github.com/TmpName/TinyJSParser
#
# A basic JS interpreter in python, made for the Kodi addon Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
# *********************************************************************************************************************


# TODO LIST
# ---------
# Regex will work only for normal name, not for exotic name
# Object
# Globla/Local variables/function/object
# utiliser un tableau special pr variable passe en parametres > clash

# help
# https://sarfraznawaz.wordpress.com/2012/01/26/javascript-self-invoking-functions/
# https://nemisj.com/python-api-javascript/
# https://fr.wikiversity.org/wiki/Python/Les_types_de_base
# https://javascriptobfuscator.com/Javascript-Obfuscator.aspx
# https://nemisj.com/python-api-javascript/

# UNICODE ERROR
# print(a.decode('utf-8').encode('ascii', 'replace'))
# true = 1 instead of true

# phrase=raw_input()
# phrase.xxx

# https://javascriptweblog.wordpress.com/2011/04/04/the-javascript-comma-operator/


import re
import types
from types import NoneType
import math

# import time
# import sys

REG_NAME = '[\w]+'
REG_OP = '[\/\*\-\+<>\|\&=~^%!]+'  # not space here, and no bracket
DEBUG = False  # Never enable it in kodi, too big size log
MAX_RECURSION = 50
ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

# if(!_0x45ae41[_0x5949('28')](_0x5949('9'),document)||!(!(typeof (document.write) == 'undefined'))){

# ---------------------------------------------------------------------------------


def logwrite(stri):
    fh = open('G:\\JSparser\\debug.txt', 'a')
    fh.write(stri + '\n')
    fh.close()


def RemoveGuil(string):
    if not (isinstance(string, types.StringTypes)):
        return string
    string = string.strip()
    if string.startswith('"') and string.endswith('"'):
        return string[1:-1]
    if string.startswith("'") and string.endswith("'"):
        return string[1:-1]
    return string


def ASCIIDecode(string):
    i = 0
    l = len(string)
    ret = ''
    while i < l:
        c = string[i]
        if string[i:(i + 2)] == '\\x':
            c = chr(int(string[(i + 2):(i + 4)], 16))
            i += 3
        if string[i:(i+2)] == '\\u':
            c = chr(int(string[(i + 2):(i + 6)], 16))
            i += 5
        ret = ret + c
        i += 1

    return ret


def IsUnicode(s):
    if isinstance(s, unicode):
        return True
    return False


def out(string):
    if DEBUG:
        print(str(string.decode('latin-1').encode('ascii', 'replace')))


def Ustr(string):
    if isinstance(string, unicode):
        return str(string.encode('ascii', 'replace'))
    return str(string)


def GetNextchar(string, pos):
    if len(string) <= (pos + 1):
        return ''
    return string[pos + 1]


def GetNextUsefullchar(string):
    j = 0
    try:
        while string[j].isspace():
            j += 1
    except:
        return '', 0
    return string[j], j


def GetPrevchar(string, pos):
    if (pos - 1) < 0:
        return ''
    return string[pos - 1]


def CheckType(value):
    if isinstance(value, types.StringTypes):
        return 'String'
    if isinstance(value, bool):
        return 'Bool'
    if isinstance(value, (int, long, float)):
        return 'Numeric'
    if type(value) in [list, tuple, dict]:
        return 'Array'
    if isinstance(value, NoneType):
        return 'Undefined'
    if isinstance(value, fonction):
        return 'Fonction'
    return 'Unknow'


# Fonction to return only one parameter from a string with correct closed [] () "" and ''
def GetItemAlone(string, separator=' '):

    l = len(string) - 1
    ret = ''

    i = -1
    p = 0   # parenthese
    a = 0   # accolade
    b = 0   # bracket
    c1 = 0  # chain with "
    c2 = 0  # chain with '
    n = False
    last_char = ''

    s = False

    while i < l:
        i += 1
        ch = string[i]
        ret = ret + ch
        n = False

        # Return if the is complete and before the char wanted but not if it's the first one
        if (ch in separator) and not p and not a and not b and not c1 and not c2 and not n and (i > 0):
            return ret[:-1]

        # Skip empty space
        if ch.isspace():
            continue

        if ch == '"' and not GetPrevchar(string, i) == '\\' and not c2:
            c1 = 1 - c1
        if ch == "'" and not GetPrevchar(string, i) == '\\' and not c1:
            c2 = 1 - c2

        if not c1 and not c2:
            if ch == '(':
                p += 1
            if ch == ')':
                p -= 1
            if ch == '{':
                a += 1
            if ch == '}':
                a -= 1
            if ch == '[':
                b += 1
            if ch == ']':
                b -= 1

            if ch == '.' and not ((last_char in '0123456789') or (string[i + 1] in '0123456789')):
                n = True

        # return if the chain is complete but with the char wanted
        if (ch in separator) and not p and not a and not b and not c1 and not c2 and not n and (i > 0):
            return ret

        last_char = ch

    return ret


def MySplit(string, char, NoEmpty=False):
    r = []
    l = len(string)
    i = 0
    chain = 0
    p = 0
    e = ''

    if not l:
        if NoEmpty:
            return []

    while l > i:
        c = string[i]
        if c == '"':
            chain = 1-chain
        if c == '(':
            p += 1
        if c == ')':
            p -= 1

        if (c == char) and not chain and not p:
            r.append(e.strip())
            e = ''
        else:
            e += c

        i += 1

    r.append(e.strip())
    return r


def GetConstructor(value):
    if isinstance(value, (int, long)):
        r = fonction('Number', '', '\n    [native code]\n', True)
        return r
    elif isinstance(value, fonction):
        r = fonction('Function', '', '\n    [native code]\n', True)
        return r
    elif isinstance(value, types.StringTypes):
        r = fonction('String', '', '\n    [native code]\n', True)
        return r
    return ''


class JSBuffer(object):
    PRIORITY = {'+': 3, '-': 3, '*': 4, '/': 4, '>': 1, '<': 1, '&': 2, '|': 2}

    def __init__(self):
        self.type = None
        self.buffer = ''
        self.__op = ''
        self.__value = None

        # buffers
        self.buf = []
        self.opBuf = []

    def SetOp(self, op):
        if (op == '&') and (self.__op == '&'):
            return
        if (op == '|') and (self.__op == '|'):
            return
        else:
            self.__op = self.__op + op

    def CheckString(self):
        if len(self.buf) >= len(self.opBuf):
            return True
        return False

    # Need 3 values for priority
    def AddValue(self, value):
        out('ADD ' + Ustr(value) + ' ' + Ustr(type(value)) + ' a ' + Ustr(self.buf))

        if not self.type:
            self.type = CheckType(value)
            self.Push(value, self.__op)
            return

        if not self.__op:
            out('op ' + str(self.opBuf) + ' - buff ' + str(self.buf))
            raise Exception('Missing operator')

        self.Push(value, self.__op)
        self.__op = ''

    def GetPrevious(self):
        ret = None
        if len(self.buf) > 0:
            ret = self.buf[-1]
            del self.buf[-1]
            self.__op = self.opBuf[-1]
            del self.opBuf[-1]
        if not len(self.buf):
            self.type = None

        return ret

    def Compute(self):

        # check type
        if len(self.buf) > 1:
            if not (self.type == CheckType(self.buf[len(self.buf) - 1])):
                # Type different mais juste operation logique
                if self.opBuf[1] == '==':
                    self.type = 'Logic'
                # Type different mais JS convertis en string
                else:
                    out('string convertion')

                    if not CheckType(self.buf[0]) == 'String':
                        self.buf[0] = self.SpecialStr(self.buf[0])
                    if len(self.buf) > 1:
                        if not CheckType(self.buf[1]) == 'String':
                            self.buf[1] = self.SpecialStr(self.buf[1])
                    self.type = 'String'

        # Work for operateur + | !
        if self.type == 'String':
            if '!' in self.opBuf[0]:
                self.buf[0] = not self.buf[0]
                self.opBuf[0] = self.opBuf[0].replace('!', '')
            if len(self.buf) > 1:
                if self.opBuf[1] == '!':
                    self.buf[1] = not self.buf[1]
                    self.opBuf[1] = self.opBuf[1].replace('!', '')
                if self.opBuf[1] == '+':
                    self.buf[0] = self.buf[0] + self.buf[1]
                if self.opBuf[1] == '|':
                    if not self.buf[0]:
                        self.buf[0] = self.buf[1]
                if '==' in self.opBuf[1]:
                    self.buf[0] = (self.buf[1] == self.buf[0])
                    self.type == 'Logic'
                if '!=' in self.opBuf[1]:
                    self.buf[0] = (self.buf[1] != self.buf[0])
                    self.type == 'Logic'

                # decale
                del self.opBuf[-1]
                del self.buf[-1]

        # work for all operator
        elif self.type == 'Numeric':
            if len(self.buf) > 1:
                self.buf[0] = self.opBuf[0] + str(self.buf[0]) + self.opBuf[1] + str(self.buf[1])
                self.opBuf[0] = ''
                # decale
                del self.opBuf[-1]
                del self.buf[-1]
            else:
                self.buf[0] = self.opBuf[0] + str(self.buf[0])
                self.opBuf[0] = ''

        # work for bool
        elif self.type == 'Bool':
            if len(self.buf) > 1:
                self.buf[0] = self.opBuf[0] + str(self.buf[0]) + self.opBuf[1] + str(self.buf[1])
                self.opBuf[0] = ''
                # decale
                del self.opBuf[-1]
                del self.buf[-1]
            else:
                self.buf[0] = self.opBuf[0] + str(self.buf[0])
                self.opBuf[0] = ''

        # work for
        elif self.type == 'Logic':
            if not self.buf[0] == self.buf[1]:
                self.buf[0] = False
            else:
                self.buf[0] = True
            # decale
            del self.opBuf[-1]
            del self.buf[-1]

        elif len(self.buf) > 1:
            print(self.type)
            print(self.buf)
            print(self.opBuf)
            raise Exception("Can't compute")

    # on decale tout
    def Push(self, value, op):

        if len(self.buf) > 1:
            self.Compute()

        self.buf.append(value)
        self.opBuf.append(op)
        return

    def SpecialStr(self, value):
        if CheckType(value) == 'Numeric':
            return str(value)
        if value == None:
            return 'Undefined'
        if value == True:
            return 'true'
        if value == False:
            return 'false'
        if type(value) in [list]:
            convert_first_to_generator = (str(w) for w in value)
            return ','.join(convert_first_to_generator)
        if type(value) in [dict]:
            return '[object Object]'
        if CheckType(value) == 'Fonction':
            return value.ToStr()

        return str(value)

    # ok all finished, force compute
    def GetBuffer(self):

        # Force compute
        self.Compute()
        while len(self.buf) > 1:
            self.Compute()

        if self.type == 'Logic':
            return self.buf[0]

        if self.type == 'Numeric':
            return self.SafeEval(self.buf[0])

        if self.type == 'Bool':
            if self.SafeEval(self.buf[0].replace('True', '1').replace('False', '0')):
                return True
            else:
                return False

        if self.type == None:
            return ''

        return self.buf[0]

    # WARNING : Take care if you edit this function, eval is realy unsafe.
    # better to use ast.literal_eval() but not implemented before python 3
    def SafeEval(self, str):
        if not str:
            raise Exception('Nothing to eval')
        f = re.search('[^0-9+-.\(\)<>=&%!*\^\/]', str)
        if f:
            raise Exception('Wrong parameter to Eval : ' + str)
            return 0
        str = str.replace('!', 'not ')
        # str = str.replace('=', '==')
        # print('>>' + str)
        return eval(str)


class fonction(object):
    def __init__(self, name, param, data, c=False):
        self.name = name
        self.code = data
        self.param = param
        self.const = c

    def ToStr(self):
        return 'function ' + self.name + '(' + str(self.param)[1:-1] + ') {' + self.code + '}'


class Hack(object):
    def __init__(self, var):
        self.var = var

    def text(self):
        return self.var


class JsParserHelper1(object):
    def __init__(self, tmp_var):
        self.reset()
        self.used = False
        self.Tmp_var = tmp_var
        self.op = None

    def reset(self):
        type = None
        self.name = None
        self.t = None
        self.arg = None
        self.rest_code = ''
        # self.op = None
        self.eval = False
        self.property = False

    def process(self, JScode):

        # IDK why ?
        if self.op:
            return False
        self.reset()
        self.at1 = None

        # If already started
        if JScode.startswith(self.Tmp_var):
            self.name = self.Tmp_var
        else:
            # si on a rien encore trouve on recherche une variable/fonction
            r = re.search('^(\w[\w]*)', JScode)
            if r and not self.used:
                self.name = r.group(1)
            else:
                return False

        self.used = True

        # By defaut
        self.t = 'var'
        JScode = JScode[(len(self.name)):]

        c, p = GetNextUsefullchar(JScode)
        while (c in '.[') and c and not self.at1:
            JScode = JScode[p:]
            if c == '[':
                a = GetItemAlone(JScode, ']')
                JScode = JScode[(len(a)):]
                self.at1 = a[1:-1]
                self.eval = True
            if c == '.':
                a = GetItemAlone(JScode[1:], '[(.\/*-+{}<>|=~^%!')
                JScode = JScode[(len(a)+1):]
                self.at1 = a
                self.property = True

            c, p = GetNextUsefullchar(JScode)

        if c == '(':
            a = GetItemAlone(JScode, ')')
            JScode = JScode[(len(a)):]
            self.arg = a[1:-1]
            self.t = 'fct'

        # operation ?
        if not self.t == 'fct':
            m = re.search('^(' + REG_OP + '|\[|$)', JScode, re.UNICODE)
            if m and JScode:
                self.op = m.group(1).strip()
                if self.op == '[':
                    self.op = None
                else:
                    # prb because the only possible case  is ==
                    if len(self.op) > 1 and self.op[0] == '=' and not self.op[1] == '=':
                        self.op = self.op[0]

                    JScode = JScode[(len(self.op)):]

        if self.t == 'fct':
            out('Fonction :' + self.name + ' method: ' + str(self.at1) + ' arg: ' + self.arg)
        elif self.t == 'var':
            if self.property:
                self.at1 = '"' + self.at1 + '"'
            out('Variable :' + self.name + ' []= ' + str(self.at1) )
            # Exit if nothing to process
            if (self.name == self.Tmp_var) and not self.at1 and not self.op:
                return False
        if self.op:
            out('operation :' + self.name + ' []= ' + str(self.at1) + ' op: ' + str(self.op) )

        self.rest_code = JScode

        return True


class JsParser(object):
    def __init__(self):
        self.Unicode = False
        self.HackVars = []
        self.debug = False
        self.LastEval = ''
        self.SpecialOption = ''
        self.Return = False
        self.ReturnValue = None
        self.Break = False
        self.continu = False
        self.FastEval_vars = []
        self.FastEval_recur = 0
        self.option_ForceTest = False

    def SetReturn(self, r, v):
        self.Return = True
        self.RecursionReturn = r
        self.ReturnValue = v

    def SetOption(self, option):
        if option == 'ForceTest':
            self.option_ForceTest = True

    def AddHackVar(self, name, value):
        self.HackVars.append((name, value))

    def GetVarHack(self, name):
        return self.GetVar(self.HackVars, name)

    def PrintVar(self, vars):
        for i, j in vars:
            print(i + ' : ' + str(j))

    # Need to take care at chain var with " and '
    def ExtractFirstchain(self, string):

        # print(string.encode('ascii', 'replace'))

        if not len(string.strip()):
            return '', 0

        l = len(string)
        string = string + ' '  # To prevent index out of range, hack

        i = -1
        p = 0      # parenthese
        a = 0      # accolade
        b = 0      # bracket
        f = False  # fonction ?
        r = False  # Regex
        com1 = False
        com2 = False
        prev = ''  # previous char
        c1 = 0     # string with "
        c2 = 0     # string with '

        stringR = ''

        while l > i:

            i += 1

            # ignore comment
            if string[i:(i+2)] == '/*':
                com1 = True
            if com1:
                if string[i:(i+2)] == '*/':
                    com1 = False
                    i += 1
                continue
            if string[i:(i+2)] == '//' and not r:
                com2 = True
            if com2:
                if string[i] == '\n':
                    com2 = False
                else:
                    continue

            ch = string[i]

            # if ch == '"' and not GetPrevchar(string,i) == '\\' and not c2:
            if ch == '"' and not c2:
                c1 = 1 - c1
            if ch == "'" and not c1:
                c2 = 1 - c2

            # if we are in a chain no more thing to do than waiting for end
            if c1 or c2:
                stringR = stringR + ch
                continue

            if ch == '(':
                p += 1
            if ch == ')':
                p -= 1
            if ch == '{':
                a += 1
            if ch == '}':
                a -= 1
            if ch == '[':
                b += 1
            if ch == ']':
                b -= 1
            if r and ch == '/':
                r = False
            if ch == '/' and prev == '=':
                r = True

            # vire espace inutile
            if ch.isspace() and not c1 and not c2:
                if not(prev in ALPHA and GetNextchar(string, i) in ALPHA):
                    continue

            stringR = stringR + ch

            # memorise last char
            if not ch.isspace():
                prev = ch

            # Dans tout les cas les parenthses doivent etre fermees, ainsi que les crochet
            if not p and not b:
                # Si on rencontre un ; par defaut
                if (ch == ';') and not f:
                    # Ok, accolade fermees aussi, c'est tout bon
                    if not a:
                        return stringR, i
                    # Accoloade non fermee, c'est une fonction
                    else:
                        f = True
                # si c'est une fonction et l'accolade fermee
                if f and not a:

                    # quel est le caractere suivant ?
                    j = i + 1
                    while (string[j].isspace()) and (l > j):
                        j += 1
                    # Si parenthese on repart
                    if string[j] == '(':
                        continue

                    # Mal formated string ?
                    # Sometime, coder forget the last ; before the }
                    # Desactived for the moment, because can bug in 'a = {};'
                    if False:
                        j = -2
                        while (stringR[j].isspace()) or (stringR[j] == '}'):
                            j -= 1
                        if not (stringR[j] == ';'):
                            j += 1
                            stringR = stringR[:j] + ';' + stringR[j:]

                    # if there is a last ; add it
                    if string[i+1] == ';':
                        stringR = stringR + ';'
                        i += 1

                    return stringR, i

        # chaine bugguée ?
        if ';' not in string:
            # out('ERROR Extract chain without ";" > ' + string)
            return string.rstrip() + ';', i

        raise Exception("Can't extract chain " + string)

    # Everything Without a "Real" is False
    def CheckTrueFalse(self, string):
        # out('> Check True or false : ' + str(string))

        if isinstance(string, bool):
            if string == True:
                return True
        elif isinstance(string, types.StringTypes):
            if not string == '':
                return True
        if isinstance(string, (int, long, float)):
            if not (string == 0):
                return True
        if isinstance(string, (list, tuple)):
            if not (string == []):
                return True
        return False

    # Syntax > aaaaaa.bbbbbb(cccccc) ou bbbb(cccc) ou "aaaa".bb(ccc) ou aa[bb](cc)
    def FonctionParser(self, vars, allow_recursion, name, function, arg2, JScode):

        arg = arg2.strip()

        out('fonction > Name: ' + Ustr(name) + ' arg: ' + Ustr(arg) + ' function: ' + Ustr(function))

        # hack ?
        if isinstance(name, Hack):
            a = MySplit(arg, ',', True)

            # In this case function = text but useless ATM

            if a:
                # ecriture
                vv = self.evalJS(a[0], vars, allow_recursion)
                self.AddHackVar(name.var, vv)
                return vv, JScode
            else:
                # lecture
                vv = self.GetVarHack(name.var)
                out('Hack vars (set): ' + vv)
                return vv, JScode

        # Definite function ?
        fe = self.IsFunc(vars, function)
        if not fe:
            try:
                fe = self.IsFunc(vars, '%s["%s"]' % (name, function))
            except:
                pass

        if fe:

            if fe == '$':
                a = MySplit(arg, ',', True)
                vv = self.evalJS(a[0], vars, allow_recursion)
                fff = Hack(vv)

                return fff, JScode

            elif isinstance(fe, types.MethodType):
                # print(fe.im_func.__name__)  # parseint
                # print(fe.im_class.__name__)  # Basic
                function = fe.im_func.__name__
                out("> function (native): " + function + ' arg=' + arg)
                # and continu with native fonction

            elif isinstance(fe, fonction):
                out('> fonction definie par code : ' + function)
                n, p, c, ct = fe.name, fe.param, fe.code, fe.const
                a = MySplit(arg, ',', True)
                a2 = []
                # out('code de la fonction : ' + c)

                if ct:
                    out('constructor mode')
                    # hack
                    # Make replacement
                    JScode = "%s(%s)%s" % (n, arg, JScode) + ';'

                    NewEval = self.Parse(JScode, vars, allow_recursion)
                    return NewEval, ''

                for i in a:
                    vv = self.evalJS(i, vars, allow_recursion)
                    a2.append(RemoveGuil(vv))

                List_tmpvar = []
                if (len(p) > 0) and (len(a2) > 0):
                    nv = tuple(zip(p, a2))
                    for z, w in nv:
                        self.SetVar(vars, z, w)
                        List_tmpvar.append(z)

                jjj = self.Parse(c, vars, allow_recursion)

                # And delete tmp var
                for i in List_tmpvar:
                    self.InitVar(vars, i)

                if self.Return:
                    self.Return = None

                # return jjj, JScode
                return self.ReturnValue, JScode

            else:
                raise Exception("Strnage fonction")

        # Native fonction
        # http://stackoverflow.com/questions/1091259/how-to-test-if-a-class-attribute-is-an-instance-method
        s = ''
        if type(name) in [list, tuple, dict, types.MethodType, NoneType]:
            s = name
        else:
            if name.startswith('"') or name.startswith("'"):
                s = RemoveGuil(name)
            else:
                if self.IsVar(vars, name):
                    s = self.GetVar(vars, name)
                else:
                    s = name

        for lib in List_Lib:
            if hasattr(lib, function):
                if not function == 'eval':
                    arg = MySplit(arg, ',')
                    for i in range(len(arg)):
                        arg[i] = self.evalJS(arg[i], vars, allow_recursion)

                # for fastcall
                self.FastEval_vars = vars
                self.FastEval_recur = allow_recursion

                cls = lib(self, s)

                r = getattr(cls, function)(arg)

                # set new value if changed
                if hasattr(lib, 'Get'):
                    NV = getattr(cls, 'Get')()
                    if not NV == s:
                        self.SetVar(vars, name, NV)

                return r, JScode

        # test, if all is ok, never reached
        if False:
            # function
            if function == 'function':
                pos9 = len(JScode)
                v = self.MemFonction(vars, '', arg, False, JScode)[2]
                JScode = JScode[pos9:]
                return v, JScode

        # constructor
        if function == 'Function':
            NewCode = RemoveGuil(arg) + ';'

            v = self.MemFonction(vars, '', '', False, '{' + NewCode + '}')[2]
            JScode = v + JScode

            NewEval = self.Parse(JScode, vars, allow_recursion)
            return NewEval, ''

        self.PrintVar(vars)
        raise Exception('Unknow fonction : ' + function)

    def Fast_Eval(self, strg):
        r = self.evalJS(strg, self.FastEval_vars, self.FastEval_recur)
        return r

    def VarParser(self, vars, allow_recursion, variable, op, JScode):

        New_Var = False

        out('Variable : ' + str(variable) + '  operator : ' + op)

        # if it's a creation/modification
        if op == '=':

            out('creation/modification')

            v1 = GetItemAlone(JScode, ',')
            JScode = JScode[(len(v1)):]

            v1 = v1.strip()

            self.VarManage(allow_recursion, vars, variable, v1)

            # and return it
            r = self.GetVar(vars, variable)
            return r, JScode

        if not self.IsVar(vars, variable):
            raise Exception("Cannot find var " + str(variable))

        r = self.GetVar(vars, variable)

        # Only modification
        if len(op) == 2:

            # just put var because not managed here
            if op[0] in '=!':
                return r, op + JScode

            # ok so what is it ?
            out('> var ' + variable + '=' + str(r))

            # check if it's i++ ou i -- form
            if op == '++':
                self.SetVar(vars, variable, r + 1)
                return r, JScode

            elif op == '--':
                self.SetVar(vars, variable, r-1)
                return r, JScode

            # a += 1 form
            elif op[1] == '=' and op[0] in '+-*/%^':
                n = GetItemAlone(JScode, ';,')
                out('A rajouter ' + n)
                r = self.evalJS(variable + op[0] + n, vars, allow_recursion)
                # self.SetVar(vars, variable, r)

                if isinstance(r, (int, long, float)):
                    self.VarManage(allow_recursion, vars, variable, str(r))
                if isinstance(r, str):
                    self.VarManage(allow_recursion, vars, variable, '"' + r + '"')
                else:
                    self.VarManage(allow_recursion, vars, variable, str(r))

                JScode = JScode[(len(n)):]
                return r, JScode

        # just var
        # re-ad op if not used
        JScode = op + JScode
        return r, JScode

    def evalJS(self, JScode, vars, allow_recursion):

        if allow_recursion < 0:
            raise Exception('Recursion limit reached')

        allow_recursion -= 1

        # plus que la chaine a evaluer
        JScode = JScode.strip()

        out('-------------')
        out(str(allow_recursion) + ' : A evaluer >' + JScode + '<\n')

        # ********************************************************

        InterpretedCode = JSBuffer()

        while len(JScode) > 0:
            c = JScode[0]

            # print('InterpretedCode > ' + InterpretedCode)
            out('JScode > ' + JScode.encode('ascii', 'replace') + '\n')

            # parentheses
            if c == '(':

                c2 = GetItemAlone(JScode, ')')[1:-1]
                pos2 = len(c2) + 2
                JScode = JScode[pos2:]

                v = self.evalJS(c2, vars, allow_recursion)
                self.SetVar(vars, 'TEMPORARY_VARS' + str(allow_recursion), v)
                JScode = 'TEMPORARY_VARS' + str(allow_recursion) + JScode

            # remove "useless" code
            if JScode.startswith('new '):
                JScode = JScode[4:]
                continue

            # in operator
            if JScode[0:2] == 'in':
                A = InterpretedCode.GetPrevious()
                B = GetItemAlone(JScode[2:], ',;&|')
                B2 = self.evalJS(B, vars, allow_recursion)

                if type(B2) in [types.MethodType, types.InstanceType]:
                    B2 = str(B2)

                if A in B2:
                    InterpretedCode.AddValue(True)
                else:
                    InterpretedCode.AddValue(False)
                JScode = JScode[(len(B) + 2):]
                continue

            # Special value
            m = re.search('^(true|false|null|String)', JScode, re.UNICODE)
            if m:
                v = m.group(1)
                JScode = JScode[len(v):]

                if v == 'true':
                    InterpretedCode.AddValue(True)
                if v == 'false':
                    InterpretedCode.AddValue(False)
                if v == 'null':
                    InterpretedCode.AddValue(None)
                if v == 'String':
                    self.SetVar(vars, 'TEMPORARY_VARS ' + str(allow_recursion), '')
                    JScode = 'TEMPORARY_VARS' + str(allow_recursion) + JScode
                # if v == 'Array':
                #     InterpretedCode.AddValue([])

                continue

            # hackVars
            r = re.search('^\$\("#([\w]+)"\)\.text\(\)', JScode)
            if r:
                InterpretedCode.AddValue(self.GetVar(self.HackVars, r.group(1)))
                JScode = JScode[(r.end()):]
                continue

            if JScode[0] == '$':
                InterpretedCode.AddValue('$')
                JScode = JScode[1:]
                continue

            # new function delcaration ? Need to be before the fonction/variable parser.
            # var x = function (a, b) {return a * b};
            # function myFunction(a, b) {return a * b};
            if JScode.startswith('function'):
                m = re.search(r'^function(?: ([\w]+))* *\(([^\)]*)\) *{', JScode, re.DOTALL)
                if m:
                    name = ''
                    openparenthesis = False
                    if m.group(1):
                        name = m.group(1)

                    replac, pos3, v = self.MemFonction(vars, name, m.group(2), openparenthesis, JScode)
                    JScode = replac
                    InterpretedCode.AddValue(v)
                    continue

            # pointeur vers fonction ?
            if hasattr(Basic, JScode):
                fm = getattr(Basic(self, None), JScode)
                InterpretedCode.AddValue(fm)
                JScode = ''
                continue

            # 3 - numeric chain
            r = re.search('(^(?:0x)*[0-9]+)', JScode)
            if r:
                v = JScode[0:r.end()]
                if v.startswith('0x'):
                    v = int(v, 0)
                else:
                    v = int(v)
                InterpretedCode.AddValue(v)
                JScode = JScode[(r.end()):]
                continue  # for this one continue directly

            # 4 - Regex
            r = re.search('^\/.*\/(.*$)', JScode)
            if r:
                reg = r.group(0)
                flag = r.group(1)
                # test if the regex is valid
                if flag:
                    for i in flag:
                        if i not in 'gimuy':
                            reg = None
                            break
                InterpretedCode.AddValue(reg)
                JScode = JScode[(len(r.group(0))):]
                continue  # return directly

            # 1 - Array / method
            if c == '[':
                c2 = GetItemAlone(JScode, ']')[1:-1]
                pos2 = len(c2) + 2
                # v = self.evalJS(c2,vars,allow_recursion)

                # all this part is managed away but not for some rare case.
                A = InterpretedCode.GetPrevious()
                if not A:
                    valueT = MySplit(c2, ',', True)
                    JScode = JScode[pos2:]
                    InterpretedCode.AddValue(valueT)
                    continue

                # other case
                self.SetVar(vars, 'TEMPORARY_VARS' + str(allow_recursion), A)
                JScode = 'TEMPORARY_VARS' + str(allow_recursion) + JScode

            # 2 - Alpha chain
            elif c == '"' or c == "'":

                ee = GetItemAlone(JScode, c)
                e = len(ee)
                vv = ee[1:-1]

                # raw string cannot end in a single backslash
                # if vv[-1:] == '\\' and  not vv[-2:-1] == '\\':
                #     vv = vv + '\\'

                # warning with this function
                # if not vv.endswith('\\'):
                #     vv = vv.decode('string-escape')

                JScode = JScode[e:]

                # to be faster
                if len(JScode) == 0:
                    InterpretedCode.AddValue(vv)
                    continue
                # normal way
                else:
                    self.SetVar(vars, 'TEMPORARY_VARS' + str(allow_recursion), vv)
                    JScode = 'TEMPORARY_VARS' + str(allow_recursion) + JScode

            item = ''
            # 5 Variable/fonction/object
            P1 = JsParserHelper1('TEMPORARY_VARS' + str(allow_recursion))
            while P1.process(JScode):
                JScode = P1.rest_code
                r = None

                if P1.t == 'var':

                    # special vars
                    if P1.name == 'window' and P1.at1:
                        P1.name = RemoveGuil(P1.at1)
                        P1.at1 = ''

                    Var_string = P1.name
                    if P1.at1:
                        Var_string = "%s[%s]" % (P1.name, str(P1.at1))

                    # operation / creation ?
                    if P1.op:
                        out('creation/modification ' + Var_string + ' ' + P1.op)
                        r, JScode = self.VarParser(vars, allow_recursion, Var_string, P1.op, JScode)

                    else:
                        if not self.IsVar(vars, P1.name):
                            self.PrintVar(vars)
                            raise Exception('Variable error : ' + P1.name)

                        r = self.GetVar(vars, Var_string)

                elif P1.t == 'fct':
                    if P1.at1:
                        fonction = P1.at1
                        name = P1.name
                    else:
                        fonction = P1.name
                        name = ''
                    if P1.eval:
                        fonction = self.evalJS(fonction, vars, allow_recursion)

                    # hack, devrait etre acive tout le temps
                    if 'TEMPORARY_VARS' in name:
                        name = self.evalJS(name, vars, allow_recursion)

                    gg = fonction + '***' + P1.arg + '**' + JScode
                    r, JScode = self.FonctionParser(vars, allow_recursion, name, fonction, P1.arg, JScode)

                # to speed up
                if not JScode:
                    # It speed up but cause some TEMPORARY_VARS stay in code.
                    InterpretedCode.AddValue(r)
                    continue
                # normal way
                else:
                    self.SetVar(vars, 'TEMPORARY_VARS' + str(allow_recursion), r)
                    JScode = 'TEMPORARY_VARS' + str(allow_recursion) + JScode

            # after this part, all TEMPORARY_VARS need to be removed
            if JScode.startswith('TEMPORARY_VARS' + str(allow_recursion)):
                r = self.GetVar(vars, 'TEMPORARY_VARS' + str(allow_recursion))
                self.InitVar(vars, 'TEMPORARY_VARS' + str(allow_recursion))
                JScode = JScode[(len('TEMPORARY_VARS' + str(allow_recursion))):]
                InterpretedCode.AddValue(r)
                continue
            if P1.used:
                continue

            # --var method, HACK
            if JScode[0:2] == '--' or JScode[0:2] == '++':
                m = re.search('^(\({0,1}\w[\w\.]*\){0,1} *(?:\[[^\]]+\])* *)(' + REG_OP + '|\[|$)', JScode[2:], re.UNICODE)
                if m:
                    l = len(m.group(1))
                    JScode = m.group(1) + JScode[0:2] + JScode[(l+2):]
                    continue
                else:
                    bb(mm)

            # Space to remove
            if c == ' ' or c == '\n':
                JScode = JScode[1:]
                continue

            # Escape char
            if c == '\\':
                JScode = JScode[1:]
                continue

            # Special if (A)?(B):(C)
            if c == '?':
                out(" ****** Special if 1 ********* ")
                # need to find all part
                A = InterpretedCode.GetPrevious()
                B = GetItemAlone(JScode, ':')
                C = GetItemAlone(JScode[(len(B) + 1):])

                Totlen = len(B) + len(C) + 2
                B = B[1:]
                if B.startswith('('):
                    B = B[1:-1]
                if C.startswith('('):
                    C = C[1:-1]
                if A:
                    r = self.evalJS(B, vars, allow_recursion)
                else:
                    r = self.evalJS(C, vars, allow_recursion)

                InterpretedCode.AddValue(r)
                JScode = JScode[Totlen:]
                continue

            # Short-circuiting evaluations
            if JScode[0:2] == '&&' or JScode[0:2] == '||':
                out(" ****** Short-circuiting  ********* ")
                A = InterpretedCode.GetPrevious()
                B = GetItemAlone(JScode[2:])

                Totlen = len(B) + 2
                if B.startswith('('):
                    B = B[1:-1]

                # for && if the first operand evaluates to false, the second operand is never evaluated
                if JScode[0:2] == '&&':
                    if A:
                        r = self.evalJS(B, vars, allow_recursion)
                        InterpretedCode.AddValue(r)
                    else:
                        InterpretedCode.AddValue(A)
                # for || if the result of the first operand is true, the second operand is never operated
                if JScode[0:2] == '||':
                    if not A:
                        r = self.evalJS(B, vars, allow_recursion)
                        InterpretedCode.AddValue(r)
                    else:
                        InterpretedCode.AddValue(A)

                JScode = JScode[Totlen:]
                continue

            # Operation
            if c in '+<>-*/=&%|!^.':
                InterpretedCode.SetOp(c)
                JScode = JScode[1:]
                continue

            # No sure how to put this
            if JScode == '{}':
                InterpretedCode.AddValue({})
                JScode = JScode[2:]
                continue
            if JScode == '[]':
                InterpretedCode.AddValue([])
                JScode = JScode[2:]
                continue

            # ???
            if JScode == ';':
                JScode = JScode[1:]
                continue

            # comma
            if c == ',':
                InterpretedCode.GetPrevious()
                JScode = JScode[1:]
                continue

            # Not found part
            # We will make another turn
            self.PrintVar(vars)
            out("Can't eval string :" + JScode)
            out('Last eval : ' + str(self.LastEval))

            # print(debug.encode('ascii', 'replace'))
            raise Exception(str(allow_recursion) + " : Cannot Eval chain : " + JScode)

        InterpretedCode2 = InterpretedCode.GetBuffer()

        out(str(allow_recursion) + ' : Evalue > ' + Ustr(InterpretedCode2) + ' type ' + Ustr(type(InterpretedCode2)))
        out('-------------')

        self.LastEval = InterpretedCode2
        return InterpretedCode2

    def InitVar(self, var, variable):
        variable = variable.strip()

        for j in var:
            if j[0] == variable:
                var.remove(j)
                return

    def GetVar(self, var, variable):

        # variable = variable.strip()

        index = None
        if '[' in variable:
            index = GetItemAlone(variable[(variable.find('[')):], ']')
            index = index[1:-1]
            variable = variable.split('[')[0]
            index = self.evalJS(index, var, 50)

        if '.' in variable:
            index = variable.split('.')[1]
            variable = variable.split('.')[0]

        # out('Variable Get ' + variable + ' index :' + str(index))

        for j in var:
            if j[0] == variable:
                k = j[1]
                r = k
                if not (index == None):
                    # Special method
                    if index == 'length':
                        r = len(k)
                        return r
                    if index == 'constructor':
                        return GetConstructor(k)

                    if type(k) in [list, tuple, str]:
                        if CheckType(index) == 'Numeric':
                            if int(index) < len(k):
                                r = k[int(index)]
                            else:
                                r = 'undefined'
                        elif CheckType(index) == 'String':
                            index = RemoveGuil(index)
                            try:
                                r = k[index]
                            except:
                                r = k[int(index)]
                    elif type(k) in [dict]:
                        index = RemoveGuil(index)
                        r = k.get(index)
                    elif type(k) in [type]:
                        r = getattr(k(self, None), index)

                return r

        # search it in hackvar ?
        for j in self.HackVars:
            if j[0] == variable:
                return j[1]

        raise Exception('Variable not defined: ' + str(variable))

    def SetVar(self, var, variable, value, i=None):
        variable = variable.strip()

        # Existing var ?
        for j in var:
            if j[0] == variable:

                if i == None:
                    # vars ?
                    if isinstance(value, types.StringTypes):
                        var[var.index(j)] = (variable, value)
                    # Numeric
                    else:
                        var[var.index(j)] = (variable, value)
                else:
                    # Array
                    if type(var[var.index(j)][1]) in [list, tuple]:

                        Listvalue = var[var.index(j)][1]

                        # ok this place doesn't esist yet
                        l = int(i) - len(Listvalue) + 1
                        while l > 0:
                            Listvalue.append('undefined')
                            l -= 1
                        # Now modify it
                        if type(value) in [list, tuple]:
                            Listvalue = value
                        else:
                            Listvalue[int(i)] = value
                        var[var.index(j)] = (variable, Listvalue)
                    # dictionnary
                    elif type(var[var.index(j)][1]) in [dict]:
                        Listvalue = var[var.index(j)][1]
                        Listvalue[i] = value
                        var[var.index(j)] = (variable, Listvalue)

                return

        # New var
        var.append((variable, value))

    def GetTypeVar(self, var, variable):
        try:
            variable = variable.split('[')[0]
            variable = variable.split('.')[0]
            for j in var:
                if j[0] == variable:
                    return type(j[1])
            return 'Undefined'
        except:
            return 'Undefined'

    def IsVar(self, var, variable, index=None):
        try:
            variable = variable.split('[')[0]
            variable = variable.split('.')[0]
            for j in var:
                if j[0] == variable:
                    if index == None:
                        return True
                    if index in var[var.index(j)][1]:
                        return True

            return False
        except:
            return False

    # Need to use metaclass here
    def IsFunc(self, vars, name):
        bExist = False
        bExist = self.IsVar(vars, name)
        if not bExist:
            return False

        f = self.GetVar(vars, name)
        if f == '$':
            return '$'
        if isinstance(f, fonction):
            return f
        elif isinstance(f, types.MethodType):
            return f
        else:
            return self.IsFunc(vars, f)

    def VarManage(self, allow_recursion, vars, name, value=None):

        index = None
        init = False

        try:
            value = value.strip()
        except:
            pass
        name = name.strip()

        # variable is an object
        if '.' in name:
            if self.GetTypeVar(vars, name) == 'tuple':
                index = name.split('.')[1]
                name = name.split('.')[0]
        # Variable is an array ?
        m = re.search(r'^\({0,1}([\w]+)\){0,1}\[(.+?)\]$', name, re.DOTALL | re.UNICODE)
        if m:
            name = m.group(1)
            index = m.group(2)
            index = self.evalJS(index, vars, allow_recursion)

        if value:
            if isinstance(value, (int, long, float)):
                value = self.evalJS(value, vars, allow_recursion)
            else:
                # Values is an array []
                if value.startswith('[') and value.endswith(']'):
                    value = value[1:-1]

                    # hack
                    if value == '':
                        value = []
                    # normal way
                    else:
                        valueT = MySplit(value, ',')
                        v = []
                        for k in valueT:
                            v2 = self.evalJS(k, vars, allow_recursion)
                            v.append(v2)
                        value = v
                        if index == None:
                            index = 0
                            init = True
                # Values is an array {}
                elif value.startswith('{') and value.endswith('}'):
                    value = value[1:-1]
                    valueT = MySplit(value, ',', True)
                    v = {}
                    for k in valueT:
                        l = k.split(':')
                        # WARNING : no eval here in JS
                        v2g = RemoveGuil(l[0])
                        v2d = self.evalJS(l[1], vars, allow_recursion)
                        v[v2g] = v2d
                    value = v
                    if index == None:
                        index = 0
                        init = True
                # string and other
                else:
                    value = self.evalJS(value, vars, allow_recursion)

        name = name.strip()

        # Output for debug
        if not (index == None):
            out('> Variable in parser => ' + Ustr(name) + '[' + Ustr(index) + ']' + ' = ' + Ustr(value))
        else:
            out('> Variable in parser => ' + Ustr(name) + ' = ' + Ustr(value))

        # chain
        if isinstance(value, types.StringTypes):
            self.SetVar(vars, name, value, index)
        # number
        elif isinstance(value, (int, long, float)):
            self.SetVar(vars, name, value, index)
        # list
        elif type(value) in [list, tuple, dict]:
            if init:
                self.InitVar(vars, name)
            self.SetVar(vars, name, value, index)
        # fonction
        elif isinstance(value, fonction):
            self.SetVar(vars, name, value, index)
        # undefined
        elif value == None:
            self.SetVar(vars, name, None, index)
        else:
            print(type(value))
            raise Exception('> ERROR : Var problem >' + str(value))
        return

    def MemFonction(self, vars, name, parametres, openparenthesis, data):

        if not name:
            n0 = 0
            while self.IsFunc(vars, 'AnonymousFunc' + str(n0)):
                n0 = n0 + 1
            name = 'AnonymousFunc' + str(n0)

        if self.SpecialOption:
            if self.SpecialOption.split('=')[0] == 'Namefunc':
                name = self.SpecialOption.split('=')[1]
            self.SpecialOption = ''

        param = MySplit(parametres, ',', True)

        out('Extract function :' + name + ' ' + str(param))

        pos = 0
        replac = ''

        while not data[0] == '{':
            data = data[1:]

        content = GetItemAlone(data, '}')[1:-1]
        pos2 = len(content) + 1

        fm = fonction(name, param, content.lstrip())
        self.SetVar(vars, name, fm)

        data = data[(pos2 + 1):]

        if openparenthesis:
            c, p = GetNextUsefullchar(data)
            if c == ')':
                data = data[(p + 1):]
                openparenthesis = False

        selfinvoked = False
        if len(data) > 0:
            if data[0] == '(':
                selfinvoked = True

        # self invoked ?
        if selfinvoked:
            paraminvoked = GetItemAlone(data, ')')
            out('Self invoked ' + str(paraminvoked))
            replac = name + paraminvoked

            data = data[(len(paraminvoked)):]

            if openparenthesis:
                c, p = GetNextUsefullchar(data)
                if c == ')':
                    data = data[(p + 1):]
                    openparenthesis = False

        replac = replac + data

        return replac, 0, name

    def Parse(self, JScode, vars, allow_recursion=MAX_RECURSION):

        if allow_recursion < 0:
            raise Exception('Recursion limit reached')

        allow_recursion -= 1

        # ************************
        #    Post traitement
        # ************************
        # Need all functions first, because they can be called first and be at the bottom of the code
        # So we extract all functions first, and replace them by a simple call in the code, if they are self invoked

        # Make this part only if needed
        if 'function' in JScode:
            posG = 0

            while True:

                chain, pos = self.ExtractFirstchain(JScode[posG:])
                if not chain:
                    break

                Startoff = posG
                Endoff = posG + pos + 1
                posG = Endoff

                # skip empty char
                chain = chain.strip()

                # fonction
                m = re.search(r'^(\()* *function(?: ([\w]+))* *\(([^\)]*)\) *{', chain, re.DOTALL)
                if m:
                    name = ''
                    openparenthesis = False
                    if m.group(2):
                        name = m.group(2)
                    if m.group(1):
                        openparenthesis = True

                    replac, pos3, xyz = self.MemFonction(vars, name, m.group(3), openparenthesis, chain)

                    JScode = JScode[:Startoff] + replac + JScode[Endoff:]

                    posG = Startoff + len(replac)

        # ***********************
        # The real Parser
        # **********************

        Parser_return = None

        while True:

            if self.continu:
                break

            chain, pos = self.ExtractFirstchain(JScode)
            if not chain:
                break

            JScode = JScode[(pos + 1):]

            chain = chain.lstrip().rstrip()
            # empty ?
            if chain == ';':
                continue

            out('D++++++++++++++++++')
            out(chain.encode('ascii', 'replace'))
            out('F++++++++++++++++++')

            # hackVars ?
            m = re.search(r'^\$\("#([^"]+)"\)\.text\(([^\)]+)\);', chain)
            if m:
                out('> hack ' + m.group(0) + ' , variable est ' + m.group(1))
                self.SetVar(self.HackVars, m.group(1),self.GetVar(vars, m.group(2)))
                continue

            # break
            if chain.startswith('break'):
                self.Break = True
                return

            # continue
            if chain.startswith('continue'):
                self.continu = True
                return

            # Return ?
            if chain.startswith('return'):
                m = re.match(r'return *;', chain)
                if m:
                    self.Return = True
                    self.ReturnValue = None
                    return None
                m = re.match(r'^return *([^;]+)', chain)
                if m:
                    chain = m.group(1)
                    r = self.evalJS(chain, vars, allow_recursion)
                    self.Return = True
                    self.ReturnValue = r
                    return self.ReturnValue

            # Variable creation/modification ?
            if chain.startswith('var '):
                out('var')

                chain = chain[4:]

                # Now need to extract all vars from chain
                while chain:
                    v1 = GetItemAlone(chain, ',').strip()
                    chain = chain[(len(v1) + 1):]
                    if v1.endswith(',') or v1.endswith(';'):
                        v1 = v1[:-1]
                    self.evalJS(v1, vars, allow_recursion)
                continue

            name = ''
            # Extraction info
            # Problem, catch fonction too :(
            m = re.search(r'^([\w]+) *(\(|\{)', chain, re.DOTALL)
            # Syntax > aaaaa(bbbbb) .........
            if m:
                name = m.group(1)
                sp = m.group(2)
                if sp == '(':
                    arg = GetItemAlone(chain[(m.end()-1):], ')')[1:-1]
                    pos3 = len(arg) + 1

                    code = chain[(m.end() + pos3):]
                elif sp == '{':
                    arg = ''
                    code = chain[(m.end()-1):]
                else:
                    raise Exception('> Er 74')

                out('DEBUG > Name: ' + name + ' arg: ' + arg + ' code: ' + code + '\n')

                # Jquery
                if name == 'DOCUMENT_READY':
                    out('DOCUMENT_READY ' + arg)
                    self.SpecialOption = 'Namefunc=DR'
                    self.Parse(arg, vars, allow_recursion)

                    # It's not the correct place to do that, but for the moment ...
                    self.Parse('DR();', vars, allow_recursion)

                    continue

                # For boucle ?
                if name == 'for':
                    arg = arg.split(';')
                    v = arg[0] + ';'
                    t = arg[1]
                    i = arg[2] + ';'
                    f = code
                    if GetNextUsefullchar(f)[0] == '{':
                        f = GetItemAlone(f, '}')[1:-1]

                    # init var
                    self.Parse(v, vars, allow_recursion)
                    # loop
                    while self.CheckTrueFalse(self.evalJS(t, vars, allow_recursion)):
                        # fonction
                        self.Parse(f, vars, allow_recursion)
                        if self.Break:
                            self.Break = False
                            break
                        # incrementation
                        self.Parse(i, vars, allow_recursion)

                    continue

                # boucle while ?
                if name == 'while':
                    f = code
                    if GetNextUsefullchar(f)[0] == '{':
                        f = GetItemAlone(f, '}')[1:-1]

                    # loop
                    while self.CheckTrueFalse(self.evalJS(arg, vars, allow_recursion)):
                        # fonction
                        self.Parse(f, vars, allow_recursion)
                        if self.Break:
                            self.Break = False
                            break

                        if self.continu:
                            self.continu = False

                    continue

                # boucle do/while
                if name == 'do':
                    f = code
                    e = ''
                    if sp == '{':
                        f = GetItemAlone(f, '}')

                    if f.startswith('{'):
                        f = f[1:-1]

                    # Need to check the while part ?
                    chain2, pos2 = self.ExtractFirstchain(JScode)
                    if 'while' in chain2:
                        chain2 = chain2.lstrip()
                        JScode = JScode[(pos2 + 1):]
                        m2 = re.search(r'while\s*\((.+?)\);$', chain2, re.DOTALL)
                        if m2:
                            e = m2.group(1)

                    if not e:
                        raise Exception('> While error')

                    out('> Boucle do/while : test :' + e + ' code: ' + f)

                    # loop
                    # 1 forced execution because do/while
                    self.Parse(f, vars, allow_recursion)
                    if self.Break:
                        self.Break = False
                        continue  # stop all

                    if self.continu:
                        self.continu = False
                    # and now the loop
                    while self.CheckTrueFalse(self.evalJS(e, vars, allow_recursion)):
                        # fonction
                        self.Parse(f, vars, allow_recursion)
                        if self.Break:
                            self.Break = False
                            break

                        if self.continu:
                            self.continu = False

                    continue
                # boucle switch
                if name == 'switch':
                    v = self.evalJS(arg, vars, allow_recursion)
                    f = code[1:]

                    if v == 'undefined':
                        continue

                    # Search the good case code
                    StrToSearch = "case%s:" % (str(v))

                    while (not f.startswith(StrToSearch)) and (len(f) > 0):
                        tmp_str = GetItemAlone(f, ';}')
                        f = f[(len(tmp_str) + 1):]

                    if len(f) < 1:
                        self.PrintVar(vars)
                        raise Exception("Can't find switch value " + str(v))

                    f = f[(len(StrToSearch)):]

                    self.Parse(f, vars, allow_recursion)

                    continue

                # Boucle if
                if name == 'if':
                    t = arg
                    f = code
                    e = ''

                    if GetNextUsefullchar(f)[0] == '{':
                        f = GetItemAlone(f, '}')[1:-1]

                    # Need to check if there is else statement ?
                    chain2, pos2 = self.ExtractFirstchain(JScode)
                    if 'else' in chain2:
                        chain2 = chain2.lstrip()
                        JScode = JScode[(pos2 + 1):]
                        m2 = re.search(r'else\s*{(.+?)}$', chain2, re.DOTALL)
                        if m2:
                            e = m2.group(1)

                    # hack, need to memorise working test in future
                    if self.option_ForceTest:
                        try:
                            ttt = self.CheckTrueFalse(self.evalJS(t, vars, allow_recursion))
                        except:
                            from random import choice
                            ttt = choice([True, False])
                            # thx to come every day, to help me to find bug on this code

                        if ttt:
                            self.Parse(f, vars, allow_recursion)
                        elif e:
                            self.Parse(e, vars, allow_recursion)
                        continue
                    # normal way
                    else:
                        if self.CheckTrueFalse(self.evalJS(t, vars, allow_recursion)):
                            self.Parse(f, vars, allow_recursion)
                        elif e:
                            self.Parse(e, vars, allow_recursion)
                        continue

                if name == 'with':
                    f = code
                    if GetNextUsefullchar(f)[0] == '{':
                        f = GetItemAlone(f, '}')

                    # list all arg membre.
                    member_list = self.GetVar(vars, arg)

                    out('> With fonction : exp=' + arg + ' values=' + str(member_list))
                    # print('Before: ' + f)
                    # print(member_list)

                    def sub(g):
                        g = g.group()
                        return g[0] + arg + '["' + g[1:-1] + '"]' + g[-1:]

                    # Hack again
                    if type(member_list) in [type]:
                        for i in member_list.__dict__:
                            f = re.sub(r'[^\w]' + str(i) + '[^\w]', sub, f, re.DOTALL)
                    else:
                        for i in member_list:
                            f = re.sub(r'[^\w]' + i + '[^\w]', sub, f, re.DOTALL)

                    # print('after: ' + f)

                    self.Parse(f[1:-1], vars, allow_recursion)
                    # JScode = f[1:-1] + ';' + JScode
                    continue

            # Pas trouve, une fonction ?
            if chain.endswith(';'):
                Parser_return = self.evalJS(chain[:-1], vars, allow_recursion)
                # hack
                # if 'return "ok"' in str(Parser_return):
                #     JScode = str(Parser_return)
                #     continue

            # hack, need to be reenabled
            # Non gere encore
            if not chain.endswith(';'):
                print('> ' + JScode)
                raise Exception('> ERROR : Cannot parse >' + chain)

        return Parser_return

    def ProcessJS(self, JScode, vars=[]):
        vars_return = []

        # unicode ?
        if False:
            out('Unicode convertion')
            JScode = unicode(JScode, 'utf-8')
            self.Unicode = True

        # Special
        vars.append(('Math', Math))

        vars.append(('String', ''))
        vars.append(('document', {'write': 'ok'}))

        # Hack
        JScode = JScode.replace('$(document).ready', 'DOCUMENT_READY')

        # Start the parsing
        ret = self.Parse(JScode, vars)

        # Memorise vars

        return ret


# ---------------------------------------------------------------------------------------------------------------------
# fonctions
#

def toStr(str):
    def decorator(f):
        class _temp:
            def __call__(self, *args, **kwargs):
                return f(self.real_self, *args, **kwargs)

            def __str__(self):
                return str % f.__name__
        return _temp()
    return decorator


class Math(object):
    def __init__(self, initV1, initV2):
        pass

    def max(self, arg):
        t1 = arg[0]
        t2 = arg[1]
        return max(t1, t2)

    def min(self, arg):
        t1 = arg[0]
        t2 = arg[1]
        return min(t1, t2)

    def abs(self, arg):
        return abs(arg[0])

    def pow(self, arg):
        t1 = arg[0]
        t2 = arg[1]
        return pow(t1, t2)

    @toStr('function %s() {\n    [native code]\n}')
    def sin(self, arg):
        return math.sin(arg[0])

    @toStr('function %s() {\n    [native code]\n}')
    def atan(self, arg):
        return math.atan(arg[0])

    def __contains__(self, arg):
        if arg in ['max', 'min', 'abs', 'pow', 'sin', 'atan']:
            return True
        return False


class String(object):
    def __init__(self, initV1, initV2=''):
        self._JSParser = initV1
        self._string = initV2

    def Get(self):
        return self._string

    def charCodeAt(self, arg):
        v = arg[0]
        return ord(self._string[int(v)])

    def length(self, arg):
        return len(self._string)

    def substring(self, arg):
        p1 = arg[0]
        if len(arg) > 1:
            p2 = arg[1]
            return self._string[int(p1): int(p2)]
        else:
            return self._string[int(p1):]

    def replace(self, arg):
        t1 = arg[0]
        t2 = arg[1]

        # if not t1.startswith('/'):
        #     t1 = self.evalJS(t1,vars,allow_recursion)

        # regex mode ? HACK
        if t1.startswith('/'):
            jr = re.findall(t1.split('/')[1], self._string)

            for k in jr:
                if not self._JSParser.IsFunc(self._JSParser.FastEval_vars, t2):
                    self._string = self._string.replace(k, t2)
                    out('Replace (F) ' + str(k) + ' by ' + str(t2))
                else:
                    v = self._JSParser.Fast_Eval(t2 + '(' + k + ')')
                    v = str(v)
                    self._string = self._string.replace(k, v)
                    out('Replace ' + str(k) + ' by ' + str(v))
        # String mode
        else:
            # t1 = self.evalJS(t1, vars, func, allow_recursion)
            self._string = s.replace(t1, t2)
        return self._string

    def fromCharCode(self, arg):
        return chr(int(arg[0]))

    def split(self, arg):
        arg = arg[0].replace('"', '').replace("'", "")
        if arg == '':
            return list(self._string)
        else:
            return self._string.split(arg)

    def indexOf(self, arg):
        start = 0
        if len(arg) > 1:
            start = int(arg[1])
        return self._string.find(arg[0], start)


class Array(object):
    def __init__(self, initV1, initV2=[]):
        self._array = initV2

    def Get(self):
        return self._array

    def join(self, arg):
        t = arg[0].replace('"', '').replace("'", "")
        return t.join(self._array)

    def push(self, arg):
        t1 = arg[0]
        if len(arg) > 1:
            # use s.extend-[array])
            raise Exception('Not implemented - push')
        self._array.append(t1)

        v = len(self._array)
        return v

    def slice(self, arg):
        p1 = arg[0]
        if len(arg) > 1:
            p2 = arg[1]
            sr = self._array[int(p1):int(p2)]
        else:
            sr = self._array[int(p1):]
        sr = '"' + sr + '"'
        return sr

    def splice(self, arg):
        t1 = arg[0]
        t2 = arg[1]
        if len(arg) > 2:
            raise Exception('Not implemented - splice')
        tab = self._array[:t1] + self._array[(t1 + t2):]
        tabsup = self._array[t1:(t1 + t2)]

        self._array = tab
        return tabsup

    def shift(self, arg):
        if len(self._array) == 0:
            return None
        return self._array.pop(0)


class Basic(object):
    def __init__(self, initV1, initV2):
        self._JSParser = initV1
        self._name = initV2
        pass

    def Setting(self, vars):
        self._vars = vars

    def parseInt(self, arg):
        t1 = arg[0]
        t2 = arg[1]
        if t1 == '':
            return None
        r = int(t1, int(t2))
        return r

    def typeof(self, arg):
        return type(arg)

    def debug(self, arg):
        print('------------------------------------')
        self._JSParser.PrintVar(self._JSParser.FastEval_vars)
        print('------------------------------------')
        raise Exception('DEBUG')
        return

    def eval(self, arg):
        out('To eval >' + arg)
        r = self._JSParser.Parse(RemoveGuil(arg), self._JSParser.FastEval_vars, self._JSParser.FastEval_recur)
        return r

    def Array(self, arg):
        if arg[0]:
            if isinstance(arg[0], (int, long)):
                return []
            return arg
        return []

    def alert(self, arg):
        # logwrite(str(arg))
        print('------------ALERT-------------------')
        print(arg)
        print('------------------------------------')
        return ''

    def RegExp(self, arg):
        t1 = RemoveGuil(arg[0])
        t2 = RemoveGuil(arg[1])
        return '/' + t1 + '/' + t2

    # this fonction if for object normaly
    def toString(self, arg):
        t1 = arg[0]
        try:
            f = self._name.im_func.__name__
        except:
            f = "HACK'"
        t = 'function %s() {\n    [native code]\n}' % f
        return t


List_Lib = [Basic, Array, String, Math]
