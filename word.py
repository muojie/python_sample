#!/usr/bin/python3
# -*- coding:utf8 -*-
import codecs
import os
import shutil
import zipfile
import csv
import types
from collections import namedtuple
from tempfile import NamedTemporaryFile
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.pylab import datestr2num
import matplotlib.pyplot as pl
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np
import chardet
from pylab import *

TBN = 1000

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


def isNum(value):
    try:
        float(value)
    except:
        isFloat = False
    else:
        isFloat = True

    try:
        int(value)
    except:
        isInt = False
    else:
        isInt = True
    return isFloat or isInt


def frame_proccess_data(csv_filename_got, csv_filename_queue, csv_filename_dequeue, csv_filename_video, filename_all, filename_discard):
    f = open(filename_all, 'w+', encoding='utf8',newline='')
    f_discard = open(filename_discard, "w+", encoding='utf8',newline='')
    for i in [f, f_discard]:
        print("ts_pts, ts_got, ts_queue, ts_dequeue, ts_render, to_decode, decode_time, to_render_time, total_time", file=i)
    queue_done = 0
    dequeue_done = 0
    video_done = 0
    for line in open(csv_filename_got, 'r', encoding='utf8',newline=''):
        line=line.strip('\n')
        line=line.strip('\r')
        str_got, ts_pts, ts_got = line.split(",")
        ts_list = [ts_pts, ts_got]
        if not isNum(ts_pts):
            print(ts_pts)
            continue

        skip = queue_done
        for line in open(csv_filename_queue, 'r', encoding='utf8',newline=''):
            if skip > 0:
                skip -= 1
                continue
            line=line.strip('\n')
            line=line.strip('\r')
            str_queue, pts_queue, ts_queue = line.split(",")
            if isNum(pts_queue) and ((int(pts_queue)-int(ts_pts)*1000)) == 0:
                queue_done += 1
                ts_list.append(ts_queue)
                break

        skip = dequeue_done
        for line in open(csv_filename_dequeue, 'r', encoding='utf8',newline=''):
            if skip > 0:
                skip -= 1
                continue
            line=line.strip('\n')
            line=line.strip('\r')
            str_dequeue, pts_dequeue, ts_dequeue = line.split(",")
            if (int(pts_dequeue) - int(ts_pts) * 1000) == 0:
                dequeue_done += 1
                ts_list.append(ts_dequeue)
                break

        skip = video_done
        for line in open(csv_filename_video, 'r', encoding='utf8', newline=''):
            if skip > 0:
                skip -= 1
                continue
            line = line.strip('\n')
            line = line.strip('\r')
            str_video, pts_video, dequeue_video, ts_render = line.split(",")
            if (float(pts_video) - float(ts_pts) / 1000) == 0:
                video_done += 1
                ts_list.append(ts_render)
                break

        if len(ts_list) < 5:
            for item in ts_list:
                f_discard.write("'{}, ".format(item))
            f_discard.write("\n")
        else:
            # print(ts_pts, ts_got, ts_pts_queue, ts_queue, ts_queue_video, ts_dequeue, ts_render)
            # print(ts_pts, ts_queue, ts_dequeue, ts_render)
            try:
                to_decode = int(ts_queue) - int(ts_got)
                decode_time = int(ts_dequeue) - int(ts_queue)
                to_render = int(ts_render) - int(ts_dequeue)
                total_time = int(ts_render) - int(ts_got)
                print("{0}, '{1}, '{2}, '{3}, '{4}, {5}, {6}, {7}, {8}".format(ts_pts, ts_got, ts_queue,
                                                                           ts_dequeue, ts_render,
                                                                           to_decode, decode_time,
                                                                           to_render, total_time),
                    file=f)
            except:
                f_discard.write("{0}, '{1}, '{2}, '{3}, '{4}, {5}, {6}, {7}, {8}\n".format(ts_pts, ts_got, ts_queue,
                                                                           ts_dequeue, ts_render,
                                                                           to_decode, decode_time,
                                                                           to_render, total_time));
   # with open(csv_filename_got, 'r+', encoding='utf8',newline='') as csvfile_got, open(csv_filename_all, 'w', encoding='utf8',newline='') as csvfile_all:
   #     writer = csv.writer(csvfile_all, delimiter=",")
   #     reader = csv.reader(csvfile_got, delimiter=",")
   #     head = ['describe', 'ts_pts', 'ts_got', 'ts_decoded', 'ts_torende', 'decode_time', 'to_render_time', 'total_time']
   #     writer.writerow(head)


def log_from_tecent(root_dir):
    unzip_dir =  root_dir + "/log_from_zip/"
    
    if os.path.isdir(unzip_dir):
        print("deleting dir "+unzip_dir)
        shutil.rmtree(unzip_dir)
        print("done")

    os.mkdir(unzip_dir)

    for list in os.listdir(root_dir):
        # if list.find("_log") == -1:
        #     continue
        filename = os.path.join(root_dir, list, 'log.zip')
        if zipfile.is_zipfile(filename):
            tag_dir = os.path.join(unzip_dir, list.split("_", 1)[1])
            print(tag_dir)
            if os.path.isdir(tag_dir):
                pass
            else:
                os.mkdir(tag_dir)
            un_zip(filename, tag_dir)

    log_from_mine(root_dir)


def split_log_file(dir, filename, keyword):
    in_filename = os.path.join(dir, filename)
    bit_rates = ["300KB", "400KB", "500KB", "1MB"]
    out_filename = [os.path.join(dir, bit_rate) for bit_rate in bit_rates]
    i = 0
    f = open(out_filename[i], 'w+', encoding='utf8',errors='ignore',newline='')

    f_in = open(in_filename, 'rb')
    result = chardet.detect(f_in.readline())
    print(result['encoding'])
    content = []
    for line in open(in_filename, 'r', encoding='utf8',errors='ignore',newline=''):
        if line.find(keyword) == -1:
            content.append(line)
            # f.writelines(line)
        else:
            for line in content:
                f.write(line)
            content = []
            f.close()
            i += 1
            if i >= len(out_filename):
                break
            f = open(out_filename[i], 'w+', encoding='utf8',errors='ignore',newline='')
    for line in content:
        f.write(line)
    f.close()
    return out_filename


def analyze_log(in_filename, result_dir):
    csv_filename_got = os.path.join(result_dir, os.path.basename(in_filename) + '.got.csv')
    keyword = "frame_process(got)"
    extract_and_format(in_filename, csv_filename_got, keyword)

    csv_filename_queue = os.path.join(result_dir, os.path.basename(in_filename) + '.queue.csv')
    keyword = "frame_process(queue)"
    extract_and_format(in_filename, csv_filename_queue, keyword)

    csv_filename_dequeue = os.path.join(result_dir, os.path.basename(in_filename) + '.dequeue.csv')
    keyword = "frame_process(dequeue)"
    extract_and_format(in_filename, csv_filename_dequeue, keyword)

    csv_filename_video = os.path.join(result_dir, os.path.basename(in_filename) + '.video.csv')
    keyword = "frame_process(video)"
    extract_and_format(in_filename, csv_filename_video, keyword)

    csv_filename_all = os.path.join(result_dir, os.path.basename(in_filename) + '.all.csv')
    filename_discard = os.path.join(result_dir, os.path.basename(in_filename) + '.discard.csv')

    if os.path.exists(csv_filename_got):
        frame_proccess_data(csv_filename_got, csv_filename_queue, csv_filename_dequeue, csv_filename_video, csv_filename_all,
                            filename_discard)
        # log2csv(out_filename, csv_filename)


def analyze_data(src_dir, result_dir):
    for lists in os.listdir(src_dir):
        tag_dir = os.path.join(src_dir, lists)
        out_dir = os.path.join(result_dir, lists)
        os.mkdir(out_dir)
        print(tag_dir)

        files = split_log_file(tag_dir, "log.txt", "monstartup already called")
        for file in files:
            analyze_log(file, out_dir)


def mydraw(data_file, headers):
    with open(data_file, 'r', encoding='utf8', newline='') as f:
        r_csv = csv.DictReader(f)
        field_value = ['start_1', 'start_2', 'consume_102', 'start_3', 'consume_201', 'start_4', 'got_frame']
        field_lable = [u'开始启动', u'测速完成', u'片头播放完成', u'拿到cid', u'成功连接SaaS', u'getCloudService成功', u'拿到流地址', u'拿到第一帧']
        for r in r_csv:
            print(r)
            print(len(field_value))
            valuesum = 0
            myploty = [0]
            for key in field_value:
                if r[key]:
                    valuesum += int(r[key])
                    myploty.append(valuesum)
                else:
                    myploty.append(0)
            print(myploty)
            myplotx = range(len(myploty))
            # myplotx = [datestr2num(i) for i in field_value]
            if myploty[1] and myploty[2] and myploty[3]:
                plt.plot(myplotx, myploty, 'b-', linewidth=1)
            else:
                plt.plot(myplotx, myploty, 'r-', linewidth=1)
            # plt.xticks(['测速', '端上处理', 'gedCID'])
            # plt.xlabel()
        ax = plt.gca()
        # ax.xaxis.set_major_formatter(FuncFormatter(field_value))
        plt.ylabel(u'每个阶段耗时(ms)')
        plt.xlabel(u'各阶段')
        plt.rcParams['font.sans-serif'] = ['SimHei']    #用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        ymajorLocator = MultipleLocator(5000)  # 将y轴主刻度标签设置为0.5的倍数
        # ymajorFormatter = FormatStrFormatter('%1.1f')  # 设置y轴标签文本的格式
        yminorLocator = MultipleLocator(500)  # 将此y轴次刻度标签设置为0.1的倍数
        # 设置主刻度标签的位置,标签文本的格式

        ax.yaxis.set_major_locator(ymajorLocator)
        # ax.yaxis.set_major_formatter(ymajorFormatter)

        # 显示次刻度标签的位置,没有标签文本
        ax.yaxis.set_minor_locator(yminorLocator)

        ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
        ax.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度
        # 有中文出现的情况，需要u'内容'
        plt.plot([0], [0], 'b-', label=u'正常播流')
        plt.plot([0], [0], 'r-', label=u'切换码率')
        plt.legend()
        xticks(np.arange(len(myploty)), field_lable, rotation=45)
        # plt.xticks(roataion=45)
        plt.show()


def business_proccess(result_dir, file_suffix):

    result_file = os.path.join(result_dir, 'analyze.csv')

    headers = ['request_104', 'response_104', 'request_108', 'response_108', 'user_start',
               'speed_test', 'speed_value', 'request_102', 'response_102', 'request_201', 'response_201',
               'getCloudService', 'op_10', 'op_5', 'got_first_frame', 'codec', 'request_202',
               'response_202', 'consume_104', 'consume_108', 'start_1', 'start_2', 'consume_102', 'start_3',
               'consume_201', 'start_41', 'start_42', 'start_4', 'got_frame', 'consume_202']

    with open(result_file, 'w',encoding='utf8', newline='') as outfile:
        f_csv = csv.DictWriter(outfile, headers)
        f_csv.writeheader()

        for lists in os.listdir(result_dir):
            if lists.find(file_suffix) != -1:
                business_file = os.path.join(result_dir, lists)
                with open(business_file, 'r', encoding="utf8") as infile:
                    dict1 = {i: None for i in headers}
                    for line in infile:
                        line = line.strip('\n')
                        line = line.strip('\r')
                        mylist = line.split(',', line.count(','))
                        for item in headers:
                            if mylist[0].find(item) != -1:
                                if dict1[item] != None:
                                    f_csv.writerow(dict1)
                                    dict1 = {i: None for i in headers}
                                dict1.update({item: mylist[1]})
                                if item == "speed_test":
                                    dict1.update({'speed_value': mylist[2]})
                                if item == "getCloudService":
                                    dict1.update({'op_10': mylist[2]})
                                    dict1.update({'op_5': mylist[3]})
                                if item == "got_first_frame":
                                    dict1.update({'codec': mylist[3]})
                                break
                    f_csv.writerow(dict1)

    tempfile = NamedTemporaryFile('r+', encoding='utf8', newline='', delete=False)
    field_value = [('consume_104', 'request_104', 'response_104'),
                   ('consume_108', 'request_108', 'response_108'),
                   ('start_1', 'user_start', 'speed_test'),
                   ('start_2', 'speed_test', 'request_102'),
                   ('consume_102', 'request_102', 'response_102'),
                   ('start_3', 'response_102', 'request_201'),
                   ('consume_201', 'request_201', 'response_201'),
                   ('start_41', 'response_201', 'op_10'),
                   ('start_42', 'op_10', 'op_5'),
                   ('start_4', 'response_201', 'op_5'),
                   ('got_frame', 'op_5', 'got_first_frame'),
                   ('consume_202', 'request_202', 'response_202')]
    with open(result_file, 'r+', encoding='utf8', newline='') as f, tempfile:
        r_csv = csv.DictReader(f)
        w_csv = csv.DictWriter(tempfile, headers)
        w_csv.writeheader()
        for r in r_csv:
            for key, key1, key2 in field_value:
                if r[key1] and r[key2]:
                    r[key] = int(r[key2]) - int(r[key1])
            w_csv.writerow(r)
    shutil.move(tempfile.name, result_file)

    mydraw(result_file, headers)



def analyze_business(tag_dir, result_dir):
    file_suffix = '.business.csv'
    for lists in os.listdir(tag_dir):
        in_filename = os.path.join(tag_dir, lists, 'log.txt')
        print(in_filename)
        business_file = os.path.join(result_dir, lists + file_suffix)
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
                        str1, str2 = line.split("CloudTest>>", 1)
                        str2 = str2.replace(' ', '')
                        str2 = str2.replace(":", ",")
                        outfile.write(str2)
                outfile.close()
        else:
            print(in_filename + " ========> no this file")

    if os.path.exists(result_dir):
        business_proccess(result_dir, file_suffix)


def log_from_mine(root_dir):

    unzip_dir = root_dir + "/log_from_zip/"
    result_dir = root_dir + "/log_result/"
    
    if os.path.isdir(result_dir):
        print("deleting dir "+result_dir)
        shutil.rmtree(result_dir)
        print("done")

    os.mkdir(result_dir)

    analyze_data(unzip_dir, result_dir)
    # analyze_business(unzip_dir, result_dir)

    # for lists in os.listdir(root_dir):
    #     path = os.path.join(root_dir, lists)
    #     if os.path.isdir(path):
    #         print(path)
    #         tag_dir = os.path.join(unzip_dir, lists)
    #         # analyze_data(tag_dir, result_dir)


def log_for_one():
    root_dir = r'C:\Users\lenovo\Downloads\cloudTest4\other'
    base_dir = u'motorola_Moto M_6.0'
    src_dir = root_dir + '\log_from_zip'
    result_dir = root_dir + '\log_result'

    out_dir = os.path.join(result_dir, base_dir)
    tag_dir = os.path.join(src_dir, base_dir)

    print(src_dir)
    print(tag_dir)
    print(out_dir)

    # bit_rates = ["1MB", "500KB", "400KB", "300KB"]
    # bit_rates = ["1MB", "500KB"]
    # files = [os.path.join(tag_dir, bit_rate) for bit_rate in bit_rates]
    files = split_log_file(tag_dir, "log.txt", "ffp_toggle_buffering: completed: OK")

    for file in files:
        analyze_log(file, out_dir)


def main(name):
    tecentDir = r'C:\Users\lenovo\Downloads\cloudtest4\gionee'
    myDir = r'C:\Users\lenovo\Downloads\cloudtest4\samsung'
    # log_from_tecent(tecentDir)
    # log_from_mine(myDir)
    log_for_one()


if __name__ == '__main__':
    import sys
    main(*sys.argv)