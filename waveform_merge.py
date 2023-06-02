#!/usr/bin/env python
# coding: utf-8
#平均波形を計算し、比べる
#waveform_merge.py filename biasvoltage filename biasvoltage ....

import numpy as np
from glob import glob
import math
import matplotlib.pyplot as plt
from natsort import natsorted
import os
import re
import sys
import xml.etree.ElementTree as ET
import warnings
import matplotlib.cm as cm
import matplotlib.colors
from scipy.optimize import curve_fit
warnings.simplefilter('ignore')


plt.rcParams['font.family'] = 'Times New Roman' # font familyの設定
plt.rcParams['mathtext.fontset'] = 'stix' # math fontの設定
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams["figure.figsize"] = (16,9)
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
plt.xlabel('Time(ns)', fontsize=20)
plt.ylabel('Voltage(mV)', fontsize=20)
plt.tick_params(labelsize=15)


args = sys.argv

size = 2

for data, voltage in (args[start:start + size] for start in range(1, len(args), size)):
    d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
    time = d[0]             #読まれた配列の一行目が時間
    current = d[1:]         #二行目以降が電流 currentは行列　
    R = 50                  #オシロスコープの抵抗
    n = int(len(current))
    N = int(len(time))
    average_current = np.mean(current,axis=0)
    print('Number of events: %s' %n)
    print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか
    plt.plot(list(time),list(average_current * 50), linewidth=1,label=voltage)


plt.title('Average Wave Form of %s events' %n, fontsize=20)
plt.legend()

'''
save_path = data.replace('.npy','_av.png')
plt.savefig(save_path, dpi=200, bbox_inches="tight", pad_inches=0.2)
print('Output:', save_path)
'''


plt.show()