# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 09:47:58 2020
Read data from trinity gage 
@author: bydd1
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import os 

file = r'D:\gage_data_trinity.txt'
x = pd.read_csv(file,delimiter=r'\t',skiprows = 46)

discharge = '133939_00060_00003'
stage = '133940_00065_00003'
dis = x[discharge][1:]
stage = x[stage][1:]
time = x['datetime'][1:]
d = [float(x) for x in dis]
stage = [float(x) for x in stage]
plt.figure()
plt.subplot(2,1,1)
plt.plot(np.arange(0, len(time),1), d)
plt.subplot(2,1,2)
plt.plot(np.arange(0, len(time),1), stage)