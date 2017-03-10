#!/usr/bin/python3
# -*- coding:utf8 -*-
import codecs
import os
import shutil
import zipfile
import csv
import types  


def un_zip(file_name, tag_dir):  
    """unzip zip file"""  
    zip_file = zipfile.ZipFile(file_name)
    for names in zip_file.namelist():  
        zip_file.extract(names,tag_dir)  
    zip_file.close()  

def extractAndFormat(inFileName, outFileName, keyword):
    if(os.path.exists(inFileName)):
        with open(inFileName, 'r', encoding="utf8") as infile, open(outFileName, 'w') as outfile:
            copy = False
            for line in infile:
                if line.find(keyword) == -1:
                    copy = False
                else:
                    copy = True
                if copy:
                    str1,str2 = line.split("CloudTest>>", 1)
                    str2 = str2.replace(' ', '')
                    str2 = str2.replace(":", ",")
                    outfile.write(str2)
            outfile.close()
    else:
       print(inFileName + " ========> no this file")


def log2csv(filename, csvFileName):
    with open(filename, 'r', encoding="utf8") as infile, open(csvFileName, 'w', encoding='utf8',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        head = ['describe', 'ts_got', 'ts_decoded', 'ts_torende']
        writer.writerow(head)
        for line in infile:
            if line.find("frame_process") != -1:
                writer.writerow(line)
        csvfile.close()

def formatcsv(filename):
    csvFilename = filename
    with open(csvFilename, 'r+', encoding='utf8',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        reader = csv.reader(csvfile, delimiter=",")
        head = ['describe', 'ts_got', 'ts_decoded', 'ts_torende', "decode_time", "to_render_time", "total_time", "speed_test_time", "speed_test_value", "op_start", "op_10", "op_5", "first_frame", "mediaCodec"]
        #writer.writerow(head)
        csvfile.close()

def formatcsv2(csvFileNameGot, csvFileNameQueue, csvFileNameVideo, csvFileNameAll):
    f = open(csvFileNameAll, 'w+')
    print("ts_pts, ts_got, ts_queue, ts_dequeue, ts_render, to_decode, decode_time, to_render_time, total_time", file=f)  
    for line in open(csvFileNameGot, 'r', encoding='utf8',newline=''):
        line=line.strip('\n')
        line=line.strip('\r')
        str_got, ts_pts, ts_got = line.split(",")
        for line in open(csvFileNameQueue, 'r', encoding='utf8',newline=''):
            line=line.strip('\n')
            line=line.strip('\r')
            str_queue, ts_pts_queue, ts_queue = line.split(",")
            if(ts_pts == ts_pts_queue):
                for line in open(csvFileNameVideo, 'r', encoding='utf8',newline=''):
                    line=line.strip('\n')
                    line=line.strip('\r')
                    str_video, ts_queue_video, ts_dequeue, ts_render = line.split(",")
                    #print(ts_queue_video, ts_dequeue, ts_render)
                    #print(type(ts_queue_video), type(ts_queue))
                    #print(len(ts_queue_video), len(ts_queue))
                    if ts_queue == ts_queue_video :
                        #print(ts_pts, ts_got, ts_pts_queue, ts_queue, ts_queue_video, ts_dequeue, ts_render)
                        #print(ts_pts, ts_queue, ts_dequeue, ts_render)
                        to_decode = int(ts_queue) - int(ts_got)
                        decode_time = int(ts_dequeue) - int(ts_queue)
                        to_render = int(ts_render) - int(ts_dequeue)
                        total_time = int(ts_render) - int(ts_got)
                        print("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}".format(ts_pts, ts_got, ts_queue, ts_dequeue, ts_render, to_decode, decode_time, to_render, total_time), file=f)  
                        break
                break

    
#    with open(csvFileNameGot, 'r+', encoding='utf8',newline='') as csvfile_got, open(csvFileNameAll, 'w', encoding='utf8',newline='') as csvfile_all:
#        writer = csv.writer(csvfile_all, delimiter=",")
#        reader = csv.reader(csvfile_got, delimiter=",")
#        head = ['describe', 'ts_pts', 'ts_got', 'ts_decoded', 'ts_torende', 'decode_time', 'to_render_time', 'total_time']
#        writer.writerow(head)
        
def log_from_tecent(rootDir):
    unzipDir =  rootDir + "/log_from_zip/"
    resultDir = rootDir + "/log_result/"
    
    if os.path.isdir(unzipDir):
        print("deleting dir "+unzipDir)
        shutil.rmtree(unzipDir)
        print("done")

    if os.path.isdir(resultDir):
        print("deleting dir "+resultDir)
        shutil.rmtree(resultDir)
        print("done")
    
    os.mkdir(unzipDir)
    os.mkdir(resultDir)
    
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            print(path)
            tag_dir = os.path.join(unzipDir, lists)

            if os.path.isdir(tag_dir):  
                pass  
            else:  
                os.mkdir(tag_dir)

            for files in os.listdir(path):
                filename = os.path.join(path, files)
                if zipfile.is_zipfile(filename):
                    un_zip(filename, tag_dir)
                
            inFileName = os.path.join(tag_dir, 'log.txt')
#            outFileName = os.path.join(resultDir, os.path.basename(tag_dir)+'.log.output')
            csvFileName = os.path.join(resultDir, os.path.basename(tag_dir)+'.csv')
            keyword = "CloudTest>>"
            extractAndFormat(inFileName, csvFileName, keyword)
            if(os.path.exists(csvFileName)):
                formatcsv(csvFileName)
#                log2csv(outFileName, csvFileName)
                
def log_from_mine(rootDir):

    unzipDir =  rootDir + "/log_from_zip/"
    resultDir = rootDir + "/log_result/"
    
    if os.path.isdir(resultDir):
        print("deleting dir "+resultDir)
        shutil.rmtree(resultDir)
        print("done")

    os.mkdir(resultDir)
    
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            print(path)
            tag_dir = os.path.join(unzipDir, lists)

            inFileName = os.path.join(tag_dir, 'log.txt')
            #outFileName = os.path.join(resultDir, os.path.basename(tag_dir)+'.log.output')

            csvFileNameGot = os.path.join(resultDir, os.path.basename(tag_dir)+'.got.csv')
            keyword = "frame_process(got)"
            extractAndFormat(inFileName, csvFileNameGot, keyword)
            
            csvFileNameQueue = os.path.join(resultDir, os.path.basename(tag_dir)+'.queue.csv')
            keyword = "frame_process(queue)"
            extractAndFormat(inFileName, csvFileNameQueue, keyword)

            csvFileNameVideo = os.path.join(resultDir, os.path.basename(tag_dir)+'.video.csv')
            keyword = "frame_process(video)"
            extractAndFormat(inFileName, csvFileNameVideo, keyword)

            csvFileNameAll = os.path.join(resultDir, os.path.basename(tag_dir)+'.all.csv')

            if(os.path.exists(csvFileNameGot)):
                formatcsv2(csvFileNameGot, csvFileNameQueue, csvFileNameVideo, csvFileNameAll)
                #log2csv(outFileName, csvFileName)

tecentDir =r'C:\Users\lenovo\Desktop\tx_round_1'
myDir =r'C:\Users\lenovo\Desktop\cloudtest\vivo\release'



#log_from_tecent(tecnetDir)
log_from_mine(myDir)

