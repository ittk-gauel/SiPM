#!/usr/bin/env python
# coding: utf-8

import sys
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
warnings.simplefilter('ignore')


# Data set
parser = argparse.ArgumentParser()

parser.add_argument(
        "--input-file",
        "-i",
        dest="input_file",
        type=str,
        required=True,
        help=".npy file ")

args = parser.parse_args()

data = args.input_file

# Parameter
F = 25
alpha = 1
density = 0
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


# Data Analysis
d = np.load(data)
time = d[0]
current = d[1:]
print(current)
R = 50
n = 0

for i in current:
    if n == 0:
        t = list(time)
        v = list(i * R)
    elif n != 0:
        t.extend(time)
        v.extend(i*R)
    n += 1
    
N = int(len(time))
print('Number of bins: %s' % N)

fig = plt.figure()
ax = fig.add_subplot(111)

h = []
H = ax.hist2d(t,v,bins=N,cmap=cm.jet,norm=matplotlib.colors.LogNorm())        
ax.set_xlabel('Time [ns]', fontsize=F)
ax.set_ylabel('Voltage [mV]', fontsize=F)
cb = fig.colorbar(H[3],ax=ax)
cb.set_label('Counts',size=F)
cb.ax.tick_params(labelsize=F) 
plt.xlim(np.min(time),np.max(time))
plt.tick_params(labelsize=F)
plt.tight_layout()

save_path = data.replace('.npy','.png')
plt.savefig(save_path, dpi=200, bbox_inches="tight", pad_inches=0.2)
print('Output:', save_path)

#plt.show()
plt.close()


