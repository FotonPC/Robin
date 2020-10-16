import random
import robinoldlib as robin
import robincalc as rocalc
import robinerror as roerror
import robinlexer as rolexer
from robincounst import *


def superslice(listi, b, e=-1, p=0):
    if len(listi)==1: return listi[0][p]
    if e==1-1 and b==0: a=listi
    elif b==0: a = listi[:e:]
    elif e==1-1: a=listi[b::]
    else: a=listi[b:e:]
    res = []
    i = 0
    
    while i < len(a):
        res += [str(a[i][p])]
        i += 1
    return res


class DataVar:
    def __init__(self):
        self.date = []

    def __getitem__(self, i):
        return self.date[i]

    def names(self, b=0):
        return [a[1] for a in self.date]

    def ids(self):
        return [a[0] for a in self.date]

    def types(self):
        return [a[2] for a in self.date]

    def values(self):
        return [a[3] for a in self.date]

    def value_re_with_name(self, n, v, l, s):
        i = 0
        while i < len(self.date):
            if self.date[i][1] == n:
                self.date[i][3] = v
                return None
            i += 1
        roerror.Ro_NameError(l, "No variable " + n + '!', s, p=list(s.replace(n, '@')).index('@'))

    def value_re_with_id(self, i, v):
        pass

    def id_re_with_name(self, n, i):
        pass

    def name_re_with_id(self, i, n):
        pass

    def type_re_with_id(self, i, t):
        pass

    def type_re_with_name(self, n, t, l, s):
        i = 0
        while i < len(self.date):
            if self.date[i][1] == n:
                self.date[i][2] = t
                return None
            i += 1
        roerror.Ro_NameError(l, "No variable " + n + '!', s, p=list(s.replace(n, '@')).index('@'))

    def find_type_with_name(self, n, line, string):
        i = 0
        while i < len(self.date):
            if self.date[i][1] == n:
                return self.date[i][2]
            i += 1
        roerror.Ro_NameError(line, "No variable " + n + '!', string, p=list(string.replace(n, '@')).index('@'))

    def find_value_with_name(self, n, line, string):
        i = 0
        while i < len(self.date):
            if self.date[i][1] == n:
                return self.date[i][3]
            i += 1
        roerror.Ro_NameError(line, "No variable " + n + '!', string, p=list(string.replace(n, '@')).index('@'))

    def add_object(self, obj):
        self.date += [obj]

    def __str__(self):
        return 'DataVar: '+str(self.date)


class StopRobinInterpretator(Exception):
    def __init__(self, *argv):
        pass


class Robin:
    """data: DataVar"""

    def __init__(self):
        self.data = DataVar()
        self.codetext = None
        self.code = None

    def __restart__(self):
        self.data = DataVar()
        self.codetext = None

    def __stop__(self):
        raise StopRobinInterpretator('Stop interpretator.')

    def __roexit__(self):
        raise roerror.RoExitError('')

    def __loadcode__(self, code):
        self.codetext = code
        self.code = []

    def __lexer__(self):
        self.code = self.codetext.replace(';', '\n')
        self.codel = self.code.split('\n')
        i = 0
        while i < len(self.codel):
            self.codel[i] = rolexer.lexer(self.codel[i])
            i += 1
        self.code = self.codel
        del self.codel

    def preproccesor(self, string, line, estr):
        varsnames = []
        i = 0
        while i < len(estr):
            cm = estr[i][1]
            cn = estr[i][0]
            if cn == 'name':
                name = cm
                if name == 'print' or name == 'if' or name == 'intentry' or name == 'strentry' or name == 'floatentry' or name == 'boolentry' or name == 'goto' or name == 'raise' or name == 'exit':
                    try:
                        roerror.Ro_SintaxError(line + 1, 'No keywords in operator arguments!', string,
                                               p=list(string.replace(cm, '@')).index('@'))
                    except:
                        exit(1)
                if name == 'and' or name == 'or':
                    continue
                varsnames += [cm]
                try:
                    value = self.data.find_value_with_name(cm, line + 1, string)
                except:
                    exit(1)
                try:
                    typeo = self.data.find_type_with_name(cm, line + 1, string)
                except:
                    exit(1)
                estr[i][0] = typeo
                estr[i][1] = value
            elif i == 0 and cn == 'operator':
                try:
                    roerror.Ro_SintaxError(line + 1, 'Arifmetic operator error!', string,
                                           p=list(string.replace(cm, '@')).index('@'))
                except:
                    exit(1)
            i += 1
        return estr

    def build_evalstr(self, estr):
        """
        :param estr:
        :return evalstrstring:
        """
        i = 0
        while i < len(estr):
            if estr[i][0] == 'string':
                estr[i][1] = '"' + estr[i][1] + '"'
            i+=1
            print(estr)
        return ''.join(superslice(estr,0,-1,1))

    def __exec__(self, i=0, block=0):
        lc = len(self.code)
        data = self.data
        block = block
        while i < lc:
            string = self.codetext.replace(';', '\n').split('\n')[i]
            lexstr = self.code[i]
            if True:
                if block > 0:
                    # block code
                    lexstr = lexstr[block::]
                elif lexstr[block][1] == '    ':
                    try:
                        roerror.Ro_TabError(i + 1, 'Bad tab!', string, p=block)
                    except:
                        exit(1)
                if lexstr[0][0] == 'name':
                    name = lexstr[0][1]
                    if name == 'print':
                        if lexstr[1][0] == 'name':
                            name = lexstr[1][1]
                            if name == 'print' or name == 'if' or name == 'intentry' or name == 'strentry' or name == 'floatentry' or name == 'boolentry' or name == 'goto' or name == 'raise' or name == 'exit':
                                try:
                                    roerror.Ro_SintaxError(i + 1, 'No keywords in operator arguments!', string,
                                                           p=list(string.replace(lexstr[1][1], '@')).index('@'))
                                except:
                                    exit(1)
                            elif len(lexstr) == 2:
                                v = self.data.find_value_with_name(lexstr[1][1], i + 1, string)
                                print(v)

                            else:
                                if True:
                                    if ',' in superslice(lexstr,0,-1,1):
                                        stringi = []
                                        indexi = robin.superindex(superslice(lexstr,1,-1,1), ',')
                                        cs=lexstr[1::]
                                        beginb = 0
                                        i2=0
                                        while i2 < len(indexi):
                                            gg = cs[beginb:indexi[i]:]
                                            stringi += [gg]
                                            beginb = indexi[i] + 1
                                            i2 += 1
                                        i2 = 0
                                        while i2 < len(stringi):
                                            try:
                                                stringi[i] = self.preproccesor(string, i + 1, stringi[i])
                                            except:
                                                exit(1)
                                            i2 += 1
                                        i2 = 0
                                        while i2 < len(stringi):
                                            try:
                                                stringi[i] = self.build_evalstr(stringi[i])
                                            except:
                                                exit(1)
                                            i2 += 1
                                        while i2 < len(stringi):
                                            if '"' in stringi[i]:
                                                continue
                                            try:
                                                stringi[i] = rocalc.evalstr(stringi[i])
                                            except:
                                                try:
                                                    roerror.Ro_SintaxError(i + 1, 'Sintax error!', string)
                                                except:
                                                    exit(1)
                                            i2 += 1
                                        i2 = 0
                                        print(' '.join(map(str, stringi)))
                                    else:
                                        bex = lexstr[1::]
                                        try:
                                            stringi = self.preproccesor(string, i + 1, bex)
                                        except:
                                            exit(1)
                                        stringi = self.build_evalstr(stringi)
                                        if True:
                                        #try:
                                            stringi = rocalc.evalstr(stringi)
                                        #except:
                                            #try:
                                             #   roerror.Ro_SintaxError(i + 1, 'Sintax error!', string)
                                            #except:
                                              #  exit(1)
                                        print(stringi)
                                    stringi = None
                        elif lexstr[1][0] == 'string':
                            if len(lexstr) == 2:
                                print(lexstr[1][1])
                            elif ',' in superslice(lexstr,0,-1,1):
                                stringi = []
                                indexi = robin.superindex(superslice(lexstr,1,-1,1), ',')
                                beginb = 0
                                cs = lexstr[1::]
                                i2 = 0
                                while i2 < len(indexi):
                                    gg = cs[beginb:indexi[i]:]
                                    stringi += [gg]
                                    beginb = indexi[i] + 1
                                    i2 += 1
                                i2 = 0
                                while i2 < len(stringi):
                                    try:
                                        stringi[i] = self.preproccesor(string, i + 1, stringi[i])
                                    except:
                                        exit(1)
                                    i2 += 1
                                i2 = 0
                                while i2 < len(stringi):
                                    try:
                                        stringi[i] = self.build_evalstr(stringi[i])
                                    except:
                                        exit(1)
                                    i2 += 1
                                i2 = 0
                                while i2 < len(stringi):
                                    if stringi[i]:
                                        continue
                                    try:
                                        stringi[i] = rocalc.evalstr(stringi[i])
                                    except:
                                        try:
                                            roerror.Ro_SintaxError(i + 1, 'Sintax error!', string)
                                        except:
                                            exit(1)
                                    i2 += 1
                                i2 = 0
                                print(' '.join(map(str, stringi)))
                        else:
                            if ',' in superslice(lexstr,1,-1,1):
                                stringi = []
                                indexi = robin.superindex(superslice(lexstr,1,-1,1), ',')
                                beginb = 0
                                cs=lexstr[1::]
                                i2 = 0
                                while i2 < len(indexi):
                                    gg = cs[beginb:indexi[i]:]
                                    stringi += [gg]
                                    beginb = indexi[i] + 1
                                    i2 += 1
                                i2 = 0
                                while i2 < len(stringi):
                                    try:
                                        stringi[i] = self.preproccesor(string, i + 1, stringi[i])
                                    except:
                                        exit(1)
                                    i2 += 1
                                i2 = 0
                                while i2 < len(stringi):
                                    try:
                                        stringi[i] = self.build_evalstr(stringi[i])
                                    except:
                                        exit(1)
                                    i2 += 1
                                i2 = 0
                                while i2 < len(stringi):
                                    if '"' in stringi[i]:
                                        continue
                                    try:
                                        stringi[i] = rocalc.evalstr(stringi[i])
                                    except:
                                        try:
                                            roerror.Ro_SintaxError(i + 1, 'Sintax error!', string)
                                        except:
                                            exit(1)
                                    i2 += 1
                                i2 = 0
                                print(' '.join(map(str, stringi)))
                            else:
                                bex = lexstr[1::]
                                print(bex)
                                try:
                                    stringi = self.preproccesor(string, i + 1, bex)
                                except:
                                    exit(1)
                                print(stringi)
                                stringi = self.build_evalstr(stringi)
                                #try:
                                print(stringi)
                                stringi = rocalc.evalstr(stringi)
                                """
                                except:
                                    try:
                                        roerror.Ro_SintaxError(i + 1, 'Sintax error!', string)
                                    except:
                                        exit(1)"""
                                print(stringi)
                                stringi = None
                    elif name == 'if':
                        # Operator IF
                        bm = superslice(lexstr,0,-1,1).index(':')
                        es = lexstr[1:bm]
                        try:
                            es = self.preproccesor(string, i + 1, es)
                        except:
                            exit(1)
                        es = self.build_evalstr(es)
                        try:
                            es = rocalc.evalstr(es)
                        except:
                            try:
                                roerror.Ro_SintaxError(i + 1, 'Bad!', string)
                            except:
                                exit(1)
                        if es: block += 1
                    elif name == 'intentry':
                        if len(lexstr) == 2:
                            try:
                                self.__newobj__('int', int(input()), lexstr[1][1], i + 1, string)
                            except:
                                try:
                                    roerror.Ro_ValueError(i + 1, 'Must be input only number!', string, p=0)
                                except:
                                    exit(1)
                        elif len(lexstr) == 1:
                            input()
                        else:
                            try:
                                roerror.Ro_ValueError(i + 1, 'Bad arguments', string, p=10)
                            except:
                                exit(1)
                    elif name == 'strentry':
                        if len(lexstr) == 2:
                            try:
                                self.__newobj__('str', input(), lexstr[1][1], i + 1, string)
                            except:
                                roerror.Ro_RobinError(i + 1, 'Robin stdin error!', string)
                        elif len(lexstr) == 1:
                            input()
                        else:
                            try:
                                roerror.Ro_ValueError(i + 1, 'Bad arguments', string, p=10)
                            except:
                                exit(1)
                    elif name == 'floatentry':
                        if len(lexstr) == 2:
                            try:
                                self.__newobj__('float', float(input()), lexstr[1][1], i + 1, string)
                            except:
                                try:
                                    roerror.Ro_ValueError(i + 1, 'Must be input only number!', string, p=0)
                                except:
                                    exit(1)
                        elif len(lexstr) == 1:
                            input()
                        else:
                            try:
                                roerror.Ro_ValueError(i + 1, 'Bad arguments', string, p=10)
                            except:
                                exit(1)
                    elif name == 'boolentry':
                        if len(lexstr) == 2:
                            try:
                                self.__newobj__('bool', bool(input()), lexstr[1][1], i + 1, string)
                            except:
                                try:
                                    roerror.Ro_ValueError(i + 1, 'Must be input only number!', string, p=0)
                                except:
                                    exit(1)
                        elif len(lexstr) == 1:
                            input()
                        else:
                            try:
                                roerror.Ro_ValueError(i + 1, 'Bad arguments', string, p=10)
                            except:
                                exit(1)
                    elif name == 'goto':
                        try:
                            i = rocalc.evalstr(self.build_evalstr(self.preproccesor(string, i + 1, lexstr[1::]))) - 1
                        except roerror.RoExitError:
                            exit(1)
                        except:
                            try:
                                roerror.Ro_SintaxError(i + 1, 'Goto argument error!', string, p=6)
                            except:
                                exit(1)
                    elif name == 'raise':
                        try:
                            roerror.Ro_SimpleError(i + 1, '', string, p=0)
                        except:
                            exit(1)
                    elif name == 'exit':
                        exit(0)
                    elif name == 'qwene':
                        print(self.codetext)
                    else:
                        if lexstr[1][1] == '=':
                            if len(lexstr) == 3 and lexstr[2][0] == 'string':
                                self.__newobj__('string', lexstr[2][1], lexstr[0][1], i + 1, string)
                            elif lexstr[2][0] == 'name':
                                if self.data.find_type_with_name(lexstr[2][1],i+1,string) == 'string':
                                    if len(lexstr) == 3:
                                        self.__newobj__('string', lexstr[2][1], lexstr[0][1], i + 1, string)
                                    else:
                                        try:
                                            roerror.Ro_SintaxError(i + 1, 'No operation with string!', string)
                                        except:
                                            exit(1)
                                else:
                                    bex = lexstr[2::]
                                    try:
                                        stringi = self.preproccesor(string, i + 1, bex)
                                    except:
                                        exit(1)
                                    stringi = self.build_evalstr(stringi)
                                    try:
                                        stringi = rocalc.evalstr(stringi)
                                    except:
                                        try:
                                            roerror.Ro_SintaxError(i + 1, 'Sintax error!', string)
                                        except:
                                            exit(1)
                                    if string.__class__.__name__ == 'int':
                                        self.__newobj__('int', stringi, lexstr[0][1], i + 1, string)
                                    if string.__class__.__name__ == 'float':
                                        self.__newobj__('float', stringi, lexstr[0][1], i + 1, string)
                                    if string.__class__.__name__ == 'bool':
                                        self.__newobj__('bool', stringi, lexstr[0][1], i + 1, string)
                            else:
                                bex = lexstr[2::]
                                try:
                                    stringi = self.preproccesor(string, i + 1, bex)
                                except:
                                    exit(1)
                                stringi = self.build_evalstr(stringi)
                                try:
                                    stringi = rocalc.evalstr(stringi)
                                except:
                                    try:
                                        roerror.Ro_SintaxError(i + 1, 'Sintax error!', string)
                                    except:
                                        exit(1)
                                if stringi.__class__.__name__ == 'int': self.__newobj__('int', stringi, lexstr[0][1],
                                                                                       i + 1, string)
                                if stringi.__class__.__name__ == 'float': self.__newobj__('float', stringi, lexstr[0][1],
                                                                                         i + 1, string)
                                if stringi.__class__.__name__ == 'bool': self.__newobj__('bool', stringi, lexstr[0][1],
                                                                                        i + 1, string)
                elif lexstr[0][1] == '    ':
                    # block code
                    pass
                else:
                    try:
                        roerror.Ro_SintaxError(i + 1, 'Bad sintax!', string)
                    except:
                        exit(1)
            i += 1
            print(self.data)

    def __newobj__(self, typev, value, name, line, string):
        if name in self.data.names():
            self.data.value_re_with_name(name, value, line, string)
            return 0
        id_o = random.randint(0, COUNST_RO_INT_SIZE_32)
        id_o = str(id_o)
        id_o = "0" * (COUNST_RO_LENGTH_INT_32 - len(id_o)) + id_o
        self.data.add_object([id_o, name, typev, value])


if __name__ == '__main__':
    ro = Robin()
    while (True):
        if True:
        #try:
            inp = input('>>>')
            ro.__loadcode__(inp)
            ro.__lexer__()
            ro.__exec__()
        #except:
            #print('Exit 1')
