import os
from os import path
import datetime
from datetime import date, time, timedelta
import time
import pathlib
import hashlib

def main():
    rootdir='C:\\Oracle\\Scripts'
    for root, dirs, files in os.walk(rootdir,topdown=True):
        for name in files:
            # print(path.join(root,name))
            ListFile(path.join(root,name))

def ListFile(fullpath):
    if(path.isfile(fullpath)):
        filedir,filename = path.split(path.realpath(fullpath))
        t = datetime.datetime.fromtimestamp(path.getmtime(fullpath)).strftime('%Y-%m-%d %H:%M:%S')
        filesize =path.getsize(fullpath)
        md5 = hashlib.md5(pathlib.Path(fullpath).read_bytes()).hexdigest()
        print(','.join(('"'+filedir+'"','"'+filename+'"',t,str(filesize),md5)))
        
if __name__ == '__main__':
    main()

