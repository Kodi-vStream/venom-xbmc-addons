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


import re
import types

REG_NAME = '[\w]+'
REG_OP = '[\/*-+\(\)\{\}\[\]<>]+'


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
        
        i = 0
        p = 0
        a = 0
        f = False
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
            if (ch == ';') and not (f) and (p == 0):
                #ok simple chain
                if (p == 0) and (a == 0):
                    i = i + 1
                    return string[:i],i
                #else function
                else:
                    f = True
            if (f) and (p == 0) and (a == 0):
                i = i + 1
                #hack
                if string[i] == ';':
                    i = i + 1
                return string[:i],i            
            i = i + 1
            
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
        return str[s:e]
        
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
                print 'ok'
                c2 = self.GetBeetweenParenth(JScode)
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
            r = re.search('^('+REG_NAME+')\(([^\)]*)\)',JScode)
            if r:
                Func_chain = r.group(0)
                print "func " + Func_chain
                
                #Def function ?
                fe = self.IsFunc(func,r.group(1))
                if fe:
                    f,p,c = fe
                    
                    if (len(p) > 0) and (len(r.group(2))>0):
                        nv = tuple(zip(p, r.group(1)))
                        vars.append(nv)

                    v = self.Parse(c,vars,func,allow_recursion)
                    
                    InterpretedCode = InterpretedCode + v
                    JScode = JScode[(len(Func_chain)):]
                    continue
                    
                #Native function ?
      
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
                        object_chain = object_chain + '(' + self.GetBeetweenParenth(JScode) + ')'
 
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
        
        #Need all functions first
        Found = True
        while (Found):
            Found = False
            #fonction
            m = re.search(r'function ([^\s]+) *\(([^\)]*)', JScode)
            if m:
                Found = True
                
                name = m.group(1)
                arg = m.group(2)

                pos,content = self.GetBeetweenCroch(JScode[m.start():])
                pos = pos + m.start()
                
                func.append((name,arg,content.lstrip()))
                JScode = JScode[:m.start()]+ JScode[(pos + 2):]
                
                #out('> Fonction ' + name)
        
        while (True):
            chain,pos = self.ExtractFirstchain(JScode)
            if not (chain):
                break
        
            chain = chain.lstrip()
            JScode = JScode[(pos + 1):]
            
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
            m = re.search(r'^if \(([^{]+)\) *{(.+?)}$', chain,re.DOTALL)
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
                
            #Variable ?
            #initalisation
            m = re.search(r'^var ([^\s]+) *= *(.+) *;$', chain)
            if m:
                variable = m.group(1)
                value = m.group(2)
                
                out( '> Variable Init => ' + variable + ' = ' + value)
                
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
                out( '> Variable => ' + m.group(1) + ' = ' + m.group(3))
            
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
