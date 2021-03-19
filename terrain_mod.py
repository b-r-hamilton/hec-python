# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 12:03:27 2021
Code to take in a BINARY raster file showing where the river channel is and 
add a LINEAR slope from TOP to BOTTOM and
add a POLYNOMIAL slope from side to side, with the minima AT THE RIVER CENTERLINE for 
every single ROW of the raster file 
@author: brynn
"""

import os 
from netCDF4 import Dataset
import numpy as np 
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
#%%
#code to modify array
def mod(top, bottom, slope, array):
    
    x = np.arange(0, array.shape[1] + 1000) #0,1,..., x-dim of input arr
    y = np.arange(0, array.shape[0])
    x_p = [-len(x)/2, 0, len(x)/2] #[0, 1/2 * x_dim, x_dim]
    y_p = [top, bottom, top] 
    
    #polynomial function with minima in center 
    def poly_func(input_data, a, b, c):
        return a*(input_data-b)**2 + c
    
    #call curve fit on the 2, 3-data point arrays
    popt, _ = curve_fit(poly_func, x_p, y_p)
    
    #fill in curve array (this is 1D) with polynomial function with calculated coeffs
    curve = poly_func(x, *popt)
    plt.figure()
    plt.plot(x, curve)
    
    #make the curve array 
    basin_slope = np.linspace(slope, 0.75*slope, len(y))
    
    mult_array = np.empty(array.shape) #empty array to populate with multiplied 
    
    #subtract 1 from the input array so the boolean works out the way I want
    invert = 1 - array
    
    #iterate over the y_dim, populating each row of the empty array with curve function
    for i in range(mult_array.shape[0]):
        
        current_vals = np.squeeze(invert[i, : ]) #row in question
        indices = []
        for j in range(len(current_vals)):
            if current_vals[j] == 0 and j > 100 and j < 2400:
                indices.append(j)
        left = indices[0]
        right = indices[-1] #this tells us first and last river edge index
        
        print((left, right))
        new_row = np.zeros(current_vals.shape)
        new_row[:left] = np.flip(curve[:left])
        new_row[right:] = curve[:len(new_row)-right]
        
        slope_val = basin_slope[i]
        mult_array[i, :] = new_row * slope_val     
    
    return mult_array

#%%
#INPUTS
#src_file: file to modify
#trg_file: where I'll put the printed netcdf with polynomial sloped basin
#top: maxima (edges) of sloped basin 
#bottom: minima(center) of sloped basin 
#s: slope 
def create_sloped_basin(src_file, trg_file, t, b, s):
    src = Dataset(src_file)
    trg = Dataset(trg_file, mode='w')

    # Create the dimensions of the file
    for name, dim in src.dimensions.items():
        trg.createDimension(name, len(dim) if not dim.isunlimited() else None)

    # Copy the global attributes
    trg.setncatts({a:src.getncattr(a) for a in src.ncattrs()})

    # Create the variables in the file
    for name, var in src.variables.items():
        
        if name == 'floodp2':
            trg.createVariable(name, np.dtype('float64'), var.dimensions)
        else:
            trg.createVariable(name, var.dtype, var.dimensions)
        # Copy the variable attributes
        trg.variables[name].setncatts({a:var.getncattr(a) for a in var.ncattrs()})
        
        # Copy the variables values (as 'f4' eventually)
            #modify fp2 
        if name == 'floodp2':
            data = src.variables[name][:].data
            new_data = mod(t, b, s, data) #MOD HERE
            trg.variables[name][:] = new_data
        else: 
            trg.variables[name][:] = src.variables[name][:]

    # Save the file
    trg.close()

#%%

d = r'C:\Users\burek\Documents\ArcGIS'
os.chdir(d)
file = r'new_input_rast.nc'
newfile = 'new_65665.nc'

maxima = 6.5
minima = 6
create_sloped_basin(file, newfile, maxima, minima, 1)

#%%
nc2 = Dataset(newfile)
x = nc2['x'][:].data
y = nc2['y'][:].data
data = nc2['floodp2'][:].data
nc2.close()

mesh = plt.pcolormesh(data, cmap = 'coolwarm')
plt.colorbar(mesh)