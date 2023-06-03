#!/usr/bin/env python
# coding: utf-8

# Binary Data Converter
#convert.py -i input-file (-n number-of-events) (-s base-line-start-time) (-e base-line-stop-time)

import sys
import numpy as np
from glob import glob
import math
import matplotlib.pyplot as plt
from natsort import natsorted
import os
import re
import transform #binary analysis program → transform.py
import xml.etree.ElementTree as ET
import warnings
import argparse
import pathlib
import shutil
warnings.simplefilter('ignore')


def change_suffix (file_name, from_suffix, to_suffix):
    #ファイルの拡張子を得る
    sf = pathlib.PurePath(file_name).suffix
    
    #変更対象かどうか判断
    if sf == from_suffix:
        #ファイル名（拡張子を除く）を得る
        st = pathlib.PurePath(file_name).stem
        
        # 変更後のファイル名を得る
        to_name = st + to_suffix
        
        abspath = pathlib.PurePath(file_name)
        
        # ファイル名を変更する
        shutil.move(file_name, str(abspath.parent) + '/' + to_name)


# Data Set
# パーサーを作る
parser = argparse.ArgumentParser()

# 引数の追加
parser.add_argument(
        "--input-file",
        "-i",
        dest="input_file",
        type=str,
        required=True,
        help="binary file you want to convert into .npy file")
parser.add_argument(
        "--number-of-events",
        "-n",
        dest="number_of_events",
        type=int,
        default=100,
        help='number of events')
parser.add_argument(
        "--base-line-start-time",
        "-s",
        dest="base_line_start_time",
        type=int,
        default=0,
        help="base line start time")
parser.add_argument(
        "--base-line-stop-time",
        "-e",
        dest="base_line_stop_time",
        type=int,
        default=400,
        help="base line stop time")


args = parser.parse_args()
data = args.input_file #input_file


# Analysis Parameter
binaryfile = data.replace('.Wfm.bin','.bin')
change_suffix(binaryfile, '.bin', '.xml')
config = data.replace('.Wfm.bin','.xml')
tree = ET.parse(config) #xmlデータの読み込み
root = tree.getroot() #一番上の階層の要素を取り出す (Database)


for child in root.iter('Prop') : #iterは指定されたタグの要素を返すイテレータ
    Name = child.attrib["Name"]
    if Name == "Resolution" :
        time_resolution = float(child.attrib["Value"])
    if Name == "SignalRecordLength" :
        signal_record_length = int(child.attrib["Value"])
    if Name == "SignalHardwareRecordLength" :
       signal_hardware_record_length = int(child.attrib["Value"])



skip_data = int(signal_hardware_record_length - signal_record_length)
record_time = (signal_hardware_record_length - skip_data) * time_resolution
        
print('-----------------------------------------')
print('Time Resolution               = %s' % time_resolution)
print('Signal Record Length          = %s' % signal_record_length)
print('Signal Hardware Record Length = %s' % signal_hardware_record_length)
print('Skip Data                     = %s' % skip_data)
print('Record Time                   = %s ns' % round(record_time*10**9))
print('-----------------------------------------')

t = np.linspace(0,record_time,signal_record_length) #0~record_timeをsignal_record_length等分する
x = t * 10**9 #ns
t_max = np.max(x)
t_min = np.min(x)


# Detailed Parameter
N = args.number_of_events #number of events
tb1 = args.base_line_start_time #base line start time
tb2 = args.base_line_stop_time #base line stop time

# Binary Conversion as Current Data
d = []

# import binary data
g = open(data, 'rb') #binary fileの読み込みのために'rb'
s = g.read() #ここで読み込んでいるのはWfm.bin file

# binary convert and remove baseline
c = transform.calculate(s, x, N, signal_record_length, skip_data, tb1, tb2) 

d.append(x) #時間データの格納
cur = np.array(c) #変換データの格納
d.extend(cur)

save_path = data.replace('.Wfm.bin', '') 
np.save(save_path, d)
print('Output:', (save_path+'.npy'))
