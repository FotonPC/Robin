def np(string):
    if 'or' in string:
        string=string+' '
        re=sind(string,'or')
        return np(string[:re:]) or np(string[re+2:len(string)-1])
    elif 'and' in string:
        string=string+' '
        re=tind(string,'and')
        return np(string[:re:]) and np(string[re+3:len(string)-1])
    elif '!=' in string:
        string=string+' '
        re=sind(string,'!=')
        return np(string[:re:])!=np(string[re+2:len(string)-1])
    elif '<' in string:
        string=string+' '
        re=list(string).index('<')
        return np(string[:re:])<np(string[re+1:len(string)-1])
    elif '>' in string:
        string=string+' '
        re=list(string).index('>')
        return np(string[:re:])>np(string[re+1:len(string)-1])
    elif '==' in string:
        string=string+' '
        re=sind(string,'==')
        return np(string[:re:])==np(string[re+2:len(string)-1])
    elif '+' in string:
        string=string+' '
        re=list(string).index('+')
        return np(string[:re:])+np(string[re+1:len(string)-1])
    elif '-' in string:
        string=string+' '
        re=list(string).index('-')
        return np(string[0:re])-np(string[re+1:len(string)-1])
    elif '*' in string:
        string=string+' '
        re=list(string).index('*')
        if string[re+1]!='*':
            return np(string[0:re])*np(string[re+1:len(string)-1])
    elif '/' in string:
        string=string+' '
        re=list(string).index('/')
        if string[re+1]!='/':
            return np(string[0:re])/np(string[re+1:len(string)-1])
    elif '%' in string:
        string=string+' '
        re=list(string).index('%')
        return np(string[0:re])%np(string[re+1:len(string)-1])
    elif '//' in string:
        string=string+' '
        re=sind(string,'//')
        return np(string[0:re])//np(string[re+2:len(string)-1])
    elif '**' in string:
        string=string+' '
        re=sind(string,'**')
        return np(string[0:re])**np(string[re+2:len(string)-1])
    else:
        return int(string)
def sind(string,sstr):
    i=0
    while i<len(string)-1:
        if string[i]+string[i+1]==sstr:
            return i
        i+=1
    raise IndexError('In string no substring!')
def tind(string,sstr):
    i=0
    while i<len(string)-2:
        if string[i]+string[i+1]+string[i+2]==sstr:
            return i
        i+=1
    raise IndexError('In string no substring!')
def evalstr(string):
    if not '(' in string:
        return np(string)
    i=0
    p0s=False
    pos0s=0
    s=0
    res1=0
    while i<len(string):
        if p0s==False and string[i]=='(': pos0s=i
        if string[i]=='(': s+=1;p0s=True
        elif string[i]==')': s-=1
        if s==0 and p0s: res1=i;break
        i+=1
    if pos0s>0 and res1<len(string)-1:
        return evalstr(string[0:pos0s]+str(evalstr(string[pos0s+1:res1]))+string[res1+1::])
    elif pos0s==0 and res1<len(string)-1:
        return evalstr(str(evalstr(string[1:res1]))+string[res1+1::])
    elif pos0s>0 and res1==len(string)-1:
        return evalstr(string[0:pos0s]+str(evalstr(string[pos0s+1:res1])))
    else:
        return evalstr(string[1:-1])
if __name__=='__main__':
    while True:
        inp=input()
        print(evalstr(inp),eval(inp))
