#!/usr/bin/python3
# -*- coding:utf8 -*-
import codecs
import os
import shutil
import zipfile


def un_zip(file_dir, file_name):  
    """unzip zip file"""  
    zip_file = zipfile.ZipFile(file_name)
    tag_dir = file_dir
    if os.path.isdir(tag_dir):  
        pass  
    else:  
        os.mkdir(tag_dir)  
    for names in zip_file.namelist():  
        zip_file.extract(names,tag_dir)  
    zip_file.close()  

def extractAndFormat(path):
    inFileName = os.path.join(path, 'log\log.txt')
    outFileName = os.path.basename(path)+'.output'
    
    with open(inFileName, 'r', encoding="utf8") as infile, open(outFileName, 'w') as outfile:
        copy = False
        for line in infile:
            if line.find("CloudTest>>") == -1:
                copy = False
            else:
                copy = True
            if copy:
                str1,str2 = line.split("CloudTest>>", 1)
                outfile.write(str2)
        outfile.close()

rootDir =r'C:\Users\lenovo\Desktop\tx_round_1'
unzipDir = rootDir + "/log_fromr_zip/"

if os.path.isdir(unzipDir):
    print("deleting dir "+unzipDir)
    shutil.rmtree(unzipDir)
    print("done")
    
os.mkdir(unzipDir)

for lists in os.listdir(rootDir): 
    path = os.path.join(rootDir, lists)
    if os.path.isdir(path):
        print(path)
        for files in os.listdir(path):
            filename = os.path.join(path, files)
            if zipfile.is_zipfile(filename):
                un_zip(os.path.join(unzipDir, lists), filename)

        #extractAndFormat(path)

