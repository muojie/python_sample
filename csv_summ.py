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


def summary_csv(src, dst):
    bit_rates = ["1MB", "500KB", "400KB", "300KB"]
    csv_files = [bit_rate + ".all.csv" for bit_rate in bit_rates]
    out_file = os.path.join(dst, os.path.basename(src) + '.summary.csv')
    f_w = open(out_file, 'w+', encoding='utf8',newline='')
    print(u"码率,解码平均耗时,总平均耗时", file=f_w)
    for file, bit_rate in zip(csv_files, bit_rates):
        file_name = os.path.join(src, file)
        if os.path.exists(file_name):
            print(file_name)
            lc = pd.DataFrame(pd.read_csv(file_name, header=0))
            print(bit_rate + "," + str(lc[' decode_time'].mean()) + "," + str(lc[' total_time'].mean()), file=f_w)


def analyze_csv(result_dir):
    for list in os.listdir(result_dir):
        src_dir = os.path.join(result_dir, list)
        # out_dir = os.path.join(result_dir, "summary")
        # if os.path.isdir(out_dir):
        #     print( "deleting dir " +out_dir)
        #     shutil.rmtree(out_dir)
        #     print("done")
        # os.mkdir(out_dir)
        print(src_dir)

        summary_csv(src_dir, src_dir)


def csv_from_mine(root_dir):
    unzip_dir = root_dir + "/log_from_zip/"
    result_dir = root_dir + "/log_result/"
    analyze_csv(result_dir)
    # if os.path.isdir(result_dir):
    #     print( "deleting dir " +result_dir)
    #     shutil.rmtree(result_dir)
    #     print("done")
    #
    # os.mkdir(result_dir)


def main(name):
    tecentDir = r'C:\Users\lenovo\Desktop\tx_round_1'
    myDir = r'C:\Users\lenovo\PycharmProjects\python_sample\cloudtest\nubia\release0420'
    # log_from_tecent(tecnetDir)
    csv_from_mine(myDir)


if __name__ == '__main__':
    import sys
    main(*sys.argv)