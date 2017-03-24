#!/usr/bin/python3
# -*- coding:utf8 -*-
import word
import os
import shutil
import pandas
import numpy
import matplotlib.pyplot as plt
import seaborn


def getxy(data, start, end):
    x = [0]
    y = [0]
    lenght = len(data)
    if lenght < end:
        return None

    # print(data)
    x1 = int(end/4)
    y1 = int(sum(data[start:x1])/(x1-start))
    # print(data[start:x1])
    x.append(x1)
    y.append(y1)
    x2 = end-2
    y2 = int(sum(data[x1:x2])/(x2-x1))
    # print(data[x1:x2])
    x.append(x2)
    y.append(y2)
    x3 = end
    y3 = int(sum(data[x2:end])/(x3-x2))
    # print(data[x2:end])
    x.append(x3)
    y.append(y3)
    print("getxy", x, y, x1, y2)
    return x, y, x1, y2


def analyze_speed(in_filename, file_pre, keyword):
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
        return speed_data["value_kb"]
    else:
        print(in_filename + " ========> no this file")


def mydraw3plot(data1, data2, data3):
    # 参考：http://matplotlib.org/examples/pylab_examples/subplots_demo.html
    ax1 = ax2 = ax3 = None
    if data1 is not None and len(data1):
        if data2 is not None and len(data2):
            if data3 is not None and len(data3):
                f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
            else:
                f, (ax1, ax2) = plt.subplots(2, sharex=True)
        else:
            f, (ax1) = plt.subplots(1)

    if ax1 is not None:
        ax1.set_title(u'每单位时间平均网速')
        # ax1.set_ylabel(u'网速(kb/s)')
        # ax1.set_xlabel(u'时间轴(30ms)')
        ax1.plot([0], [0], 'r-', label=u'最后平均网速' + str(data1[len(data1) - 1]))
        ax1.bar(range(0, len(data1)), data1)
        ax1.legend()

    if ax2 is not None:
        ax2.set_title(u'每单位时间实时网速')
        ax2.bar(range(0, len(data2)), data2)
        ax2.legend()

    if ax3 is not None:
        sorteddata = sorted(data3)
        ax3.set_title(u'排序后的实时网速')
        xs, ys, x, y = getxy(sorteddata, 0, len(sorteddata))
        ax3.bar(range(0, len(sorteddata)), sorteddata)
        ax3.text(x, y, r'排序，去掉最大的两个，去掉最小的1/4，剩下的求平均值： ' + str(y) + 'kbps', color="red")
        ax3.step(xs, ys, lw=2, color="red")

        if ax2 is not None:
            xs = []
            ys = []
            ax2.plot([0], [0], 'r-', label=u'该时间段内的网速（使用speedtest算法计算）')
            for x in [33 * i for i in range(1, 100)]:
                print("sorted, len: ", len(data2), ", x= ", x)
                if x <= len(data2):
                    sorteddata = sorted(data2[0:x])
                    xx, yy, avgx, y = getxy(sorteddata, 0, len(sorteddata))
                    if len(ys) == 0:
                        print("--------------------")
                        xs.append(0)
                        ys.append(y)
                    xs.append(x)
                    ys.append(y)
                    ax2.step([x - 20, x, x], [y, y, 0], lw=2, color="red")
                    ax2.text(x - 20, y, y, color="red")
                else:
                    break


def speed_test(data_dir):
    result_dir = data_dir + "_result/"

    if os.path.isdir(result_dir):
        print("deleting dir " + result_dir)
        shutil.rmtree(result_dir)
        print("done")

    os.mkdir(result_dir)

    for lists in os.listdir(data_dir):
        in_filename = os.path.join(data_dir, lists, 'log.txt')
        print(in_filename)
        file_pre = os.path.join(result_dir, lists)

        x_units, title = lists.split("ms_", 1)
        if x_units is None:
            x_units = 30

        if os.path.exists(in_filename):
            data1 = analyze_speed(in_filename, file_pre, "speed_test_total")
            data2 = analyze_speed(in_filename, file_pre, "speed_test_time")
            mydraw3plot(data1, data2, None)

            plt.ylabel(u'网速(kb/s)')
            plt.xlabel(u'时间轴(' + x_units + 'ms)')
            plt.suptitle(title + u'限速', fontsize=18, fontweight='bold')
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

            plt.show()


def main(name):
    myDir = r'C:\Users\lenovo\Desktop\cloudtest\spped_test\log_wifi_saas'
    speed_test(myDir)


if __name__ == '__main__':
    import sys
    main(*sys.argv)