#!/usr/bin/env python
# coding: utf-8
#平均波形を計算し、比べる

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

data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_33_082840_A3_52.npy'


# Data Analysis
d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='52V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_34_082851_A3_52.5.npy'


d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='52.5V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_35_082914_A3_53.npy'


d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='53V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_36_082931_A3_53.5.npy'

d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='53.5V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_37_082948_A3_54.npy'


d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='54V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_38_083012_A3_54.5.npy'

d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='54.5V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_39_083035_A3_55.npy'

d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='55V')



data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_40_083053_A3_55.5.npy'

d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='55.5V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_41_083119_A3_56.npy'

d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='56V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_42_083134_A3_56.5.npy'

d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列　
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='56.5V')


data = '/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-05-24_44_083216_A3_57.npy'

d = np.load(data)     #npy file を読み込んで、読み込まれた値を格納した配列(array)を返す
time = d[0]             #読まれた配列の一行目が時間
current = d[1:]         #二行目以降が電流 currentは行列
R = 50                  #オシロスコープの抵抗
n = int(len(current[0:,0]))
N = int(len(time))
average_current = np.mean(current,axis=0)


print('Number of events: %s' %n)
print('Number of bins: %s' % N)     #1event（一発の光子）で出る波形を何点とっているか

plt.plot(list(time),list(average_current * 50), linewidth=1,label='57V')



plt.title('Average Wave Form of %s events' %n, fontsize=20)
plt.legend()

'''
save_path = data.replace('.npy','_av.png')
plt.savefig(save_path, dpi=200, bbox_inches="tight", pad_inches=0.2)
print('Output:', save_path)
'''


plt.show()