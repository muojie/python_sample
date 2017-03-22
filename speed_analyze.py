#!/usr/bin/python3
# -*- coding:utf8 -*-
import word
import os
import shutil
import pandas
import numpy
import matplotlib.pyplot as plt
import seaborn


def analyze_speed(in_filename, file_pre, keyword, ax=None):
    business_file = file_pre + '.' + keyword + '.csv'
    if os.path.exists(in_filename):
        with open(in_filename, 'r', encoding="utf8") as infile, open(business_file, 'w') as outfile:
            headers = 'str, value, value_kb\n'
            outfile.write(headers)
            for line in infile:
                copy = False
                if line.find(keyword) != -1:
                    copy = True
                if copy:
                    str1, str2 = line.split("CloudTest>>", 1)
                    str2 = str2.replace(' ', '')
                    str2 = str2.replace(":", ",")
                    outfile.write(str2)
            outfile.close()
        speed_data = pandas.read_csv(business_file)
        speed_data.columns = ["str", "value", "value_kb"]
        speed_data["value_kb"] = speed_data["value"].map(lambda x: int(int(x)/1024))
        speed_data.to_csv(business_file)
        print(speed_data[:3])

        if ax:
            if keyword.find('total') == -1:
                ax.set_title(u'每单位时间实时网速')
            else:
                ax.set_title(u'每单位时间平均网速')
            ax.set_ylabel(u'网速(kb/s)')
            ax.set_xlabel(u'时间轴(30ms)')
            ax.bar(range(0, len(speed_data["value_kb"])), speed_data["value_kb"])
        else:
            if keyword.find('total') == -1:
                plt.title(u'每单位时间实时网速')
            else:
                plt.title(u'每单位时间平均网速')
            plt.ylabel(u'网速(kb/s)')
            plt.xlabel(u'时间轴(30ms)')
            plt.bar(range(0, len(speed_data["value_kb"])), speed_data["value_kb"])

        # plt.show()
        #
        # plt.hist(speed_data["value"], bins=len(speed_data["value"]))
        # seaborn.distplot(speed_data["value"], bins=len(speed_data["value"]))
        # plt.show()
    else:
        print(in_filename + " ========> no this file")

def speed_test(data_dir):
    unzip_dir = data_dir + "/log/"
    result_dir = data_dir + "/log_result/"

    if os.path.isdir(result_dir):
        print("deleting dir " + result_dir)
        shutil.rmtree(result_dir)
        print("done")

    os.mkdir(result_dir)

    for lists in os.listdir(unzip_dir):
        in_filename = os.path.join(unzip_dir, lists, 'log.txt')
        print(in_filename)
        file_pre = os.path.join(result_dir, lists)

        if os.path.exists(in_filename):
            #参考：http://matplotlib.org/examples/pylab_examples/subplots_demo.html
            f, (ax1, ax2) = plt.subplots(2, sharex=True)
            analyze_speed(in_filename, file_pre, "speed_test_time", ax1)
            analyze_speed(in_filename, file_pre, "speed_test_total", ax2)
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
            plt.show()


def main(name):
    myDir = r'C:\Users\lenovo\Desktop\cloudtest\spped_test'
    speed_test(myDir)


if __name__ == '__main__':
    import sys
    main(*sys.argv)