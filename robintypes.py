#Robin types
import random
import robinerror as error
from robincounst import *
class RoObject:
    def __init__(self,typeo='NoneType',value=None,lang='RUS'):
        self.type=typeo
        self.lang=lang
        self.value=value
    def __str__(self):
        return str(self.value)
class RoInteger(RoObject):
    def __init__(self,value):
        self=RoObject('int',value)
        self.id=random.randint(0,COUNST_RO_INT_SIZE_32)
class RoFloat(RoObject):
    def __init__(self,value):
        self=RoObject('float',value)
        self.id=random.randint(0,COUNST_RO_INT_SIZE_32)
class RoString(RoObject):
    def __init__(self,value):
        self=RoObject('str',value)
        self.id=random.randint(0,COUNST_RO_INT_SIZE_32)
class RoBool(RoObject):
    def __init__(self,value):
        self=RoObject('bool',value)
        self.id=random.randint(0,COUNST_RO_INT_SIZE_32)
class RoNoneType(RoObject):
    def __init__(self,value):
        self=RoObject()
        self.id=random.randint(0,COUNST_RO_INT_SIZE_32)
class NoneRobin:
    def __init__(self): pass
class RoFunction(RoObject):
    def __init__(self,value,argument=[],line=0):
        self=RoObject('func',value)
        self.line=line
        self.argument=argument
        self.id=random.randint(0,COUNST_RO_INT_SIZE_32)
    def run(self,argument=[NoneRobin()],DataVar=None,line=0,string='',ir=None):
        if len(self.argument)==1:
            if argument.__class__.__name__=='NoneRobin':
                return error.RoValueError(line,'An argument was expected but it isn\'t',string)
            else:
                DataVar.newobject(self.argument,argument)
        return self.line
