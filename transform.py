#バイナリ変換して電流値として出力するプログラム
import numpy as np
import sys
import struct #binary dataを処理するためのモジュール
import math
import matplotlib.pyplot as plt


def f2d(value):
    return struct.unpack('!f', bytes.fromhex(value))[0] #bites型のbinaryデータを元の型に戻す !fはfloat 16進数→2進数→float


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
 

def ampere(v,vb) :
    r = 50 #Ω
    i = 0
    N = len(v)
    c = []
    for i in v :
        '''
        dv = (i-vb) #baseline引いているところ？
        '''
        c.append(i/r) #mA
        '''
        i += 1
        '''
    return c

def calculate(s,t,N,signal_record_length,skip_data,tb1,tb2) :
    n = 0
    k = 2 #最初のイベントはバグるから
    I = []
    for n in range(N) :
        v,k = transfer(s,k,signal_record_length)
        vb = base_line(t,v,tb1,tb2)
        c = ampere(v,vb)
        I.append(c)
        k += skip_data
        n += 1
    return I #mA
