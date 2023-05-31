#!/usr/bin/env python
# coding: utf-8

# Charge Histogram

import sys
import numpy as np
import pandas as pd
from glob import glob
import math
import matplotlib.pyplot as plt
import os
import re
import xml.etree.ElementTree as ET
from natsort import natsorted
from scipy.optimize import curve_fit
from scipy import stats
from scipy.stats import chi2
from matplotlib.ticker import ScalarFormatter
import matplotlib.cm as cm
import matplotlib.colors
import warnings
import argparse
warnings.simplefilter('ignore')


def mgauss(x, *params) :
    num_func = int(len(params)/3)
    g = []
    
    #mu = give_mu()
    
    for i in range(num_func) :
        amp = params[3 * i]
        ave = params[3 * i + 1]
        sig = params[3 * i + 2]
        #y = amp * np.exp(-((x - mu[i])/sig)**2)
        y = amp * np.exp(-((x - ave)/sig)**2)
        g.append(y)
        
    y_sum = np.zeros_like(x)
    
    for j in g :
        y_sum += j
        
    return y_sum


def gauss(x,a,b,c) :
    y = a * np.exp( -((x - b)/c)**2)
    return y


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
        "--integral-start-time",
        "-s",
        dest="integral_start_time",
        type=float,
        default=50,
        help='integral start time')
parser.add_argument(
        "--integral-stop-time",
        "-e",
        dest="integral_stop_time",
        type=int,
        default=250,
        help="integral stop time")

args = parser.parse_args()

data = args.input_file


# Integration Time
integ_start_time = args.integral_start_time
integ_stop_time = args.integral_stop_time

# Setting
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

# Parameter
F = 25
e = 1.602 * 10**(-7) #pC

# Defrost
d = np.load(data)
time = d[0]
current = d[1:]
dt = time[1] - time[0]

n = m = k = 0
charge = []

for i in time:
    if i >= integ_start_time and m == 0:
        n_start = n
        m = 1
    elif i >= integ_stop_time and k == 0:
        n_end = n - 1
        k = 1
    n += 1
    
for c in current:
    q = sum(c[n_start:n_end]) * dt
    charge.append(q)

bins = 150
z = plt.hist(charge,bins=bins)
x = list(z[1])
y = list(z[0])
plt.xlabel('Charge [pC]', fontsize=F)
plt.ylabel('Counts', fontsize=F)
plt.tick_params(labelsize=F)
plt.tight_layout()
plt.grid()

save_path = data.replace('.npy','_chargehisto_int%s-%sns.png' % (integ_start_time, integ_stop_time))
plt.savefig(save_path, dpi=200, bbox_inches="tight", pad_inches=0.2)
print('Output:', save_path)

#plt.show()
plt.close()

k = input('\nContinue:0\nExit:1\n>')

if k != '0' and k != '1':
    print('Error: You have to choose either 0 or 1 !')
    exit()

if k == '1':
    print('bye!')
    exit()

# Multi-gaussian fitting
if k == '0':

    ##################################
    # [amplitude, mu, sigma]
    g0 = [150, 0.00, 0.01]
    g1 = [300, 0.05, 0.01]
    g2 = [320, 0.1, 0.01]
    g3 = [250, 0.15, 0.01]
    g4 = [150,  0.20, 0.01]
    g5 = [100,  0.25, 0.01]
    ##################################
    
    guess = [g0, g1, g2, g3, g4, g5]
    guess_total = []

    for i in guess:
        guess_total.extend(i)

    y.append(0)
    popt, pcov = curve_fit(mgauss, x, y, p0=guess_total)
    perr = np.sqrt(np.diag(pcov))

    fit_x = np.linspace(np.min(x),np.max(x),10**4)
    fit = mgauss(fit_x, *popt)
    plt.plot(fit_x, fit, color='r', label='1 p.e. charge = %.5f' % popt[4])
    plt.hist(charge, bins=bins)
    plt.xlabel('Charge [pC]', fontsize=F)
    plt.ylabel('Counts', fontsize=F)
    plt.tick_params(labelsize=F)
    plt.tight_layout()
    plt.legend(fontsize=F)
    plt.grid()

    print('1 p.e. charge: %.3f [pC]' % popt[4])

    save_path = data.replace('.npy','_int%s-%sns_fitted.png' % (integ_start_time, integ_stop_time))
    plt.savefig(save_path, dpi=200, bbox_inches="tight", pad_inches=0.2)
    print('Output:', save_path)

    plt.show()
    #plt.close()



