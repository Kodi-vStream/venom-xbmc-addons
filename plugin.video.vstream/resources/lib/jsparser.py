#coding: utf-8
#
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#

#******************************
#   A Basic Javascript parser
#******************************

# TODO LIST
# ---------
# Regex will work only for normal name, not for exotic name
# Object
# Globla/Local variables/function/object

#help
#https://sarfraznawaz.wordpress.com/2012/01/26/javascript-self-invoking-functions/

import re
import types
import time

REG_NAME = '[\w]+'
REG_OP = '[\/*-+\(\)\{\}\[\]<>]+'

JScode2 ="""
eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('(0(){4 1="5 6 7 8";0 2(3){9(3)}2(1)})();',10,10,'function|b|something|a|var|some|sample|packed|code|alert'.split('|'),0,{}));
"""


JScode ="""
var t = 78;
$(document).ready(function() {
    var y = $("#aQydkd1Gbfx").text();
    var x = $("#aQydkd1Gbf").text();
    var s = [];
    for (var i = 0; i < y.length; i++) {
        var j = y.charCodeAt(i);
        if ((j >= 33) && (j <= 126)) {
            s[i] = String.fromCharCode(33 + ((j + 14) % 94));
        } else {
            s[i] = String.fromCharCode(j);
        }
    }
    var tmp = s.join("");
    var str = tmp.substring(0, tmp.length - _CoRPE1bSt9()) + String.fromCharCode(tmp.slice(0 - _CoRPE1bSt9()).charCodeAt(0) + _0oN0h2PZmC()) + tmp.substring(tmp.length - _CoRPE1bSt9() + 1);
    $("#streamurl").text(str);
});

function nWuEkcMO4z() {
    return 2 + 1;
}

function _CoRPE1bSt9() {
    return nWuEkcMO4z() + 1478067443 - 1478067445;
}

function _0oN0h2PZmC() {
    return _CoRPE1bSt9() - _7L9xjpbs4N();
}

function _7L9xjpbs4N() {
    return -2;
}
"""
def out(string):
    print str(string)


class JsParser(object):
    def __init__(self):
        self.Jquery = ''
        self.HackVars = []
        self.debug = False
        self.LastEval = ''
    
    def AddHackVar(self,name, value):
        self.HackVars.append((name,value))
        
    def GetVarHack(self,name):
        return self.GetVar(self.HackVars,name)
    
    #Need to take care at chain var with " and '
    def ExtractFirstchain(self,string):
        if len(string.strip()) == 0:
            return '',0
    
        l = len(string)
        string = string + ' ' #To prevent index out of range, hack
        
        i = 0
        p = 0 #parenbthese
        a = 0 #accolade
        f = False #fonction ?
        while (l > i):
            ch = string[i]
            if ch == '(':
                p = p + 1
            if ch == ')':
                p = p - 1
            if ch == '{':
                a = a + 1
            if ch == '}':
                a = a - 1
            #Dans tout les cas les parenthses doivent etre fermees
            if (p == 0):
                #Si on rencontre un ; par defaut
                if (ch == ';') and not (f):
                    #Ok, accolade fermees aussi, c'est tout bon
                    if(a == 0):
                        i = i + 1
                        return string[:i],i
                    #Accoloade non fermee, c'est une fonction
                    else:
                        f = True
                #si c'est une fonction et l'accolade fermee
                if (f) and (a == 0):
                    #quel est le caractere suivant ?
                    i = i + 1
                    while (string[i] == ' ') and(l > i):
                        i = i + 1
                    #on repart
                    if string[i] == '(':
                        continue
                    
                    #hack
                    if string[i] == ';':
                        i = i + 1
                        
                    return string[:i],i            
            i = i + 1
        
        #chaine bugguée ?
        if ';' not in string:
            out('ERROR Extract chain without ;')
            return self.ExtractFirstchain(string + ';')
            
        raise Exception("Can't extract chain " + string)
           
    def GetBeetweenParenth(self,str):
        #Search the first (
        s = str.find('(')
        if s == -1:
            return ''
            
        n = 1
        e = s + 1
        while (n > 0) and (e < len(str)):
            c = str[e]
            if c == '(':
                n = n + 1
            if c == ')':
                n = n - 1
            e = e + 1
            
        s = s + 1
        e = e - 1
        return e,str[s:e]
        
    def GetBeetweenCroch(self,str):
        #Search the first (
        s = str.find('{')
        if s == -1:
            return ''
            
        n = 1
        e = s + 1
        while (n > 0) and (e < len(str)):
            c = str[e]
            if c == '{':
                n = n + 1
            if c == '}':
                n = n - 1
            e = e + 1
            
        s = s + 1
        e = e - 1
        return e,str[s:e]

    #WARNING : Take care if you edit this function, eval is realy unsafe.
    #better to use ast.literal_eval() but not implemented before python 3
    def SafeEval(self,str):
        f = re.search('[^0-9+-.\(\)<>=&%]',str)
        if f:
            out ('Wrong parameter to Eval : ' + str)
            return 0
        #out('SafeEval : ' + str)
        return eval(str)
        
    def AlphaConcat(self,string):
        #if string.startswith('"'):
        #    string = string[1:]
        #if string.endswith('"'):
        #    string = string[:-1]
        string =string.replace('"+"','')  
        return string
        
    def evalJS(self,JScode,vars,func,allow_recursion):
    
        if allow_recursion < 0:
            raise Exception('Recursion limit reached')
            
        allow_recursion = allow_recursion - 1
    
        #https://nemisj.com/python-api-javascript/

        #plus que la chaine a evaluer
        JScode = JScode.replace(' ','')
        
        debug = JScode
        

        out( '-------------')
        out( 'A evaluer >'+ JScode)
            
        #********************************************************
        
        InterpretedCode = ''
        
        while (len(JScode)>0):
            c = JScode[0]
            
            #print 'InterpretedCode > ' + InterpretedCode
            #print 'JScode > ' + JScode

            #Alpha chain
            if c == '"':
                e = JScode[1:].find('"') + 2
                if e == 1:
                    raise Exception("Can't eval chain " + JScode)
                InterpretedCode = InterpretedCode + JScode[0:e]
                JScode = JScode[(e):]
                continue
            if c == "'":
                e = JScode[1:].find("'")
                if e == -1:
                    raise Exception("Can't eval chain " + JScode)
                InterpretedCode = InterpretedCode + JScode[0:e]
                JScode = JScode[(e+1):]
                continue
            #numeric chain
            r = re.search('(^[0-9]+)',JScode)
            if r:
                InterpretedCode = InterpretedCode + JScode[0:r.end()]
                JScode = JScode[(r.end()):]
                continue
            #parentheses
            if c == "(":
                c2 = self.GetBeetweenParenth(JScode)[1]
                v = self.evalJS(c2,vars,func,allow_recursion)
                InterpretedCode = InterpretedCode + v
                JScode = JScode[(len(c2) + 2):]
                continue
                
            #hack
            r = re.search('^\$\("#([\w]+)"\)\.text\(\)',JScode)
            if r:
                InterpretedCode = InterpretedCode + self.FormatVarOutput(self.GetVar(self.HackVars,r.group(1)))
                JScode = JScode[(r.end()):]
                continue            
                
            #use precedent result ?
            if c == '.':
                #Make a false var
                self.SetVar(vars,'LAST_RESULT',InterpretedCode)
                #And a small rollback
                JScode = 'LAST_RESULT' + JScode
                InterpretedCode = ''
             
            #fonction ?
            r = re.search('^('+REG_NAME+')\(',JScode)
            if r:
                Func_chain = r.group(0)[:-1]
                
                #need to find all arg
                pos,content = self.GetBeetweenParenth(JScode[(r.end()-1):])
                arg = content.split(',')
                
                out( "> func : " + Func_chain +'(' + content + ')')
                
                #Def function ?
                fe = self.IsFunc(func,r.group(1))
                if fe:
                    n,p,c = fe
                    
                    if (len(p) > 0) and (len(arg)>0):
                        nv = tuple(zip(p, arg))
                        vars.append(nv)

                    v = self.Parse(c,vars,func,allow_recursion)
                    
                    InterpretedCode = InterpretedCode + v
                    JScode = JScode[(len(Func_chain) + len(content) + 2):]
                    continue
                    
                #Native function ?
                
                #error
                print str(func)
                raise Exception("Can't find function " +Func_chain)
                
            #variables
            r = re.search('^(' + REG_NAME + ')(?:' + REG_OP + '|$)',JScode)
            if r:
                print "> var " +r.group(1)
                if self.IsVar(vars,r.group(1)):

                    v = self.FormatVarOutput(self.GetVar(vars,r.group(1)))
                    
                    InterpretedCode = InterpretedCode + v
                    JScode = JScode[(len(r.group(1))):]
                    continue
                    
                raise Exception("Can't find var " + r.group(1))                 
                
            #object ?
            r = re.search('^('+REG_NAME+')\.('+REG_NAME+')',JScode)
            if r:
                object_chain = r.group(0)
                #parentheses ?
                if len(JScode) > len(r.group(0)):
                    if JScode[r.end()] == '(':
                        object_chain = object_chain + '(' + self.GetBeetweenParenth(JScode)[1] + ')'
 
                print "Obj " + object_chain
                
                #Native
                #charCodeAt
                r = re.search('(^[\w]+)\.charCodeAt\((.+)\)$',object_chain)
                if r:
                    s = self.GetVar(vars,r.group(1))
                    #out('CharcodeAt : ' + str(s) + " " + str(r.group(2)))
                    v = self.evalJS(r.group(2),vars,func,allow_recursion)
                    InterpretedCode = InterpretedCode + str(ord(s[int(v)]))
                    JScode = JScode[(len(object_chain)):]
                    continue
                #length
                r = re.search('(^[\w]+)\.length',object_chain)
                if r:
                    s = self.GetVar(vars,r.group(1))
                    InterpretedCode = InterpretedCode + str(len(s))
                    JScode = JScode[(len(object_chain)):]
                    continue
                #Substring
                r = re.search('^(^[\w]+)\.substring\((.+?)(?:,(.+))*\)$',object_chain)
                if r:
                    s = self.GetVar(vars,r.group(1))
                    p1 = self.evalJS(r.group(2),vars,func,allow_recursion)
                    if r.group(3):
                        p2 = self.evalJS(r.group(3),vars,func,allow_recursion)
                        InterpretedCode = InterpretedCode + '"' + s[ int(p1) : int(p2) ] + '"'
                    else:
                        InterpretedCode = InterpretedCode + '"' + s[ int(p1) :] + '"'
                    out('Substring : var = ' + s + ' index=' + str(p1) )

                    JScode = JScode[(len(object_chain)):]
                    continue
                #join
                r = re.search('(^[\w]+)\.join\((.*)\)',object_chain)
                if r:
                    t = r.group(2).replace('"','').replace("'","")
                    s = self.GetVar(vars,r.group(1))
                    #out('Join : avec ' + str(t) + 'var = ' + str(s))
                    InterpretedCode = InterpretedCode + '"' + t.join(s) + '"'
                    JScode = JScode[(r.end()):]
                    continue
                #slice
                r = re.search('^(^[\w]+)\.slice\((.+?)(?:,(.+))*\)$',object_chain)
                if r:
                    s = self.GetVar(vars,r.group(1))
                    #out('Slice : ' + r.group(0))
                    #out('Slice : ' + r.group(1) + '=' + s)
                    p1 = self.evalJS(r.group(2),vars,func,allow_recursion)
                    if r.group(3):
                        p2 = self.evalJS(r.group(3),vars,func,allow_recursion)
                        sr = s[int(p1):int(p2)]
                    else:
                        sr = s[int(p1):]
                    sr = '"' + sr + '"'
                    InterpretedCode = InterpretedCode + sr
                    
                    JScode = JScode[(r.end()):]
                    continue
                #string.fromCharCode
                r = re.search('^String\.fromCharCode\((.+)\)$',object_chain)
                if r:
                    v = self.evalJS(r.group(1),vars,func,allow_recursion)
                    out('StringFromCharcode ' +  r.group(1) + '=' + str(v))
                    InterpretedCode = InterpretedCode + '"' + chr(int(v)) + '"'
                    JScode = JScode[(len(object_chain)):]
                    continue

            #Simple operation
            if c in '+<>-*/=&%':
                InterpretedCode = InterpretedCode + c
                JScode = JScode[1:]
                continue
                    
            # Not found part
            # We will make another turn
            out("Can't eval string :" + JScode)
            out("Last eval : " + self.LastEval)
            print c
            InterpretedCode = InterpretedCode + JScode
            self.debug = True
            ee(pp)
            continue

                
            #remplacement en laissant parenthses
            #r = re.search('[\(\),]([0-9+-]+[+-][0-9]+)[\(\),]',JScode)
            #if r:
            #    JScode = JScode.replace(r.group(1),str(self.SafeEval(r.group(1))))
            #    continue
            
            #Si pas de parentheses et que des chiffres
            #r = re.search('^[0-9+-.\(\)<>]+$',JScode)
            #if r:
            #    JScode = str(self.SafeEval(JScode))
            #    continue      


        #Bool operation
        if ('True' in InterpretedCode) or ('False' in InterpretedCode):
            InterpretedCode = InterpretedCode.replace('True','1')
            InterpretedCode = InterpretedCode.replace('False','0')
            InterpretedCode = InterpretedCode.replace('&&','&')
            InterpretedCode = InterpretedCode.replace('||','|')
            InterpretedCode = str(self.SafeEval(InterpretedCode))
            InterpretedCode = InterpretedCode.replace('1','True')
            InterpretedCode = InterpretedCode.replace('0','False')
            
        
        #Numeric calculation
        r = re.search('^[0-9+-.\(\)<>&=%]+$',InterpretedCode)
        if r:
            InterpretedCode = str(self.SafeEval(InterpretedCode))
    
        #Alphanumeric concatenation
        InterpretedCode = self.AlphaConcat(InterpretedCode)
        #InterpretedCode = InterpretedCode.replace('+','')
        

        out( 'Evalue >'+ InterpretedCode )
        out( '-------------')
        
        self.LastEval = InterpretedCode
        
        return InterpretedCode
        
    def FormatVarOutput(sel,variable):
        if (isinstance(variable, types.StringTypes)):
            return '"' + variable + '"'
        elif type(variable) in [list,tuple]:
            return variable
        else:
            return str(variable)    
        
    def GetVar(self,var,variable):
        for j in var:
            if j[0] == variable:
                    return j[1]
        raise Exception('Variable not defined: ' + variable)
            
    def SetVar(self,var,variable,value,i = 0):


        #Array
        if value == '[]':
            value = []
        else:
            try:
                #Alpha
                r = re.match(r'^"(.+)"$', value)
                if r:
                    value = r.group(1)
                #Numeric
                else:
                    value = int(value)
            except:
                pass
            
        #Existing var ?
        for j in var:
            if j[0] == variable:

                #vars ?
                if (isinstance(var[var.index(j)][1], types.StringTypes)):
                    var[var.index(j)] = (variable,value)
                #Array
                elif type(var[var.index(j)][1]) in [list,tuple]:

                    Listvalue = var[var.index(j)][1]
                    
                    print Listvalue
                    
                    #ok this place doesn't esist yet
                    l = int(i) - len(Listvalue) + 1
                    while l > 0:
                        Listvalue.append('undefined')
                        l = l - 1
                    #Now modify it
                    Listvalue[int(i)] = value
                    var[var.index(j)] = (variable,Listvalue)
                #Numeric
                else:
                    var[var.index(j)] = (variable,value)

                return
                
        #New var
        var.append((variable,value))
    
    def IsVar(self,var,variable):
        for j in var:
            if j[0] == variable:
                return True
        return False
        
    def IsFunc(self,Func,name):
        for j in Func:
            if j[0] == name:
                return j
        return False
    
    def ReplaceVar(self,JScode):
        modif = True
        while (modif):
            modif = False
            for j in self.Var:
                if j[0] in JScode:
                    JScode = JScode.replace(j[0],'(' + j[1]+ ')')
                    modif = True
                    
        return JScode
        
    def Parse(self,JScode,vars,func,allow_recursion=50):
    
        if allow_recursion < 0:
            raise Exception('Recursion limit reached')
            
        allow_recursion = allow_recursion - 1
    
        #on decoupe le code
        
        #Need all functions first, because they can be called first and be at the bottom of the code
        #So we extract all functions first, and replace them by a simple call in the code, if they are self invoked
        
        posG = 0
        Startoff = 0
        Endoff = 0
        
        while (True):

            chain,pos = self.ExtractFirstchain(JScode[posG:])
            if not (chain):
                break

            Endoff = posG + pos
            #skip empty char
            before = len(chain)
            chain = chain.lstrip()
            posG = posG + before - len(chain)
                
            Startoff = posG
                
            #out('> ' + chain)
            posG = posG + pos
            
            #fonction
            m = re.search(r'^(\()* *function(?: ([\w]+))* *\(([^\)]*)\) *{', chain,re.DOTALL)
            if m:
                if m.group(2):
                    name = m.group(2)
                else:
                    n0 = 0
                    while self.IsFunc(func,'AnonymousFunc' + str(n0)):
                        n0=n0+1
                    name = 'AnonymousFunc' + str(n0)
                param = m.group(3).split(',')
                
                out('Function ' + name + str(param))

                #self invoked ? Not workign yet
                if m.group(1):
                    ddd(pp)
                    pos,content = self.GetBeetweenParenth(chain)
                    pos = pos + m.start()
                    print '++ ' + chain[(pos+2):]
                    print content
                    #need arg too
                    pos2,content2 = self.GetBeetweenParenth(chain[(pos+2):])
                    arg = content2
                    
                    func.append((name,param,content.lstrip()))

                    
                    chain = chain[pos:] 
                    
                else:
                    pos,content = self.GetBeetweenCroch(chain)
                    pos = pos + 1
                    out('content >' + content)
                    func.append((name,param,content.lstrip()))

                    chain = chain[pos:] 
                    
                #param in function ?
                if len(chain)> 0:
                    r = name + chain
                    if not chain.endswith(';'):
                        r = r + ';'
                    out('Self invoked > ' + r)
                    out('param inside ' + chain)
                    JScode = JScode[:Startoff]+ r + JScode[Endoff:]

                else:
                    JScode = JScode[:Startoff]+ JScode[Endoff:]
                    posG = Startoff
                    

        while (True):
            chain,pos = self.ExtractFirstchain(JScode)
            if not (chain):
                break
                
            JScode = JScode[pos:]
                        
            chain = chain.lstrip()
            chain = chain.rstrip()
              
            #print '++++++++++++++++++'
            #print chain
            #print '++++++++++++++++++'
            
            #Jquery ?
            m = re.search(r'^\$\(document\)\.ready\(function\(\) {(.+?)}\);', chain,re.DOTALL)
            if m:
                out('Jquery')
                self.Jquery = m.group(1)
                JScode = JScode.replace(m.group(0),'')
                
                #Pas sur que ce soit a la bonne place
                if self.Jquery:
                    vars = self.Parse(self.Jquery,vars,func,allow_recursion)
                    
                continue
                
            #eval ?
            m = re.search(r'^eval\((.+)\);$', chain,re.DOTALL)
            if m:
                out('Eval')
                JScode = JScode.replace(m.group(0),'')
                #out('To eval >' + m.group(1))
                vars = self.Parse(m.group(1),vars,func,allow_recursion)

            #For boucle ?
            m = re.search(r'^for *\((var[^;]+;)([^;]+);([^\)]+)\) *{(.+?)}$', chain,re.DOTALL)
            if m:
                v = m.group(1)
                t = m.group(2)
                i = m.group(3) + ';'
                f = m.group(4)
                
                #out('> Boucle for : ' + m.group(0))
                
                #init var
                self.Parse(v,vars,func,allow_recursion)

                while (self.evalJS(t,vars,func,allow_recursion) == 'True'):
                    #fonction
                    print '++++++++++++++++++++++++++++'
                    self.Parse(f,vars,func,allow_recursion)
                    #incrementation
                    self.Parse(i,vars,func,allow_recursion)       

                if (False):
                    #Disabled for the moment
                    #So we use hack
                    m = re.search(r'var j = ([\w])\.charCodeAt', chain)
                    if m:
                        Coded_chain = self.GetVar(vars,m.group(1))
                    m = re.search(r'([\w])\[i\] = String.fromCharCode', chain)    
                    if m:
                        tmp = self.GetVar(vars,m.group(1))           
                    
                    url = []
                    for c in Coded_chain:
                        v = ord(c)              
                        if v >= 33 and v <= 126:
                            v = ((v + 14) % 94) + 33
                        url.append(chr(v))

                    print 'url >> ' + str(url)


                continue
                
            #Boucle if
            print '** ' + chain
            m = re.search(r'^if *\(([^{]+)\) *{(.+?)}$', chain,re.DOTALL)
            if m:
                t = m.group(1)
                f = m.group(2)
                e = ''

                #Need to check if there is else statement ?
                chain,pos = self.ExtractFirstchain(JScode)
                if 'else' in chain:
                    chain = chain.lstrip()
                    JScode = JScode[(pos + 1):]
                    m2 = re.search(r'else\s*{(.+?)}$', chain,re.DOTALL)
                    if m2:
                        e = m2.group(1)
                
                #out('> Boucle if : ' + m.group(0) + m2.group(0))
                
                if (self.evalJS(t,vars,func,allow_recursion) == 'True'):
                    self.Parse(f,vars,func,allow_recursion)
                    
                    
                elif (e):
                    self.Parse(e,vars,func,allow_recursion)

                continue
                
            #Variable operation/creation ?
            m = re.search(r'^(?:var )*([^\s\[]+) *= *(.+) *;$', chain)
            if m:
                variable = m.group(1)
                value = m.group(2)
                
                if value == 'String':
                    value = '""'
                
                out( '> Variable Creation => ' + variable + ' = ' + value)
                print chain
                
                #chain
                m = re.match(r'^"([^"]+)"$', value)
                if m:
                    self.SetVar(vars,variable,value)
                #list
                elif value == '[]':
                    self.SetVar(vars,variable,'[]')
                #number
                elif re.match(r'([0-9.-]+)', value):
                    self.SetVar(vars,variable,value)
                #to eval
                else:
                    v = self.evalJS(value,vars,func,allow_recursion)
                    self.SetVar(vars,variable,v)

                continue
            #modification
            m = re.search(r'^([\w]+)(?:\[([^\]]+)\])*\s*=([^;]+);$', chain)
            if m:
                out( '> Variable Modification => ' + m.group(1) + ' = ' + m.group(3))
            
                v = self.evalJS(m.group(3),vars,func,allow_recursion)

                if not m.group(2):
                    self.SetVar(vars,m.group(1),v)
                else:
                    i = self.evalJS(m.group(2),vars,func,allow_recursion)
                    self.SetVar(vars,m.group(1),v,i)
                continue
   
            #Return ?
            if chain.startswith('return '):
                m = re.match(r'return *;', chain)
                if m:
                    return ''
                m = re.match(r'^return ([^;]+)', chain)
                if m:
                    chain = m.group(1)
                    return self.evalJS(chain,vars,func,allow_recursion)
                    
            #operation ?
            m = re.search(r'^(' + REG_NAME + ')\+\+;', chain)
            if m:
                v = str(int(self.GetVar(vars,m.group(1))) + 1)
                self.SetVar(vars,m.group(1),v)
                continue
            m = re.search(r'^(' + REG_NAME + ')\-\-;', chain)
            if m:
                v = str(int(self.GetVar(vars,m.group(1))) - 1)
                self.SetVar(vars,m.group(1),v)
                continue
                    
            #hack ?
            m = re.search(r'\$\("#([^"]+)"\)\.text\(([^\)]+)\);', chain)
            if m:
                out( '> hack ' + m.group(0) + ' , variable est ' + m.group(1))
                self.SetVar(self.HackVars,m.group(1),self.GetVar(vars,m.group(2)))
                continue
            
            #Pas trouve, une fonction ?
            self.evalJS(chain,vars,func,allow_recursion)
            
            #Non gere encore
            out( '> ERROR : can t parse >' + chain)
            
        return vars

    def ProcessJS(self,JScode,vars = []):
        func = []
        vars_return = []
        
        return self.Parse(JScode,vars,func)

        
 

#main

JP = JsParser()
JP.AddHackVar('aQydkd1Gbfx',"u'@D||&FBgHO`cfggghaddOb`]bg]_]_OE59ys33I")
JP.AddHackVar('aQydkd1Gbf',"u'@D||&FBgHO`cfggghaddOb`]bg]_]_OE59ys33)")
vars = JP.ProcessJS(JScode)
print 'return '  + JP.GetVarHack('streamurl')
print vars
