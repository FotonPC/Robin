import robin_pl as robin
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Menu
import requests
import webbrowser 
import re,keyboard
from tkinter.ttk import Combobox
import random,sys,os
### import modules
def sinput(p=''):
    sprint(p)
    return shell_out.readline()
def sprint(*value,out=0):
    if(out==1):
        sys.stdout.write(str('' .join(value)))
        return
    shell_out.write(str(' '.join(map(str,value))))
def superremove(s,v):
    while True:
        try: s.remove(v)
        except: break
    return s
#Core Robin
def is_error(obj):
    try:
        obj.ie()
        return True
    except:
        return False
def supereval(value):
    res=value
    while True:
        try:
            res=eval(res)
        except: break
    return res
def superindex(it,value):
    res=[]
    for i in range(len(it)):
        if it[i]==value:
            res+=[i]
    return res
class RoExitStringError(Exception):
    def __init__(self,*argv):
        pass
class Ro_Error:
    def __init__(self,line,text,string,p=0,lang='RUS'):
        self.lang=lang
        self.line=line
        self.info=text
        self.string=string
        self.out(p)
        raise RoExitStringError('')
    def ie(self): pass
    def out(self,p):
        sprint(self.stroka(),str(self.line)+':',"\n "+self.string,"\n"+self.pos(p),'\n',self.name()+':',self.info)
    def name(self):
        if self.lang=='RUS':
            return "Базовая ошибка"
        return 'BasicError'
    def pos(self,p):
        return ' '*(p+1)+"^"
    def stroka(self):
        if self.lang=='EN':
            return ' In string'
        return ' В строке'
class Ro_NameError(Ro_Error):
    def name(self):
        if self.lang=='RUS':
            return 'Ошибка имени переменной'
        return 'NameError'
class Ro_SintaxError(Ro_Error):
    def name(self):
        if self.lang=='RUS':
            return 'Ошибка синтаксиса'
        return 'SintaxError'
class data:
    def __init__(self,lang='RUS'):
        self.date=[];self.lang=lang
    def __getitem__(self,i):
        return self.date[i]
    def names(self,b=0):
        return [a[1] for a in self.date]
    def ids(self):
        return [a[0] for a in self.date]
    def types(self):
        return [a[2] for a in self.date]
    def values(self):
        return [a[3] for a in self.date]  
    def value_re_with_name(self,n,v,l,s):
        i=0
        while i<len(self.date):
            if self.date[i][1]==n:
                self.date[i][3]=v
                return None
            i+=1
        if self.lang=='RUS': Ro_NameError(l,"Нет имени "+n+'!',s,p=list(s.replace(n,'@')).index('@'))
        if self.lang=='EN': Ro_NameError(l,"No variable "+n+'!',s,p=list(s.replace(n,'@')).index('@'),lang='EN')
    def value_re_with_id(self,i,v): pass
    def id_re_with_name(self,n,i): pass
    def name_re_with_id(self,i,n): pass
    def type_re_with_id(self,i,t): pass
    def type_re_with_name(self,n,t): pass
    def find_value_with_name(self,n,line,string):
        i=0
        while i<len(self.date):
            if self.date[i][1]==n:
                return self.date[i][3]
            i+=1
        if self.lang=='RUS': Ro_NameError(line,"Нет имени "+n+'!',string,p=list(string.replace(n,'@')).index('@'))
        if self.lang=='EN': Ro_NameError(line,"No variable "+n+'!',string,p=list(string.replace(n,'@')).index('@'),lang='EN')
    def add_object(self,obj):
        self.date+=[obj]
    def __str__(self):
        return str(self.date)
    
class Robin:
    def __init__(self,lang='RUS'):
        self.data=data(lang)
        self.lang=lang
        self.idnumber=1
        if lang=="EN":
            self.new_object("True",'bool',True,None,None)
            self.new_object("False",'bool',False,None,None)
            sprint('Robin 0.5.3 open sourse edition.\nDeveloper Foton-PC')
        if lang=='RUS':
            self.new_object("Истина",'bool',True,None,None)
            self.new_object("Ложь",'bool',False,None,None)
            sprint('Робин 0.5.3 открытое издание.\nРазрабочик Foton-PC')
    def load(self,ert):
        self.eexece(ert)
    def eexece(self,code):
        code=code.replace(';','\n')
        self.exec(code)
    def error(self,e):
        e.out()
    def str_re(self,bex,l,s):
        stri=superindex(bex,'"')
        if len(stri)%2==1:
            if self.lang=='RUS': Ro_SintaxError(l,'Неожиданный маркер "',s,p=max(stri),lang=self.lang)
            if self.lang=='EN': Ro_SintaxError(l,'Unexpected marker "',s,p=max(stri),lang=self.lang)
        for i in range(0,len(stri)//2,2):
            self.new_object("|"+'s'*self.idnumber,'str',"'"+bex[stri[i]+1:stri[i+1]:]+"'",l,s)
            bex=bex.replace(bex[stri[i]:stri[i+1]+1:],"|"+'s'*self.idnumber)
            self.idnumber+=1
        return bex
    def boolexex(self,bex,l,string):
        sc=string
        exc=bex
        stri=superindex(bex,'"')
        for c in list('.+-*/%1234567890>=<!'):
            try:
                exc=exc.replace(c," ")
            except: pass
        exc=exc.split()
        if self.lang=='RUS':
            bex=bex.replace('не','not')
            bex=bex.replace('и','and')
            bex=bex.replace('или','or')
        for nm in exc:
            bex=bex.replace(nm,str(self.data.find_value_with_name(nm,l,sc)))
        return bex
    def exec(self,codepart,line=0,lines=None):
        lang=self.lang
        codepartlist=list(codepart.split("\n"))
        i=line
        if(lines==None):
            lines=len(codepartlist)
        while i<lines:
            win.update()
            string=codepartlist[i]
            string=self.str_re(string,i+1,codepartlist[i])
            if ' ' in string:
                oper=string.split()[0]
                oper2=string.split()[1]
                if oper=='строка' and lang=='RUS' or oper=='goto' and lang=='EN':
                    #if True:
                    try:
                        i=eval(self.boolexex(string.split()[1],i+1,string))-2
                    except:
                        if lang=="RUS": Ro_SintaxError(i+1,'Должно быть число',string)
                        if lang=="EN": Ro_SintaxError(i+1,'Must be a number',string,lang='EN')
                if oper=='печать' and lang=='RUS' or oper=='print' and lang=='EN':
                    #if True:
                    try:
                        sprint(eval(self.boolexex(string.split()[1],i+1,string)))
                    except Exception as e:
                        if e.__class__.__name__=='RoExitStringError':
                            return 'Fail'
                        Ro_SintaxError(i+1,'',string,lang=lang)
                if oper2=='++':
                    try:
                        self.new_object(oper,'int',self.data.find_value_with_name(oper,i+1,string)+1,i+1,string)
                    except Exception as e:
                        if e.__class__.__name__=='RoExitStringError':
                            return 'Fail'
                        Ro_SintaxError(i+1,'',string,lang=lang)
                if oper=='чисввод' and lang=='RUS' or oper=='intentry' and lang=='EN':
                    #if True:
                    try:
                        self.new_object(string.split()[1],'int',int(input()),i+1,string)
                    except ValueError:
                        if lang=='EN': Ro_SintaxError(i+1,'Must be input a number!',string,lang=self.lang)
                        if lang=='RUS': Ro_SintaxError(i+1,'Введено не число!',string,lang=self.lang)
                if oper=='если' and lang=='RUS' or oper=='if' and lang=='EN':
                    n=string.index(':')
                    s1=string.index('(')
                    s2=string.index(')')
                    #if True:
                    try:
                        if(bool(eval(self.boolexex(string[s1+1:s2:],i+1,string)))):
                            strin=string[n+1::]
                            if ' ' in strin:
                                oper=strin.split()[0]
                                if oper=='строка' and lang=='RUS' or oper=='goto' and lang=='EN':
                                    try:
                                        i=int(strin.split()[1])-2
                                    except:
                                        if lang=="RUS": Ro_SintaxError(i+1,'Должно быть число',strin)
                                        if lang=="EN": Ro_SintaxError(i+1,'Must be a number',strin,lang=lang)
                                if oper=='печать' and lang=='RUS' or oper=='print' and lang=='EN':
                                    #if True:
                                    try:
                                        sprint(eval(self.boolexex(strin.split()[1],i+1,strin)))
                                    except Exception as e:
                                        if e.__class__.__name__=='RoExitStringError':
                                            return 'Fail'
                                        Ro_SintaxError(i+1,'',strin,lang=lang)
                                if oper2=='++':
                                    try:
                                        self.new_object(oper,'int',self.data.find_value_with_name(oper,i+1,string)+1,i+1,string)
                                    except Exception as e:
                                        if e.__class__.__name__=='RoExitStringError':
                                            return 'Fail'
                                        Ro_SintaxError(i+1,'',string,lang=lang)
                                if oper=='чисввод' and lang=='RUS' or oper=='intentry' and lang=='EN':
                                    #if True:
                                    try:
                                        self.new_object(string.split()[1],'int',int(input()),i+1,string)
                                    except ValueError:
                                        if lang=='EN': Ro_SintaxError(i+1,'Must be input a number!',string,lang=self.lang)
                                        if lang=='RUS': Ro_SintaxError(i+1,'Введено не число!',string,lang=self.lang)
                            if "=" in strin:
                                strlist=strin.split("=")
                                #if(True):
                                try:
                                    es=eval(self.boolexex(strlist[1],i+1,strin))
                                    self.new_object(strlist[0],'int',es,i+1,strin)
                                except Exception as e:
                                    if e.__class__.__name__=='RoExitStringError':
                                        return 'Fail'
                                    Ro_SintaxError(i+1,'',strin,lang=lang)
                    except Exception as e:
                        if e.__class__.__name__=='RoExitStringError':
                            return 'Fail'
                        Ro_SintaxError(i+1,'',string,lang=lang)
                i+=1
                continue
            if "=" in string:
                strlist=string.split("=")
                #if(True):
                try:
                    es=eval(self.boolexex(strlist[1],i+1,string))
                    if type(es)==type(''):
                        es="'"+es+"'"
                    self.new_object(strlist[0],str(type(es)),es,i+1,string)
                except Exception as e:
                    if e.__class__.__name__=='RoExitStringError':
                        return 'Fail'
                    Ro_SintaxError(i+1,'',string,lang=lang)
            i+=1
            win.update()
    def new_object(self, name,typeo,value,line,string):
        if name in self.data.names():
            self.data.value_re_with_name(name,value,line,string)
            return None
        id_o=random.randint(0,1000000000000)
        id_o=str(id_o)
        id_o="0"*(13-len(id_o))+id_o
        self.data.add_object([id_o,name,typeo,value])
def exec_robin(code,lang='RUS'):
    robin_inter=Robin(lang=lang)
    robin_inter.load(code)
#Core Robin
class Shell(scrolledtext.ScrolledText):
    def __init__(self,master,width=100,height=50):
        self._w=scrolledtext.ScrolledText(master,width=width,height=height)
        self.tk=win
        self.master=master
    def write(self,value):
        self._w.insert(END,'\n'+value)
    def readline(self):
        self._w.insert(END,'\n')
        while True:
            try:
                if keyboard.is_pressed('Enter'):
                    break
            except: pass
            win.update()
        res=str(self._w.get(1.0,END))
        return superremove(res.split('\n'),'')[-1]
tabs_list=[]
scrtext_list=[]
win=Tk()
win.title('Robin IDE')
def quitc(): win.destroy()
def openf():
    fn=filedialog.askopenfilename()
    text=open(fn).read()
    newf(title=fn.split('/')[-1],text=text)
def savef():
    newname=filedialog.asksaveasfilename()
    ind=tab_control.tabs().index(tab_control.select())
    file=open(newname,mode='w+',encoding='UTF-8')
    file.write(scrtext_list[ind].get(1.0,END))
    file.close()
    tab_control.tab("current", text=newname.split('/')[-1])
def newf(title='Новый',text=''):
    global tabs_list,scrtext_list
    tabs_list+=[ttk.Frame(tab_control)]
    scrtext_list+=[scrolledtext.ScrolledText(tabs_list[-1], width=640, height=160,font=('Courier New',10,'bold'))]
    scrtext_list[-1].pack(ipady=5,ipadx=5)
    scrtext_list[-1].insert(END,text)
    tab_control.add(tabs_list[-1], text=title)
def run():
    ind=tab_control.tabs().index(tab_control.select())
    code=scrtext_list[ind].get(1.0,END)
    indexs=superindex(code, '\n')
    lang=code[0:indexs[0]:]
    code=code[indexs[0]+1::]
    exec_robin(code,lang)
def closetab():
    ind=tab_control.tabs().index(tab_control.select())
    scrtext_list.pop(ind)
    tab_control.forget(tab_control.select())
def shell():
    os.system('python core.py')
menu = Menu(win)  
file_item = Menu(menu)
file_item.add_command(label='Выход' , command=quitc)
file_item.add_command(label='Открыть' , command=openf)
file_item.add_command(label='Сохранить как...' , command=savef)
file_item.add_command(label='Новый файл...' , command=newf)
file_item.add_command(label='Закрыть файл...' , command=closetab)

menu.add_cascade(label='Файл', menu=file_item)
run_item = Menu(menu)
run_item.add_command(label='Запустить' , command=run)
run_item.add_command(label='Интерактивный режим' , command=shell)
menu.add_cascade(label='Запуск', menu=run_item)
text_editor=LabelFrame(win,text='Редактор')
shell=LabelFrame(win,text='Оболочка')
shell_out=Shell(shell,width=147,height=10)
shell_out.pack()
tab_control=ttk.Notebook(text_editor,width=1200,height=400)
tab_control.pack()
newf()
text_editor.pack()
shell.pack()
win.config(menu=menu)
win.mainloop()
