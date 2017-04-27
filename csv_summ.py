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
import xlrd

import glob
from xlsxwriter.workbook import Workbook

BIT_RATES = ["1MB", "500KB", "400KB", "300KB"]
CSV_FILES = [bit_rate + ".all.csv" for bit_rate in BIT_RATES]
SUMMARY_CSV = 'summary.csv'


def average(list):
    total = 0
    num = 0
    for item in list:
        total += int(item)
        num += 1
    if num == 0:
        return 0
    return total / num


def summary_csv(src):
    f_w = open(os.path.join(src, SUMMARY_CSV), 'w+', encoding='utf8',newline='')
    print(u"码率,解码平均耗时,总平均耗时", file=f_w)
    for file, bit_rate in zip(CSV_FILES, BIT_RATES):
        file_name = os.path.join(src, file)
        if os.path.exists(file_name):
            print(file_name)
            # lc = pd.DataFrame(pd.read_csv(file_name, header=0))
            # print(bit_rate + "," + str(lc[' decode_time'].mean()) + "," + str(lc[' total_time'].mean()), file=f_w)
            decode_time = []
            total_time = []
            with open(file_name, 'r+', encoding='utf8', newline='') as f:
                r_csv = csv.DictReader(f)
                for r in r_csv:
                    decode_time.append(r[' decode_time'])
                    total_time.append(r[' total_time'])
            print(bit_rate + "," + str(average(decode_time)) + "," + str(average(total_time)), file=f_w)
    f_w.close()


def summary_xlsx(src, dst):
    # summary to xlsx
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


def analyze_csv(dir):
    myploty = []

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

    for list in os.listdir(dir):
        list_dir = os.path.join(dir, list)
        for name in os.listdir(list_dir):
            if name.find("summary.csv") == -1:
                continue
            file = os.path.join(list_dir, name)
            with open(file, 'r+', encoding='utf8', newline='') as f:
                r_csv = csv.DictReader(f)
                for r in r_csv:
                    if (r[u'码率'] == "1MB"):
                        myploty.append(r[u'解码平均耗时'])
                        print(file, r[u'码率'], r[u'解码平均耗时'])
                        break

    myplotx = range(len(myploty))
    plt.plot(myplotx, myploty, 'bo', linewidth=1)

    ax = plt.gca()
    # ax.xaxis.set_major_formatter(FuncFormatter(field_value))
    plt.ylabel(u'解码平均耗时(ms)')
    plt.xlabel(u'手机序号')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 有中文出现的情况，需要u'内容'
    gathers = [[0,40], [40,80], [80, 120], [120, 160]]
    for min, max in gathers:
        descr = u'解码时间在['+ str(min) + ',' + str(max) + u']ms区间的个数：' + str(cal_number(myploty, min, max))
        plt.plot([0], [0], 'b-', label=descr)
    descr = u'解码时间>' + str(max) + u'ms的个数：' + str(cal_number(myploty, max, 100000))
    plt.plot([0], [0], 'b-', label=descr)
    plt.legend()
    # xticks(np.arange(len(myploty)), field_lable, rotation=45)
    # plt.xticks(roataion=45)
    plt.show()


def csv_from_mine(root_dir):
    unzip_dir = root_dir + "/log_from_zip/"
    result_dir = root_dir + "/log_result/"
    summary = True
    plt_csv = True
    generate_xlsx = True

    # summary csv
    if summary:
        for list in os.listdir(result_dir):
            src_dir = os.path.join(result_dir, list)
            print(src_dir)
            summary_csv(src_dir)

    # analyze csv
    if plt_csv:
        analyze_csv(result_dir)

    # generate xlsx file
    if generate_xlsx:
        out_dir = os.path.join(result_dir, "../summary")
        if os.path.isdir(out_dir):
            print("deleting dir " + out_dir)
            shutil.rmtree(out_dir)
            print("done")
        os.mkdir(out_dir)
        for list in os.listdir(result_dir):
            src_dir = os.path.join(result_dir, list)
            print(src_dir)
            summary_xlsx(src_dir, out_dir)


def main(name):
    tecentDir = r'C:\Users\lenovo\Desktop\tx_round_1'
    myDir = r'C:\Users\lenovo\Downloads\cloudTest2\mi37'
    # log_from_tecent(tecnetDir)
    csv_from_mine(myDir)


if __name__ == '__main__':
    import sys
    main(*sys.argv)