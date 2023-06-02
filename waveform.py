#!/usr/bin/env python
# coding: utf-8
# waveform.py -i .Wfm.bin file
#Wfm.bin fileをnpy fileに変換せずに直接波形を出力する
#平均波形の計算

import numpy as np
from glob import glob
import math
import matplotlib.pyplot as plt
from natsort import natsorted
import os
import re
import xml.etree.ElementTree as ET
import warnings
import matplotlib.cm as cm
import matplotlib.colors
from scipy.optimize import curve_fit
import argparse
import struct
warnings.simplefilter('ignore')


def f2d(value):
    return struct.unpack('!f',bytes.fromhex(value))[0]


def transfer(s,k,j) : #sはbinary file
    i = 0
    v = []
    while i < j :
        a = hex(s[4*k]).lstrip("0x")
        a = a.zfill(2)
        b = hex(s[4*k+1]).lstrip("0x")
        b = b.zfill(2)
        c = hex(s[4*k+2]).lstrip("0x")
        c = c.zfill(2)
        d = hex(s[4*k+3]).lstrip("0x")
        d = d.zfill(2)
        v0 = d + c + b + a #LE
        v0 = f2d(v0)
        v.append(v0*1000) #mV
        k += 1
        i += 1
    return v,k


def ampere(v) :
    r = 50 #Ω
    c = []
    for i in v :
        c.append(i/r) #mA
    return c


def calculate(s,N,signal_record_length,skip_data):
    n = 0
    k = 2 #最初のイベントはバグるから
    I = []
    for n in range(N) :
        v,k = transfer(s,k,signal_record_length)
        c = ampere(v)
        I.append(c)
        k += skip_data
        n += 1
    return I #mA


# Data set
parser = argparse.ArgumentParser()

parser.add_argument(
        "--input-file",
        "-i",
        dest="input_file",
        type=str,
        required=True,
        help=".npy file ")
parser.add_argument(
        "--number-of-events",
        "-n",
        dest="number_of_events",
        type=int,
        default=100,
        help='number of events')


args = parser.parse_args()

data = args.input_file

config = data.replace('.Wfm.bin','.xml')
tree = ET.parse(config) 
root = tree.getroot() 

for child in root.iter('Prop') : 
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


t = np.linspace(0,record_time,signal_record_length) 
x = t * 10**9 #ns

# Detailed Parameter
N = args.number_of_events #number of events


g = open(data, 'rb') #binary fileの読み込みのために'rb'
binary = g.read() #ここで読み込んでいるのはWfm.bin file

d = []

c = calculate(binary, N, signal_record_length, skip_data)
d.append(x) #時間データの格納
cur = np.array(c) #変換データの格納
d.extend(cur)

time = d[0]
current = d[1:]


R = 50                  #オシロスコープの抵抗
n = int(len(current))
N = int(len(time))
average_current = np.mean(current,axis=0)

print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか


# Parameter
plt.rcParams['font.family'] = 'Times New Roman' # font familyの設定
plt.rcParams['mathtext.fontset'] = 'stix' # math fontの設定
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams["figure.figsize"] = (20,9)
plt.rcParams["xtick.major.width"] = 1.2 
plt.rcParams["ytick.major.width"] = 1.2 
plt.rcParams["xtick.minor.width"] = 1.0             #x軸補助目盛り線の線幅
plt.rcParams["ytick.minor.width"] = 1.0             #y軸補助目盛り線の線幅
plt.rcParams["xtick.major.size"] = 20               #x軸主目盛り線の長さ
plt.rcParams["ytick.major.size"] = 20               #y軸主目盛り線の長さ
plt.rcParams["xtick.minor.size"] = 10               #x軸補助目盛り線の長さ
plt.rcParams["ytick.minor.size"] = 10               #y軸補助目盛り線の長さ
plt.rcParams['xtick.top'] = True                   #x軸の上部目盛り
plt.rcParams['ytick.right'] = True                 #y軸の右部目盛り
plt.title('Average Wave Form of %s events' %n, fontsize=20)
plt.xlabel('Time(ns)', fontsize=20)
plt.ylabel('Voltage(mV)', fontsize=20)
plt.plot(list(time),list(average_current * 50), linewidth=1)
plt.tick_params(labelsize=15)


save_path = data.replace('.Wfm.bin','.png')
plt.savefig(save_path, dpi=200, bbox_inches="tight", pad_inches=0.2)
print('Output:', save_path)



plt.show()




