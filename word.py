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


def extract_and_format(in_filename, out_filename, keyword):
    if(os.path.exists(in_filename)):
        with open(in_filename, 'r', encoding="utf8") as infile, open(out_filename, 'w') as outfile:
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
       print(in_filename + " ========> no this file")


def log2csv(filename, csv_filename):
    with open(filename, 'r', encoding="utf8") as infile, open(csv_filename, 'w', encoding='utf8',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        head = ['describe', 'ts_got', 'ts_decoded', 'ts_torende']
        writer.writerow(head)
        for line in infile:
            if line.find("frame_process") != -1:
                writer.writerow(line)
        csvfile.close()


def formatcsv(filename):
    csv_filename = filename
    with open(csv_filename, 'r+', encoding='utf8',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        reader = csv.reader(csvfile, delimiter=",")
        head = ['describe', 'ts_got', 'ts_decoded', 'ts_torende', "decode_time", "to_render_time", "total_time", "speed_test_time", "speed_test_value", "op_start", "op_10", "op_5", "first_frame", "mediaCodec"]
        # writer.writerow(head)
        csvfile.close()


def frame_proccess_data(csv_filename_got, csv_filename_queue, csv_filename_video, filename_all, filename_discard):
    f = open(filename_all, 'w+', encoding='utf8',newline='')
    f_discard = open(filename_discard, "w+", encoding='utf8',newline='')
    for i in [f, f_discard]:
        print("ts_pts, ts_got, ts_queue, ts_dequeue, ts_render, to_decode, decode_time, to_render_time, total_time", file=i)

    for line in open(csv_filename_got, 'r', encoding='utf8',newline=''):
        line=line.strip('\n')
        line=line.strip('\r')
        str_got, ts_pts, ts_got = line.split(",")
        ts_list = [ts_pts, ts_got]
        for line in open(csv_filename_queue, 'r', encoding='utf8',newline=''):
            line=line.strip('\n')
            line=line.strip('\r')
            str_queue, ts_pts_queue, ts_queue = line.split(",")
            if ts_pts == ts_pts_queue:
                ts_list.append(ts_queue)
                for line in open(csv_filename_video, 'r', encoding='utf8',newline=''):
                    line=line.strip('\n')
                    line=line.strip('\r')
                    str_video, ts_queue_video, ts_dequeue, ts_render = line.split(",")
                    # print(ts_queue_video, ts_dequeue, ts_render)
                    # print(type(ts_queue_video), type(ts_queue))
                    # print(len(ts_queue_video), len(ts_queue))
                    if ts_queue == ts_queue_video:
                        ts_list.append(ts_dequeue)
                        ts_list.append(ts_render)
                        # print(ts_pts, ts_got, ts_pts_queue, ts_queue, ts_queue_video, ts_dequeue, ts_render)
                        # print(ts_pts, ts_queue, ts_dequeue, ts_render)
                        to_decode = int(ts_queue) - int(ts_got)
                        decode_time = int(ts_dequeue) - int(ts_queue)
                        to_render = int(ts_render) - int(ts_dequeue)
                        total_time = int(ts_render) - int(ts_got)
                        print("{0}, '{1}, '{2}, '{3}, '{4}, {5}, {6}, {7}, {8}".format(ts_pts, ts_got, ts_queue, ts_dequeue, ts_render, to_decode, decode_time, to_render, total_time), file=f)
                        break
                break
        if len(ts_list) < 5:
            for item in ts_list:
                f_discard.write("'{}, ".format(item))
            f_discard.write("\n")

    
   # with open(csv_filename_got, 'r+', encoding='utf8',newline='') as csvfile_got, open(csv_filename_all, 'w', encoding='utf8',newline='') as csvfile_all:
   #     writer = csv.writer(csvfile_all, delimiter=",")
   #     reader = csv.reader(csvfile_got, delimiter=",")
   #     head = ['describe', 'ts_pts', 'ts_got', 'ts_decoded', 'ts_torende', 'decode_time', 'to_render_time', 'total_time']
   #     writer.writerow(head)
        
def log_from_tecent(root_dir):
    unzip_dir =  root_dir + "/log_from_zip/"
    result_dir = root_dir + "/log_result/"
    
    if os.path.isdir(unzip_dir):
        print("deleting dir "+unzip_dir)
        shutil.rmtree(unzip_dir)
        print("done")

    if os.path.isdir(result_dir):
        print("deleting dir "+result_dir)
        shutil.rmtree(result_dir)
        print("done")
    
    os.mkdir(unzip_dir)
    os.mkdir(result_dir)
    
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if os.path.isdir(path):
            print(path)
            tag_dir = os.path.join(unzip_dir, lists)

            if os.path.isdir(tag_dir):  
                pass  
            else:  
                os.mkdir(tag_dir)

            for files in os.listdir(path):
                filename = os.path.join(path, files)
                if zipfile.is_zipfile(filename):
                    un_zip(filename, tag_dir)
                
            in_filename = os.path.join(tag_dir, 'log.txt')
            # out_filename = os.path.join(result_dir, os.path.basename(tag_dir)+'.log.output')
            csv_filename = os.path.join(result_dir, os.path.basename(tag_dir)+'.csv')
            keyword = "CloudTest>>"
            extract_and_format(in_filename, csv_filename, keyword)
            if os.path.exists(csv_filename):
                formatcsv(csv_filename)
                # log2csv(out_filename, csv_filename)


def analyze_data(tag_dir, result_dir):

    in_filename = os.path.join(tag_dir, 'log.txt')
    csv_filename_got = os.path.join(result_dir, os.path.basename(tag_dir) + '.got.csv')
    keyword = "frame_process(got)"
    extract_and_format(in_filename, csv_filename_got, keyword)

    csv_filename_queue = os.path.join(result_dir, os.path.basename(tag_dir) + '.queue.csv')
    keyword = "frame_process(queue)"
    extract_and_format(in_filename, csv_filename_queue, keyword)

    csv_filename_video = os.path.join(result_dir, os.path.basename(tag_dir) + '.video.csv')
    keyword = "frame_process(video)"
    extract_and_format(in_filename, csv_filename_video, keyword)

    csv_filename_all = os.path.join(result_dir, os.path.basename(tag_dir) + '.all.csv')
    filename_discard = os.path.join(result_dir, os.path.basename(tag_dir) + '.discard.csv')

    if os.path.exists(csv_filename_got):
        frame_proccess_data(csv_filename_got, csv_filename_queue, csv_filename_video, csv_filename_all,
                            filename_discard)
        # log2csv(out_filename, csv_filename)


def business_proccess(business_file, result_file):

    with open(business_file, 'r', encoding="utf8") as infile, open(result_file, 'w') as outfile:
        # print('''104_request, 104_response, 108-request, 108-response, user_start, speed_test_time, speed,
        # 102_request, 102-response, 201-request, 201-response, got_first_frame, codec, 202_request, 202_response
        # ''', file=outfile)
        headers = ['104_request', '104_response', '108-request', '108-response', 'user_start', 'speed_test_time', 'speed',
            '102_request', '102-response', '201-request', '201-response', 'got_first_frame', 'codec', '202_request', '202_response']
        # request_104 = response_104 = request_108 = response_108 = request_102 = response_102 = request_201 = reponse_201 = request_202 = reponse_202 = None
        # usesr_start = speed_test_time = speed =
        first = False
        dict1 = {}
        for line in infile:
            line = line.strip('\n')
            line = line.strip('\r')
            list = line.split(',', line.count(','))
            if list[0] == 'business(104-request)':
                dict1.update({'104_request':list[1]})
                print(list[1])
            elif list[0] == 'business(104-response)':
                print(list[1])
                dict1.update({'104_response': list[1]})
        f_csv = csv.DictWriter(outfile, headers)
        f_csv.writeheader()
        f_csv.writerows(dict1)


def analyze_business(tag_dir, result_dir):

    in_filename = os.path.join(tag_dir, 'log.txt')
    business_file = os.path.join(result_dir, os.path.basename(tag_dir) + '.business.csv')
    keyword1 = "business("
    keyword2 = "got_first_frame"

    if os.path.exists(in_filename):
        with open(in_filename, 'r', encoding="utf8") as infile, open(business_file, 'w') as outfile:
            for line in infile:
                copy = False
                if line.find(keyword1) != -1:
                    copy = True
                if line.find(keyword2) != -1:
                    copy = True
                if copy:
                    str1,str2 = line.split("CloudTest>>", 1)
                    str2 = str2.replace(' ', '')
                    str2 = str2.replace(":", ",")
                    outfile.write(str2)
            outfile.close()
    else:
       print(in_filename + " ========> no this file")

    if os.path.exists(business_file):
        filename = os.path.join(result_dir, os.path.basename(tag_dir) + '.analyze.csv')
        business_proccess(business_file, filename)


def log_from_mine(root_dir):

    unzip_dir = root_dir + "/log_from_zip/"
    result_dir = root_dir + "/log_result/"
    
    if os.path.isdir(result_dir):
        print("deleting dir "+result_dir)
        shutil.rmtree(result_dir)
        print("done")

    os.mkdir(result_dir)
    
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if os.path.isdir(path):
            print(path)
            tag_dir = os.path.join(unzip_dir, lists)
            # analyze_data(tag_dir, result_dir)
            analyze_business(tag_dir, result_dir)



tecentDir = r'C:\Users\lenovo\Desktop\tx_round_1'
myDir = r'C:\Users\lenovo\Desktop\cloudtest\0310\release'


# log_from_tecent(tecnetDir)
log_from_mine(myDir)

