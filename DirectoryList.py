import os
from os import path
import datetime
from datetime import date, time, timedelta
import time
import pathlib
import hashlib

def main():
    rootdir='E:\\ALL_Photos'
    for root, dirs, files in os.walk(rootdir,topdown=True):
        for name in files:
            # print(path.join(root,name))
            ListFile(path.join(root,name))

def ListFile(fullpath):
    if(path.isfile(fullpath)):
        filedir,filename = path.split(path.realpath(fullpath))
        filemtime = datetime.datetime.fromtimestamp(path.getmtime(fullpath)).strftime('%Y-%m-%d %H:%M:%S')
        filesize =path.getsize(fullpath)
        try:
            md5 = hashlib.md5(pathlib.Path(fullpath).read_bytes()).hexdigest()
        except MemoryError:
            md5 = '0'
        print(','.join(('"'+filedir+'"','"'+filename+'"',filemtime,str(filesize),md5)).encode("utf-8"))
        
if __name__ == '__main__':
    main()
