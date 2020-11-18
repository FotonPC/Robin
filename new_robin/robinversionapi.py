# Version generate
import robincounst 
import sys as PYTHON_API
import datetime

def return_version():
    s1='Robin'
    s2=robincounst.COUNST_ROBIN_VERSION
    s3=PYTHON_API.platform
    s4=datetime.datetime.now()
    return ' '.join([s1,s2,'('+str(s4)+')','on',s3])
if __name__=='__main__':
    print(return_version())
