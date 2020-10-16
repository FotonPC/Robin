import robinoldlib as robin
def lexer(string):
    string_save=string
    perem_string=None
    indexstringmarker=robin.superindex(string,'"')
    string=string
    string=lns(string)
    #print(string)
    string=tokens(string)
    return string
def tokens(string):
    res=[]
    for l in string:
        if l.isdigit():
            res+=[['int',l]]
        elif isdigitstring(l):
            res+=[['float',l]]
        elif '"' in l:
            res+=[['string',l]]
        elif isalphastring(l):
            res+=[['name',l]]
        elif isoperstring(l):
            res+=[['operator',l]]
        elif l==')':
            res+=[['rightendex',l]]
        elif l=='(':
            res+=[['leftendex',l]]
        elif l==':':
            res+=[['blockbegin',l]]
        elif l=='   ':
            res+=[['blockmarker',l]]
        else:
            res+=[['error',l]]
    return res
def lns(string):
    keyl=[]
    i=0
    while i<len(string):
        if string[i]!=' ':
            keyword,i=indexlex(i,string)
            if '"' in keyword:
                i-=1
            if isalphastring(keyword) or isdigitstring(keyword) or isoperstring(keyword):
                i-=1
            keyl+=[keyword]
        i+=1
        #print(0,i)
    return keyl    
def isalpha(char):
    return char.lower() in list('abcdefghjiklmnoprstqwyxzuйцукенгшщзхъфывапролджэячсмитьбю')
def isalphastring(string):
    for char in string:
        if not isalpha(char):
            return False
    return True
def isoperstring(string):
    for char in string:
        if not isoper(char):
            return False
    return True
def isdigitstring(string):
    for char in string:
        if not isdigit(char):
            return False
    return True
def isoper(char):
    return char in list('!=+-/*.%<>,')
def isdigit(string):
    return string in "1234567890."
def indexlex(i,string):
    res=i+1
    #print(1)
    if isdigit(string[i]):
        for c in range(i,len(string)):
            if not isdigit(string[c]):
                res=c
                return string[i:res:],res
        return string[i::],len(string)
    if isalpha(string[i]):
        for c in range(i,len(string)-1):
            if not isalpha(string[c]):
                res=c
                return string[i:res:],res
        return string[i::],len(string)
    if isoper(string[i]):
        for c in range(i,len(string)-1):
            if not isoper(string[c]):
                res=c
                return string[i:res:],res
        return string[i::],len(string)
    if string[i]=='(' or string[i]==')' or string[i]==':' or string[i]=='   ' or string[i]=='\n':
        return string[i],i
    if string[i]=='"':
        for c in range(i+1,len(string)-1):
            if string[c]=='"':
                #print(2,c+1,string[i:c+1:])
                return string[i:c+1:],c+1
                
    #print(2,res,string[i:res:])
    return string[i:res:],res
if __name__=='__main__':
    print(lexer(input()))
