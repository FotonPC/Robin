def analiz(tl,lang='EN'):
    ls=superlexer(tl,lang=lang)
    return ls


def superlexer(tl,lang='EN'):
    for i in range(len(tl)):
        if tl[i][1]=='-' or tl[i][1]=='+' or tl[i][1]=='/' or tl[i][1]=='*' or tl[i][1]=='**' or tl[i][1]=='%' or tl[i][1]=='//':
            tl[i][0]='ao'
        elif tl[i][1]=='!=' or tl[i][1]=='==' or tl[i][1]=='<' or tl[i][1]=='>' or tl[i][1]=='<=' or tl[i][1]=='>=':
            tl[i][0]='bo'
        elif tl[i][1]=='>>' or tl[i][1]=='<<':
            tl[i][0]='pbo'
        elif tl[i][1]=='(':
            tl[i][0]='obe'
        elif tl[i][1]==')':
            tl[i][0]='oee'
        elif tl[i][0]=='name' and lang=='EN':
             name=tl[i][1]
            if name=='print': tl[i][0]='operatorfunc'
            elif name=='if': pass
            elif name=='intentry': tl[i][0]='operatorfunc'
            elif name=='strentry': tl[i][0]='operatorfunc'
            elif name=='floatentry': tl[i][0]='operatorfunc'
            elif name=='boolentry': tl[i][0]='operatorfunc'
            elif name=='goto': tl[i][0]='operatorfunc'
            elif name=='raise': tl[i][0]='operatorfunc'
            elif name=='exit': tl[i][0]='operatorfunc'
            else: tl[i][0]=='var'
        elif tl[i][0]=='name' and lang=='RUS':
            name=tl[i][1]
            if name=='печать': tl[i][0]='operatorfunc'
            elif name=='если': pass
            elif name=='чисввод': tl[i][0]='operatorfunc'
            elif name=='стрввод': tl[i][0]='operatorfunc'
            elif name=='дробввод': tl[i][0]='operatorfunc'
            elif name=='плввод': tl[i][0]='operatorfunc'
            elif name=='строка': tl[i][0]='operatorfunc'
            elif name=='вызов': tl[i][0]='operatorfunc'
            elif name=='выход': tl[i][0]='operatorfunc'
            else: tl[i][0]=='var'
        elif tl[i][0]=='string': pass
        else:
            tl[i][0]='SintaxError'
    return tl

            
            
