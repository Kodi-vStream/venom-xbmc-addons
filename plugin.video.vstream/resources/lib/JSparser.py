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

REG_NAME = '[\w]+'
REG_OP = '[\/*-+\(\)\{\}\[\]]+'


JScode ="""
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

    def SafeEval(self,str):
        f = re.search('[^0-9+-.\(\)]',str)
        if f:
            out ('Wrong parameter to Eval : ' + str)
            return 0
        return eval(str)
        
    def evalJS(self,JScode,vars,func,allow_recursion):
    
        if allow_recursion < 0:
            raise Exception('Recursion limit reached')
            
        allow_recursion = allow_recursion - 1
    
        #https://nemisj.com/python-api-javascript/
        tmp = "abcdefghijklmon" 
        
        if 'substring' in JScode:
            good = True
        else:
            good = False
        

        
        #plus que la chaine a evaluer
        JScode = JScode.replace(' ','')
        
        if (good):
            out( '-------------')
            out( 'A evaluer >'+ JScode)
            
        #********************************************************
        # All this part need to be optimised with a real parser
        
        
        #Simple replacement
        JScode = JScode.replace('.charCodeAt(0)', '')
        
        #hack
        modif = True
        while (modif):
            modif = False
            r = re.search('\$\("#([\w]+)"\)\.text\(\)',JScode)
            if r:
                JScode = JScode.replace(r.group(0),self.GetVar(vars,r.group(1)))

        #Eval function
        modif = True
        while (modif):
            modif = False
            for f,p,c in func:
                r = re.search('('+f+'\(([^)]*)\))',JScode)
                if r:
                    if (len(p) > 0) and (len(r.group(2))>0):
                        nv = tuple(zip(p, r.group(1)))
                        vars.append(nv)

                    v = self.Parse(c,vars,func,allow_recursion)
                    JScode = JScode.replace(r.group(0),v)
                    modif = True
                    
        #Eval variables
        modif = True
        while (modif):
            modif = False
            for n,v in vars:
                r = re.search('(?:' + REG_OP + '|^)' + n + '(?:' + REG_OP + '|$)',JScode)
                if r:
                    nc = r.group(0).replace(n,v)
                    #out( '> Replacement variable :'+ str(n) + ' par ' + str(v))
                    JScode = JScode.replace(r.group(0),nc)
                    modif = True        
            
        #Eval Number
        modif = True
        while (modif):
            modif = False
            #Remplacement en virant parenthses
            r = re.search('[^a-z](\([0-9+-]+\))',JScode)
            if r:
                JScode = JScode.replace(r.group(1),str(self.SafeEval(r.group(1))))
                modif = True
            #remplacement en laissant parenthses
            r = re.search('[\(\),]([0-9+-]+[+-][0-9]+)[\(\),]',JScode)
            if r:
                JScode = JScode.replace(r.group(1),str(self.SafeEval(r.group(1))))
                modif = True
            #Si pas de parentheses et que des chiffres
            r = re.search('^[0-9+-.\(\)]+$',JScode)
            if r:
                JScode = str(self.SafeEval(JScode))
                modif = False #Pour forcer la sortie            
            #slice
            r = re.search('([\w]+)\.slice\((-*[0-9]+)(?:,(-*[0-9]+))*\)',JScode)
            if r:
                s = self.GetVar(vars,r.group(1))
                if r.group(3):
                    JScode = JScode.replace(r.group(0), str(ord(s[int(r.group(2)):int(r.group(3))][0])) )
                else:
                    JScode = JScode.replace(r.group(0),str(ord(s[int(r.group(2)):][0])) )
                modif = True
            #length
            r = re.search('([\w]+)\.length',JScode)
            if r:
                s = self.GetVar(vars,r.group(1))
                JScode = JScode.replace(r.group(0), str(len(s)) )
         
        #Eval string
        modif = True
        while (modif):
            modif = False
            #Substring
            r = re.search('([\w]+)\.substring\((-*[0-9]+)(?:,(-*[0-9]+))*\)',JScode)
            if r:
                s = self.GetVar(vars,r.group(1))
                if r.group(3):
                    JScode = JScode.replace(r.group(0),s[ int(r.group(2)) : int(r.group(3)) ] )
                else:
                    JScode = JScode.replace(r.group(0),s[ int(r.group(2)) :] )
                modif = True
            #chr
            r = re.search('String\.fromCharCode\(([0-9]+)\)',JScode)
            if r:
                JScode = JScode.replace(r.group(0),chr(int(r.group(1))) )
                modif = True
            #join
            r = re.search('([\w]+)\.join\((.*)\)',JScode)
            if r:
                t = r.group(2).replace('"','').replace("'","")
                s = self.GetVar(vars,r.group(1))
                JScode = JScode.replace(r.group(0),t.join(s) )
                modif = True         
        
        #On colle le tout
        JScode = JScode.replace ('+','')
        
        if (good):
            out( 'Evalue > '+ JScode)
            out( '-------------')
        
        return JScode
        
    def GetVar(self,var,variable):
        for j in var:
            if j[0] == variable:
                return j[1]
        raise Exception('Variable not defined: ' + variable)
            
    def SetVar(self,var,variable,value):
        for j in var:
            if j[0] == variable:
                var[var.index(j)] = (variable,value)
                return
        var.append((variable,value))
    
    def IsVar(self,var,variable):
        for j in var:
            if j[0] == variable:
                return True
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
        
    def Parse(self,JScode,vars,func,allow_recursion=100):
    
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
                
        #Jquery ?
        m = re.search(r'\$\(document\)\.ready\(function\(\) {(.+?)}\);', JScode,re.DOTALL)
        if m:
            self.Jquery = m.group(1)
            JScode = JScode.replace(m.group(0),'')
            
            #Pas sur que ce soit a la bonne place
            if self.Jquery:
                vars = self.Parse(self.Jquery,vars,func,allow_recursion)
            
        while len(JScode) > 0:

            #********************************************************************************
            
            #Code special >while for next ect ....
            
            modif = True
            while (modif):
                modif = False
                
                JScode = JScode.lstrip()
                
                #For boucle ?
                m = re.search(r'^for *\(var([^;]+);([^;]+);([^\)]+)\) *{', JScode)
                if m:
                    v = m.group(1)
                    t = m.group(2)
                    i = m.group(3)
                    
                    
                    pos,content = self.GetBeetweenCroch(JScode)
                    
                    JScode = JScode[(pos + 2):]
                    
                    #Disabled for the moment
                    #vars = self.Parse(content,vars,func,allow_recursion)
                    #So we use hack
                    m = re.search(r'var j = ([\w])\.charCodeAt', content)
                    if m:
                        Coded_chain = self.GetVar(vars,m.group(1))
                    m = re.search(r'([\w])\[i\] = String.fromCharCode', content)    
                    if m:
                        tmp = self.GetVar(vars,m.group(1))
                    
                    url = []
                    for c in Coded_chain:
                        v = ord(c)              
                        if v >= 33 and v <= 126:
                            v = ((v + 14) % 94) + 33
                        url.append(chr(v))

                    self.SetVar(vars,'s',url)
                    
                    #out('> Boucle for : ' + content)
                    modif = True
            
            #*******************************************************************************************
            
            #ok chaine simple
            
            chain = ''
            
            s = JScode.find(';') + 1
            
            #no more string to parse ?
            if s == 0:
                JScode = ''
                break
            
            chain = JScode[:s]
            JScode = JScode[(s+1):]
            
            chain = chain.strip()

            #Variable ?
            m = re.search(r'^var ([^\s]+) *= *(.+) *;$', chain)
            if m:
                variable = m.group(1)
                value = m.group(2)
                
                #out( '> Variable => ' + variable + ' = ' + value)
                
                #chain
                m = re.match(r'^"([^"]+)"$', value)
                if m:
                    self.SetVar(vars,variable,m.group(1))
                #list
                elif value == '[]':
                    self.SetVar(vars,variable,[])
                #number
                elif re.match(r'"([0-9.-]+)"', value):
                    self.SetVar(vars,variable,int(value))
                #to eval
                else:
                    v = self.evalJS(value,vars,func,allow_recursion)
                    self.SetVar(vars,variable,v)
                    
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
                    
            #hack ?
            m = re.search(r'\$\("#([^"]+)"\)\.text\(([^\)]+)\);', chain)
            if m:
                #out( '> hack ' + m.group(1))
                self.SetVar(vars,m.group(1),self.GetVar(vars,m.group(2)))
                
                continue
            
            
            #Non gere encore
            out( '> ERROR : can t parse : ' + chain)
            
        return vars

    def ProcessJS(self,JScode,vars = []):
        func = []
        vars_return = []
        return self.Parse(JScode,vars,func)

        
 

#main
vars_input = [('aQydkd1Gbfx',"u'@D||&FBgHO`cfggghaddOb`]bg]_]_OE59ys33I"),('aQydkd1Gbf',"u'@D||&FBgHO`cfggghaddOb`]bg]_]_OE59ys33)")]

JP = JsParser()
vars = JP.ProcessJS(JScode,vars_input)
print JP.GetVar(vars,'streamurl')
