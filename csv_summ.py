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
import pandas as pd
from pylab import *
import re
import xlrd

import glob
from xlsxwriter.workbook import Workbook

BIT_RATES = ["1MB", "500KB", "400KB", "300KB"]
CSV_FILES = [bit_rate + ".all.csv" for bit_rate in BIT_RATES]
SUMMARY_CSV = 'summary.csv'
SUMMARY_DIR = 'summary'
CSV_HEAD = u"码率,解码平均耗时,总平均耗时,解码器,品牌,型号,系统版本,API,color-format,overlay-format"


def average(list):
    total = 0
    num = 0
    for item in list:
        total += int(item)
        num += 1
    if num == 0:
        return 0
    return total / num


def summary_csv(src, brand, info):
    f_w = open(os.path.join(src, SUMMARY_CSV), 'w+', encoding='utf8',newline='')
    print(CSV_HEAD, file=f_w)
    for file, bit_rate in zip(CSV_FILES, BIT_RATES):
        file_name = os.path.join(src, file)
        if os.path.exists(file_name):
            # print(file_name)
            # lc = pd.DataFrame(pd.read_csv(file_name, header=0))
            # print(bit_rate + "," + str(lc[' decode_time'].mean()) + "," + str(lc[' total_time'].mean()), file=f_w)
            decode_time = []
            total_time = []
            with open(file_name, 'r+', encoding='utf8', newline='') as f:
                r_csv = csv.DictReader(f)
                for r in r_csv:
                    decode_time.append(r[' decode_time'])
                    total_time.append(r[' total_time'])
            dir_name = os.path.basename(src)
            model = dir_name
            osVersion = ''
            # for CloudTest3 start
            # if(dir_name.count("_") ==2):
            #     brand, model, osVersion = dir_name.split("_", dir_name.count("_"))
            # else:
            #     print("error name: " + dir_name + " count:" + str(dir_name.count("_")))
            # end
            print(bit_rate + "," + str(average(decode_time)) + "," + str(average(total_time)) + "," + info[0] + "," +
                  brand + "," + model + "," + osVersion + ',' + info[1] + ',' + info[2] + ',' + info[3], file=f_w)
        else:
            print(file_name)
    f_w.close()


def summary_all_csv(src, dst):
    # summary to csv
    for list in os.listdir(src):
        if list == SUMMARY_DIR:
            continue
        path = os.path.join(src, list)
        if os.path.isdir(path):
            summary_all_csv(path, dst)
        elif os.path.basename(path) == SUMMARY_CSV:
            with open(path, 'r+', encoding='utf8', errors='ignore', newline='') as f:
                reader = csv.reader(f)
                next(reader, None)
                writer = csv.writer(dst)
                for row in reader:
                    writer.writerow(row)


# def cal_csv(out_dir, infile):
#     for bit in BIT_RATES:
#         dir = os.path.join(out_dir, SUMMARY_DIR, bit)
#         os.mkdir(dir)
#     with open(infile, 'r+', encoding='utf8', newline='') as f:
#         r_csv = csv.DictReader(f)
#         for r in r_csv:
#             for bit, myploty in zip(BIT_RATES, myplotys):
#                 if (r[u'码率'] == bit):
#                     myploty.append(r[u'解码平均耗时'])
#                     print(file, r[u'码率'], r[u'解码平均耗时'])
#                     break



def summary_xlsx(src, dst):
    # summary to xlsx
    for list in os.listdir(src):
        if list == SUMMARY_DIR:
            print(list)
            continue
        path = os.path.join(src, list)
        if os.path.isdir(path):
            summary_xlsx(path, dst)
        elif os.path.basename(path) == SUMMARY_CSV:
            workbook = Workbook(os.path.join(dst, os.path.basename(src) + '.xlsx'))
            for csv_name in CSV_FILES+[SUMMARY_CSV]:
                csv_file = os.path.join(src, csv_name)
                if os.path.exists(csv_file):
                    worksheet = workbook.add_worksheet(csv_name.split(".")[0])

                    with open(csv_file, 'r', encoding='utf8',errors='ignore',newline='') as f:
                        reader = csv.reader(f)
                        for r, row in enumerate(reader):
                            for c, col in enumerate(row):
                                worksheet.write(r, c, col)
            workbook.close()

    # copy
    # files = glob.glob(os.path.join(src, "*.xlsx"))
    # if len(files) > 1:
    #     print("error(len > 1): " + files)
    # for file in files:
    #     shutil.copy(file, dst)


def cal_number(lists, min, max):
    number = 0
    for i in lists:
        if float(i)>min and float(i)<=max:
            number+=1
    return number


def mydraw4plot(data1, data2, data3, data4):
    # 参考：http://matplotlib.org/examples/pylab_examples/subplots_demo.html
    ax1 = ax2 = ax3 = ax4 = None
    # if data1 is not None and len(data1):
    #     if data2 is not None and len(data2):
    #         if data3 is not None and len(data3):
    #             if data4 is not None and len(data4):
    #                 f, axes = plt.subplots(nrows=2,ncols=2, sharex=True, sharey=True)
    #                 ax1 = axes[0, 0]
    #                 ax2 = axes[0, 1]
    #                 ax3 = axes[1, 0]
    #                 ax4 = axes[1, 1]
    #             else:
    #                 f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
    #         else:
    #             f, (ax1, ax2) = plt.subplots(2, sharex=True)
    #     else:
    #         f, (ax1) = plt.subplots(1)

    f, (ax1) = plt.subplots(1)

    axs = [ax1, ax1, ax1, ax1]
    datas = [data1, data2, data3, data4]
    colors = ['ro', 'gv', 'k<', 'b>']
    for ax, data, color, bitrate in zip(axs, datas, colors, BIT_RATES):
        if ax is not None:
            ax.set_title(u'平均解码时间分布')
            ax.plot(range(0, len(data)), data, color, label=bitrate, linewidth=1)

            # gathers = [[0, 40], [40, 80], [80, 120], [120, 160]]
            # for min, max in gathers:
            #     descr = u'解码时间在[' + str(min) + ',' + str(max) + u']ms区间的个数：' + str(cal_number(data, min, max))
            #     ax.plot([0], [0], 'b-', label=descr)
            # descr = u'解码时间>' + str(max) + u'ms的个数：' + str(cal_number(data, max, 100000))
            # ax.plot([0], [0], 'b-', label=descr)

            ax.legend()


def analyze_csv(dir):
    # for file in os.listdir(dir):
    #     if file.find(".xlsx") == -1:
    #         continue
    #     try:
    #         data = xlrd.open_workbook(os.path.join(dir, file))
    #         table = data.sheet_by_name(u'summary')
    #         if table.cell(0, 1).value == u'解码平均耗时':
    #             if table.cell(1, 0).value == u'1MB':
    #                 myploty.append(table.row(1)[1].value)
    #                 print(file, table.row(1)[1].value)
    #     except Exception as e:
    #         print(str(e))
    myploty1 = []
    myploty2 = []
    myploty3 = []
    myploty4 = []
    myplotys = [myploty1, myploty2, myploty3, myploty4]
    for list in os.listdir(dir):
        list_dir1 = os.path.join(dir, list, 'log_result')
        for list1 in os.listdir(list_dir1):
            list_dir2 = os.path.join(list_dir1, list1)
            for name in os.listdir(list_dir2):
                if name.find("summary.csv") == -1:
                    continue
                file = os.path.join(list_dir2, name)
                with open(file, 'r+', encoding='utf8', newline='') as f:
                    r_csv = csv.DictReader(f)
                    for r in r_csv:
                        for bit, myploty in zip(BIT_RATES, myplotys):
                            if (r[u'码率'] == bit):
                                myploty.append(r[u'解码平均耗时'])
                                print(file, r[u'码率'], r[u'解码平均耗时'])
                                break


    print(len(myploty1))
    print(len(myploty2))
    print(len(myploty3))
    print(len(myploty4))

    mydraw4plot(myploty1, myploty2, myploty3, myploty4)

    plt.ylabel(u'解码平均耗时(ms)')
    plt.xlabel(u'手机序号')
    # plt.suptitle(u'限速', fontsize=18, fontweight='bold')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    plt.show()


def get_codec_name(dir, base_dir):
    codec_name = ' '
    out_format = ' '
    overlay_format = ' '
    api_level = ' '
    file = os.path.join(dir, base_dir, "log.txt")
    if os.path.exists(file):
        with open(file, 'r', encoding="utf8") as infile:
            for line in infile:
                if codec_name!=' ' and out_format!=' ' and overlay_format!=' ' and api_level!=' ':
                    break
                if line.find("got_first_frame:") != -1:
                    list = line.strip().split(",")
                    if (len(list) == 3):
                        codec_name = list[2]
                    continue
                if line.find("IJKMEDIA:     color-format:") != -1:
                    list = line.strip().split("(")
                    if (len(list) == 2):
                        out_format = list[1].strip(')')
                    continue
                if line.find("fmt=_AMC vout=") != -1:
                    list = line.strip().split("fmt=_AMC vout=")
                    if (len(list) == 2):
                        overlay_format = list[1].strip(')')
                    continue
                if line.find("API-Level:") != -1:
                    list = line.strip().split("API-Level:")
                    if (len(list) == 2):
                        api_level = list[1]
                    continue
        print(file + " ========> codec name: " + codec_name + " color: " + out_format + " overlay: " + overlay_format)
    else:
        print(file + " ========> no this file")
    return codec_name,api_level,out_format,overlay_format


def main(name):
    tecentDir = r'C:\Users\lenovo\Desktop\tx_round_1'
    myDir = r'C:\Users\lenovo\Downloads\cloudTest2'
    # log_from_tecent(tecnetDir)

    rootDir = myDir
    baseDir = 'first32'
    workDir = os.path.join(rootDir, baseDir)

    unzip_dir = workDir + "/log_from_zip/"
    result_dir = workDir + "/log_result/"
    summary = False
    plt_csv = False
    generate_csv = True
    generate_xlsx = False

    # summary csv
    if summary:
        for list in os.listdir(result_dir):
            src_dir = os.path.join(result_dir, list)
            print(src_dir)
            codec = get_codec_name(unzip_dir, list)
            brand = re.sub(r'[^\D.]+', '', baseDir)
            summary_csv(src_dir, brand, codec)

    # analyze csv
    if plt_csv:
        analyze_csv(rootDir)

    # generate xlsx file
    if generate_csv:
        src_dir = rootDir
        out_dir = os.path.join(rootDir, SUMMARY_DIR, 'csv')
        if os.path.isdir(out_dir):
            print("deleting dir " + out_dir)
            shutil.rmtree(out_dir)
            print("done")
        os.mkdir(out_dir)
        f_w = open(os.path.join(out_dir, SUMMARY_CSV), 'w+', encoding='utf8', newline='')
        print(CSV_HEAD, file=f_w)
        summary_all_csv(src_dir, f_w)
        f_w.close()
        # cal_csv(out_dir, os.path.join(out_dir, SUMMARY_CSV))

    # generate xlsx file
    if generate_xlsx:
        src_dir = rootDir
        out_dir = os.path.join(rootDir, SUMMARY_DIR, 'xlsx')
        if os.path.isdir(out_dir):
            print("deleting dir " + out_dir)
            shutil.rmtree(out_dir)
            print("done")
        os.mkdir(out_dir)
        summary_xlsx(src_dir, out_dir)


if __name__ == '__main__':
    import sys
    main(*sys.argv)