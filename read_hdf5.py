# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:01:12 2021
Code for reading hdf file of HEC-RAS results and plotting several DEPTH values 
and for plotting several VELOCITY values 
@author: brynn
"""
import h5py
import os 
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np 

#%%
#change into directory where hdf file is 
os.chdir(r'D:\HECRAS')
filename = "modified1.p15.hdf" #file of interest name 

f = h5py.File(filename, "r") #use h5py library to read file 

# List all groups
print("Keys: %s" % f.keys())

#access depth and velocity arrays 
#NOTE: these are indexed by [time, index]
#index refers to a CELL (for depth) or CELL FACE (for velocity) index
#don't currently know how to plot a mesh/contour of results because of complications with HEC mesh
#find cell or cell face index by RIGHT CLICK in RASMAPPER and select "Plot Property Table"
depth = f['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['2D Flow Areas']['2dflow']['Depth'][:]
velocity = f['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['2D Flow Areas']['2dflow']['Face Velocity'][:]
#%%
#get time series 
time = f['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['Time'][:]

#convert time series to datetime by linear spacing between known start/end date 
start = pd.Timestamp(2021, 2, 26, 0)
end = pd.Timestamp(2021, 3, 2, 3)
t = np.linspace(start.value, end.value, len(time))
t = pd.to_datetime(t)
time = t
#%%
#this code runs through a given list of cell numbers and plots them 
os.chdir(r"C:\Users\burek\Documents\Brynn")
cell_numbers_file = r'cell_numbers.xlsx'
cn = pd.read_excel(cell_numbers_file, header = None, index_col = 0)

def plot(indices, legend, title):
    plt.figure()
    data_to_plot = []
    for i in indices:
        data_to_plot.append(depth[:, cn[1][i]])
    for d in data_to_plot: 
        plt.plot(time, d)
    plt.legend(legend)
    plt.xlabel('Time')
    plt.ylabel('Depth [ft]')
    plt.xticks(rotation = 60)
    plt.title(title)


plot([3,7,12], ['Upper', 'Middle', 'Lower'], 'Channel Depth')
plot([4,13], ['Upper', 'Lower'], 'Hydraulic Connection Depth')
plot([5, 9, 14], ['Upper', 'Middle', 'Lower'], 'Oxbow Lake Depth')

#%%

#plot velocities at upper river cross-section 
v1 = velocity[:, 15571]
v2 = velocity[:, 15568]
v3 = velocity[:, 6194]
v4 = velocity[:, 6188]
v5 = velocity[:, 4086]
v_t = np.linspace(start.value, end.value, velocity.shape[0])
v_t = pd.to_datetime(v_t)

plt.figure()
all_v = [v1,v2,v3,v4,v5]
for v_thing in all_v:
    plt.plot(v_t, v_thing, alpha = 0.5)
    
v_array = np.ones(shape = (len(v1), 5))

for i in range(5):
    v_array[:, i] = all_v[i]
v_avg = v_array.mean(axis = 1)
    
plt.legend([1,2,3,4,5])

plt.plot(v_t, v_avg, linewidth = 10, alpha = 0.5, color = 'red')


